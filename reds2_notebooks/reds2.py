# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:light
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.14.5
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# # New version of a simple classification

# + [markdown] jp-MarkdownHeadingCollapsed=true
# ### Notes
#
# - For importing other notebooks files see: https://stackoverflow.com/a/52923466/18511264
# - For fast searches [pyahocorasick — ahocorasick documentation](https://pyahocorasick.readthedocs.io/en/latest/)
# - [ahocorasick - YouTube](https://www.youtube.com/results?search_query=ahocorasick)
# - [Python: Python pandas select from series strings that contain](https://copyprogramming.com/howto/python-pandas-select-from-series-strings-that-contain)
#
# -

# ## Imports

# +
import warnings

# warnings.filterwarnings('ignore')

import re
import unidecode

import os
from os.path import exists, expanduser
import demoji
import unidecode
from unicodedata import normalize

import ipykernel

from prettyprinter import pprint

import json
import functools
import math

import pandas as pd

import contextlib

import time
import datetime

from time import perf_counter
import sys

from inscriptis import get_text
from tqdm.auto import tqdm

tqdm.pandas()

import nltk
from nltk.corpus import stopwords

from collections import Counter

import ahocorasick as ahc


# +
# see https://stackoverflow.com/a/68930736/18511264
# for details of logger

import logging
from IPython.display import display, HTML


class DisplayHandler(logging.Handler):
    def emit(self, record):
        message = self.format(record)
        display(message)


class HTMLFormatter(logging.Formatter):
    level_colors = {
        logging.DEBUG: "lightblue",
        logging.INFO: "dodgerblue",
        logging.WARNING: "goldenrod",
        logging.ERROR: "crimson",
        logging.CRITICAL: "firebrick",
    }

    def __init__(self):
        super().__init__(
            '<span style="font-weight: bold; color: green">{asctime}</span> '
            '[<span style="font-weight: bold; color: {levelcolor}">{levelname}</span>] '
            "{message}",
            style="{",
        )

    def format(self, record):
        record.levelcolor = self.level_colors.get(record.levelno, "black")
        return HTML(super().format(record))


# -

log = logging.getLogger()
handler = DisplayHandler()
handler.setFormatter(HTMLFormatter())
log.addHandler(handler)
log.setLevel(logging.DEBUG)


def make_aho_automaton(keywords, filler=""):
    A = ahc.Automaton()  # initialize
    for key, cat in keywords:
        A.add_word(key, (cat, key))  # add keys and categories
    A.make_automaton()  # generate automaton
    return A


# ## Stopwords


def read_stopwords() -> set:
    """Read stopwords from a file, one word per line."""
    with open("stopwords_es.txt") as f:
        lines = f.read().splitlines()
    return set(lines)


sw_es = read_stopwords()

# ## WIP

sw_es2 = []
for w in sw_es:
    w = " " + w + " "
    sw_es2.append((w, 100))


# +
def make_aho_automaton(keywords):
    A = ahc.Automaton()  # initialize
    for key, cat in keywords:
        A.add_word(key, (cat, key))  # add keys and categories
    A.make_automaton()  # generate automaton
    return A


Astopwds = make_aho_automaton(sw_es2)


# -


def find_keyword_locations(line, A):
    line_indices = [False for x in line]
    for end_index, (cat, keyw) in A.iter(line):
        start_index = end_index - len(keyw) + 2  # start index after first space
        for i in range(start_index, end_index):  # end index excluding last space
            line_indices[i] = True
    return line_indices


def no_stopwords(text: str) -> str:
    """Remove stopwords from a sentence
    returns a string WITH duplicates
    """
    return " ".join([word for word in text.split() if word not in sw_es])


# +
# # %timeit x = no_stopwords(s)
# -

# ## SymSpell

# +
from spellchecker import SpellChecker

# #####################
# SymSpell
import pkg_resources
from symspellpy import SymSpell, Verbosity

DIC_PATH = "~/miniconda3/envs/reds2/prg/reds_utils"
DIC_NAME = "es-100l.txt"
DICTIONARY = expanduser(os.path.join(DIC_PATH, DIC_NAME))
# -

CHECK_SPELLING = True
CHECK_SPELLING_TXT = True  ########## ATN false is used for tests only
CHECK_SPELLING_WRD = False
SS_DISTANCE = 1
SS_VERBOSITY = Verbosity.TOP
ss = SymSpell(max_dictionary_edit_distance=SS_DISTANCE, prefix_length=7)
ss.load_dictionary(DICTIONARY, term_index=0, count_index=1)

# +
#
# #####################
# -

# ## Text Constants

# ### RegEx

re_nums_only = re.compile(r"^[0-9]*$")
re_nums_mix = re.compile(r"([A-Za-z\u00C0-\u017F]+[\d@]+[\w@]*|[\d@]+[A-Za-z]+[\w@]*)")
wrds_with_nums = re.compile(
    r"([A-Za-z\u00C0-\u017F]+[\d@]+[\w@]*|[\d@]+[A-Za-z]+[\w@]*)"
)


# ### is_ama

ama_words = {
    "libres de preguntar",
    "hagan sus preguntas",
    "pregunte lo que quieran",
    "pregunten lo que quieran",
    "pregúntenme",
    "preguntad",
    "pregúntame",
    "preguntame",
    "alguna pregunta",
    "pregunten",
    "ama",
    "amaa",
    "tienen preguntas",
    "preguntas",
}


def is_ama(s: str) -> bool:
    '''Searches in "s" if there are terms contained in "ama_words"'''
    return any(word in s for word in ama_words)


ama_words2 = {
    " libres de preguntar ",
    " hagan sus preguntas ",
    " pregunte lo que quieran ",
    " pregunten lo que quieran ",
    " pregúntenme ",
    " preguntad ",
    " pregúntame ",
    " preguntame ",
    " alguna pregunta ",
    " pregunten ",
    " ama ",
    " amaa ",
    " tienen preguntas ",
    " preguntas ",
}


# +
def make_ama_automaton(kwds: list) -> ahc.Automaton:
    """Makes an automaton from a list of tuples(keywords, num_category"""
    automaton = ahc.Automaton()  # initialize
    for term in ama_words2:
        automaton.add_word(term, 1)  # add keys and categories
    automaton.make_automaton()  # generate automaton
    return automaton


ama_automaton = make_ama_automaton(ama_words2)


# +
def is_ama2(s: str, ama_automaton) -> bool:
    found_keywords = []
    for _, term in ama_automaton.iter(s):
        found_keywords.append(term)

    return Counter(found_keywords)


ama_automata = make_ama_automaton(ama_words2)
# -

s = """
chicas de y edit me considero el chico ideal sentimentalmente hablando pregunten lo que quieran y en base a mí repuesta seguirán pensando que soy alguien que vale mucho la pena cómo sería el chico ideal para ustedes

"""

# %timeit x = is_ama(s)

# %%timeit
x = is_ama2(s, ama_automata)

print(x)

# %timeit x = no_stopwords(s)

# %%timeit
new_text_removed = []
new_text_replaced = []
for line in s:
    line_indices = find_keyword_locations(line, Astopwds)
    line = list(line)  # split string into list
    new_line = "".join([line[i] if not x else "" for i, x in enumerate(line_indices)])
    new_text_removed.append(new_line)
    new_line = "".join([line[i] if not x else "-" for i, x in enumerate(line_indices)])
    new_text_replaced.append(new_line)

# ### is_serio

serio_words = ["pregunta seria", "serio", "respuestas serias"]


def is_serio(s: str) -> bool:
    '''Searches in "s" if there are terms contained in "serio_words"'''
    return any(word in s for word in serio_words)


# ### spell_wrd(w) -> str:


def spell_wrd(w) -> str:
    if re_nums_only.match(w):
        return w
    if re_nums_mix.match(w):
        w = (
            w.replace("1", "i")
            .replace("3", "e")
            .replace("4", "a")
            .replace("5", "s")
            .replace("7", "t")
            .replace("0", "o")
        )
    suggestions = ss.lookup(
        w,
        SS_VERBOSITY,
        max_edit_distance=SS_DISTANCE,
        include_unknown=True,
        transfer_casing=False,
    )
    return str(suggestions[0]).split(",")[0]


# ### spell_text(s: str) -> str:


def spell_text(s: str) -> str:
    """
    converts to lower text
    removes punctuation
    removes emojis
    """
    if CHECK_SPELLING:
        if wrds_with_nums.search(s):
            return " ".join(spell_wrd(w) for w in s.split())
        else:
            x = ""
            suggestions = ss.lookup_compound(s, max_edit_distance=SS_DISTANCE)
            for suggestion in suggestions:
                x += suggestion.term

            return x
    else:
        if s is None:
            return None

        s = s.strip().lower().replace("/", " ").replace("@", "o")

        if s.startswith("view poll"):
            return None

        # remove punctuation
        s = re.sub(r"[^\w\s]", " ", s)
        # remove multiple white spaces
        s = " ".join(s.split())
        # remove all the emojis, if any
        return demoji.replace(s, "")


# ## Text functions

# ### unique_list(l: list) -> list:


def unique_list(l: list) -> list:
    """Remove duplicate words from list maintaining order
    see : https://stackoverflow.com/a/7794257"""
    ulist = []
    [ulist.append(x) for x in l if x not in ulist]
    return ulist


# ### no_html(s: str) -> str:


def no_html(s: str) -> str:
    if s is None:
        return ""
    # return get_text(s).strip()
    return get_text(s)


# ### clean_text(s: str) -> str:


def clean_text(s) -> str:
    if s is None:
        return None

    if s.startswith("view poll"):
        return None

    return spell_text(s.replace("@", "o"))


# ### clean_title(s: str) -> str:


def clean_title(s: str) -> str:
    return clean_text(s)


# ### clean_body(s: str) -> str:


def clean_body(s: str) -> str:
    return clean_text(no_html(s))


# ### clean_post_row(row) -> list:


def clean_post_row(row):
    title = clean_title(row["title"])
    body = clean_body(row["body"])
    # ama = is_ama(title)

    listy = [title, body, is_ama(title), is_serio(title)]
    return pd.Series(listy)


# ### clean_comment_row(row) -> list:


def clean_comment_row(row):
    return pd.Series(clean_body(row["body"]))


# ## query functions

# ### Clean query: removes all blank characters


def clean_sql(sql: str) -> str:
    return " ".join(sql.split())


# ### Count records returned by a query


def sel_to_cnt(qry, conn) -> str:
    """returns a count query from a select one
    ignoring the LIMIT clause"""
    qry = qry.lower().partition("limit")[0]
    qry = "SELECT COUNT (*) FROM " + qry.partition("from")[2]
    num_recs = conn.execute(qry).fetchone()[0]
    return num_recs


# ## Create the database (or drop and recreate - **No data is saved**)

# ### Db constants

CHUNK = 50_000

# #### remote db

# +
DFR_EXISTS = False
# dfr_path = '~/.SomeGuySoftware/DownloaderForReddit'
dfr_path = "~/.______________SomeGuySoftware/DownloaderForReddit"
dfr_name = "dfr.db"
dfr_db = expanduser(os.path.join(dfr_path, dfr_name))

dfr_alias = "dfr"
# check if dfr exists (so we don't try to access it)
DFR_EXISTS = os.path.exists(dfr_db)

ATTACH_DFR = f"ATTACH DATABASE '{dfr_db}' AS {dfr_alias}"
print(dfr_db)
# -

# #### local db

CREATE_LOCAL_DB = True
db_path = "."
db_name = "reds.db"
db_schema_path = "~/miniconda3/envs/reds2/notebook"
db_schema_name = "db_schema.sql"
db_schema = expanduser(os.path.join(db_schema_path, db_schema_name))
db = expanduser(os.path.join(db_path, db_name))
DROP_LOCAL_DB = CREATE_LOCAL_DB and os.path.exists(db)


# ### Db functions & classes

# #### class dbs_cursor()


class dbs_cursor:
    """returns a connection on stats.db wir dfr.db attached
    return: cursor object or None
    """

    def __init__(self, msg=""):
        self._conn = self.create_conn()
        if self._conn is not None:
            self._conn.row_factory = sqlite3.Row
            self._conn.execute("pragma foreign_keys=ON")
            # self._conn.execute(GLOBS.remotedb.get('attach'))
            self._conn.execute(ATTACH_DFR)
            self._crsr = self._conn.cursor()

    def __enter__(self):
        return self._crsr

    def __exit__(self, type, value, traceback):
        _crsr.close()
        self._conn.commit()
        self._conn.close()

    def create_conn(self):
        conn = None
        try:
            # conn = sqlite3.connect(GLOBS.localdb.get('name'))
            conn = sqlite3.connect(db)
        except Error as e:
            print(e)
        return conn


# #### class dbs_connection()


class dbs_connection:
    """returns a connection on stats.db wir dfr.db attached
    return: Connection object or None
    """

    def __init__(self, msg=""):
        self._conn = self.create_conn()
        if self._conn is not None:
            self._conn.execute("pragma foreign_keys=ON")
            self._conn.row_factory = sqlite3.Row
            # self._conn.execute(GLOBS.remotedb.get('attach'))
            self._conn.execute(ATTACH_DFR)

    def __enter__(self):
        return self._conn

    def __exit__(self, type, value, traceback):
        self._conn.commit()
        self._conn.close()

    def create_conn(self):
        conn = None
        try:
            # conn = sqlite3.connect(GLOBS.localdb.get('name'))
            conn = sqlite3.connect(db)
        except Error as e:
            print(e)
        return conn


# ### Create local db

# +
if DROP_LOCAL_DB:
    if os.path.exists(db):
        os.remove(db)

if CREATE_LOCAL_DB:
    if os.path.exists(db):
        os.remove(db)

# print(db_schema)

sql = ""
f = open(db_schema, "r")
lines = f.readlines()
for l in lines:
    if l.startswith("-- END"):
        break
    elif l.startswith("--") or not l.rstrip():
        continue
    sql += l

queries_list = sql.split(";")


conn = sqlite3.connect(GLOBS["DB"].get("local"))
c = conn.cursor()
# if DFR_EXISTS:
#     c.execute(ATTACH_DFR)

for qry in queries_list:
    print(qry + ";")
    c.execute(qry)
conn.close()


# +
# conn = sqlite3.connect(db)
# c = conn.cursor()
# c.execute(ATTACH_DFR)
create
# ### Import posts / comments

# #### qry_import_post()


def qry_import_post():
    return clean_sql(
        f"""
        SELECT
            "id" AS "dfrid_post",
            "reddit_id" AS "rid_post",
            "author_id" AS "dfrid_author",
            "subreddit_id" AS "dfrid_sub",
            "title",
            "text_html" as "body",
            "strftime"('%s', "date_posted") as "date_posted",
            "score",
            "nsfw",
            FALSE AS "ama",
            FALSE AS "serio",
            0 AS "tonto_index"
        FROM
            dfr.post remote
            WHERE remote.id NOT IN
                (SELECT "dfrid_post" FROM posts)
        LIMIT {CHUNK};
    """
    )


# + [markdown] jp-MarkdownHeadingCollapsed=true
# #### qry_import_comment()
# -

# #### qry_import_comment()


def qry_import_comment():
    return clean_sql(
        f"""
        SELECT
            "id" AS "dfrid_comment",
            "reddit_id" AS "rid_comment",
            "post_id" AS "dfrid_post",
            "parent_id" AS "dfrid_parent",
            "body_html" AS "body",
            "score",
            "strftime"('%s', "date_posted") AS "date_posted",
            "author_id" AS "dfrid_author",
            "" AS "rid_author",
            NULL AS "is_op"
        FROM
            dfr.comment remote
            WHERE remote.id NOT IN
                (SELECT "dfrid_comment" FROM comments)
        LIMIT {CHUNK}
        ;
    """
    )


# ### Import dfr.post & dfr.comment
#
# **This procedure imports the data from dfr and
# normalizes it in order to be classified**
#
# Nomalization consists of:
# - remove html
# - convert to lowercase
# - replace "@" with "o"
# - remove special chars, punctuation and double spaces
# - remove emojis
# - transform embedded numbers into letters
# - correct spelling
#

start_time = time.perf_counter()

with dbs_connection() as conn:
    num_recs = sel_to_cnt(qry_import_post(), conn)
    num_chunks = math.ceil(num_recs / CHUNK)
    # num_chunks = 2
    with tqdm(total=num_recs, unit_scale=1, desc="dfr.post records to import") as pbar:
        # print(num_chunks)
        for _ in range(num_chunks):
            # print("hello")
            df = pd.read_sql(qry_import_post(), conn)
            df[["title", "body", "ama", "serio"]] = df.progress_apply(
                clean_post_row, axis=1
            )
            df.to_sql("posts", conn, if_exists="append", index=False)
            pbar.update(len(df))

with dbs_connection() as conn:
    num_recs = sel_to_cnt(qry_import_comment(), conn)
    num_chunks = math.ceil(num_recs / CHUNK)
    # num_chunks = 2
    with tqdm(total=num_recs, unit_scale=1, desc="dfr.post records to import") as pbar:
        # print(num_chunks)
        for _ in range(num_chunks):
            # print("hello")
            df = pd.read_sql(qry_import_comment(), conn)
            df[["body"]] = df.progress_apply(clean_comment_row, axis=1)
            # df['body'] = df['body'].apply(clean_body)
            df.to_sql("comments", conn, if_exists="append", index=False)
            # print("hello")
            pbar.update(len(df))

    print("END")

# +
queries_list = list()

queries_list.append(("Empty ids, just in case", """DELETE FROM ids;"""))

queries_list.append(
    (
        "Extract ids from posts",
        """
        INSERT INTO ids (tbl, id_dfr, id_red)
        SELECT
            "P" AS tbl,
            dfrid_post AS id_dfr,
            rid_post AS id_red
        FROM posts;""",
    )
)

queries_list.append(
    (
        "Extract ids from comments",
        """
    INSERT INTO ids (tbl, id_dfr, id_red)
    SELECT
        "C" AS tbl,
        dfrid_comment AS id_dfr,
        rid_comment AS id_red
    FROM comments;""",
    )
)

# lqry.append(('Update known authors ids in comments', '''
#     UPDATE comments
#     SET rid_author = posts.dfrid_author
#     FROM
#         (SELECT id_red FROM ids
#             WHERE id_dfr = comments.dfrid_author);'''))

queries_list.append(
    (
        "Import users from dfr.reddit_object",
        """
    INSERT INTO objects (dfrid_object, name, tbl)
    SELECT
        "id" AS dfrid_object,
        "name",
        substr(object_type,1,1) AS tbl
    FROM dfr.reddit_object remote
    WHERE remote.id NOT IN
        (SELECT "dfrid_object" FROM objects);""",
    )
)

queries_list.append(
    (
        "Update is_op in comments",
        """
    UPDATE comments
        SET is_op = TRUE
        WHERE EXISTS
        (SELECT *
        FROM posts p
        WHERE comments.dfrid_post == p.dfrid_post
        AND   comments.dfrid_author == p.dfrid_author);""",
    )
)

queries_list.append(
    (
        "Update reddit post id in comments",
        """
    UPDATE comments
    SET rid_post =
    (SELECT ids.id_red
        FROM ids
        WHERE ids.id_dfr = comments.dfrid_post
        AND ids.tbl = "P")
    WHERE rid_post IS NULL;""",
    )
)

# -

with dbs_connection() as conn:
    for qry in queries_list:
        if False:
            print("-------------------------------------")
            print(qry[0])
            print(qry[1])
        conn.execute(qry[1])

conn.close()

# +
end_time = time.perf_counter()
duration = round(end_time - start_time, 0)

print(f"Import time was -> {datetime.timedelta(seconds=duration)}")

# +
s = """

resulta que desde hace cuatro años estoy buscando una campera que ya no está en
venta porque fue vendida en el 1990 aprox sólo tengo fotos de esta y aparentemente no
existe otro ejemplar la campera es de marca pero aún así no he encontrado ni en
buscadores de imágenes un ejemplar idéntico a la campera existirá un sobre edit para
poder avanzar en mi búsqueda para mi el caso más extremo fue que a mí tipo le tuvieron
que amputar la primera y segunda falange de un dedo del pie porque durante y meses estaba
teniendo una herida infectada y su doctora crea que se le había inflamado y lo único que
hacia era mandarle reposo y medicamentos para el dolor tengo una amiga su mamá se casó
de otro hombre cuando ella tenía y años y desde ahí empezó su infierno bueno imagino
que este señor al principio aparentaba ser el mejor hombre del mundo era súper lindo
con mi amiga y con su mamá por qué se los juro que se hizo es el diablo andante bueno
nosotras tenemos y y años entonces han pasado casi y desde que este señor se metió a
sus vidas tienen indicios de psicópata es agresivo no en el sentido físico sino verbal
es manipulador con su mamá es muy histérico y siempre la agarra con mi amiga y le dices
cosas sobre su cuerpo le prohíbe cosas la castiga por mínima cosa que haga sea buena o
mala de hecho a veces le prohíbe ver a sus abuelos y dios maternos por que ellos saben
cómo es el y no les cae bien y a lo que el como rencor no permite que la vean a ella
saben que es lo pero que su mamá permite este tipo de abusos siendo que el ni siquiera
es su papá y siempre ha sido así desde que ellos eran novios y jamás le ha prohibido o
llamado la atención de este tipo de actitudes con su propia hija mi tía mamá de mi amiga
es muy linda obvio tiene su carácter pero es todas las jamás son así pero de ahí en fuera
es demasiado manipulada por su esposo yo no sé que ronda por su cabeza por de verdad que no
la puedo entender o sea como deja que todo esto pace como no de divorcia de este demonio de
ser humano está loco les contaré una anécdota que ella me contó era de mañana y el la iba
llevando a la escuela y mi amiga se trajo un termo ye ti es importante lo del termo ye ti y
uno de platico normal para el agua bueno pues en camino a la escuela este señor muy serio le
pregunta y si por que lleva ese termo que si se lo iba a regalar a alguien y ella le contesto
que no que simplemente tenía café por qué no durmió bien y que era para estar más despierto
pues a lo que el muy enojado le empieza a gritar que es una mentirosa que si a quien se lo
regalaría que el no era ningún pendejo como para creerse sus mentiras ella se quedó callada
a lo que se puso su cubre bocas por qué se le estaban saliendo las lágrimas y no quería que
la regalara por llorar a lo que esté señor reacciona otra vez histérico que si por que se por
que se ponía el cubre bocas si estaban en el carro y ella de inmediato se lo quito para ya no c
ausar problemas cuando llegaron a la escuela dejo el termo en el carro para ya no causar problemas
a lo que el le dice que si por y no se lleva el ye ti y ella le dice que ya no lo quiere a lo que el
empieza a reírse dice ella que como un psicópata y ya casi no recuerdo y paso ahí pero es cuando iba
entrando su maestra la vio llorando y le dijo quedarse el tiempo que quiera en la sala de maestros para
que se calmara mi amiga acaba de salirse de casa hace y días está con su tía por una pelea que tuvieron
no recuerdo por y bien pero de seguro fue por una montada ya no se que hacer siempre viene llorando amo
casa contándome lo que le hicieron ella quiere vivir con sus abuelos pero la amenazaron que si se iba ya no
le pagarían nada escuela comida ropa salidas etc ya no quiero que viva todo esto ayuda y edit como puedo
ayudar si es que no puedo de el lado legal

"""

ss = """
resulta que desde hace cuatro años estoy buscando una campera que ya no está en
venta porque fue vendida en el 1990 aprox sólo tengo fotos de esta y aparentemente no
existe otro ejemplar la campera es de marca pero aún así no he encontrado ni en
buscadores de imágenes un ejemplar idéntico a la campera existirá un sobre edit para

"""

# +
# print(is_ama(ss))

# +
# # %%timeit
# x1 = no_stopwords(s)
# # %timeit is_ama(s)
# print(is_ama(s))
# -

# !pip install -U ipykernel
