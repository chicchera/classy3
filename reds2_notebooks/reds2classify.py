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
# For importing other notebooks files see: https://stackoverflow.com/a/52923466/18511264
# -

# ## Imports

# +
import warnings
# warnings.filterwarnings('ignore')

import ipywidgets as widgets
from IPython.display import display

# from txtlists
import re
import unidecode

#from txtutils
import os
from os.path import exists, expanduser
import demoji
import unidecode
from unicodedata import normalize

from prettyprinter import pprint

import json 
import functools
import math

import pandas as pd
import sqlite3
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
        logging.DEBUG: 'lightblue',
        logging.INFO: 'dodgerblue',
        logging.WARNING: 'goldenrod',
        logging.ERROR: 'crimson',
        logging.CRITICAL: 'firebrick'
    }
    
    def __init__(self):
        super().__init__(
            '<span style="font-weight: bold; color: green">{asctime}</span> '
            '[<span style="font-weight: bold; color: {levelcolor}">{levelname}</span>] '
            '{message}',
            style='{'
        )
    
    def format(self, record):
        record.levelcolor = self.level_colors.get(record.levelno, 'black')
        return HTML(super().format(record)) 
    

# -

log = logging.getLogger()
handler = DisplayHandler()
handler.setFormatter(HTMLFormatter())
log.addHandler(handler)
log.setLevel(logging.DEBUG)

# ## Stopwords

# ### no_stopwords(s: str) -> str:

# +
# stopwords_es = ''
with open("stopwords_es.txt", 'r') as f:
    stopwords_es = set(f.read().splitlines())

# print(stopwords_es)
# -

def no_stopwords(s: str) -> str:
    if s is None:
        return None
    sset = set(s.split())
    sset.difference_update(stopwords_es)
    return ' '.join(sset)


# ### row_no_stops(row)

def row_no_stops(row):
    title = no_stopwords(row['title'])
    body = no_stopwords(row['body'])
    
    listy = [title, body]
    return pd.Series(listy)
    


# ## Text functions

xx = "yo iría al viaje conoces gente nueva conoces un lugar nuevo la vida es solo una"
print(no_stopwords(xx))


# ### unique_list(l: list) -> list:

def unique_list(l: list) -> list:
    ''' Remove duplicate words from list maintaining order
        see : https://stackoverflow.com/a/7794257 '''
    ulist = []
    [ulist.append(x) for x in l if x not in ulist]
    return ulist


# ## Database

# ### Db constants

CHUNK = 100000
CHUNK2 = int(CHUNK * 2)
CHUNK3 = int(CHUNK * 3)

# #### remote db

# +
DFR_EXISTS = False
# dfr_path = '~/.SomeGuySoftware/DownloaderForReddit'
dfr_path = '~/.______________SomeGuySoftware/DownloaderForReddit'
dfr_name = 'dfr.db'
dfr_db = expanduser(os.path.join(dfr_path, dfr_name))

dfr_alias = 'dfr'
# check if dfr exists (so we don't try to access it)
DFR_EXISTS = os.path.exists(dfr_db)

ATTACH_DFR = f"ATTACH DATABASE '{dfr_db}' AS {dfr_alias}"
print(dfr_db)
# -

# #### local db

CREATE_LOCAL_DB = False
FLUSH_CATEGORY_TABLE = True
FLUSH_POSTS_BASE = True
db_path = '.'
db_name = 'reds.db'
db_schema_path = '~/miniconda3/envs/reds2/notebook'
db_schema_name = 'db_schema.sql'
db_schema = expanduser(os.path.join(db_schema_path, db_schema_name))
db = expanduser(os.path.join(db_path, db_name))
DROP_LOCAL_DB = CREATE_LOCAL_DB and os.path.exists(db)


# ### Db functions & classes

# + [markdown] jp-MarkdownHeadingCollapsed=true
# #### class dbs_cursor()
# -

class dbs_cursor():
    ''' returns a connection on stats.db wir dfr.db attached
        return: curso object or None
    '''

    def __init__(self, msg=''):
        self._conn = self.create_conn()
        if self._conn is not None:
            self._conn.row_factory = sqlite3.Row
            # self._conn.execute(GLOBS.remotedb.get('attach'))
            self._conn.execute(ATTACH_DFR)

    def __enter__(self):
        return self._conn.cursor()

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


# + [markdown] jp-MarkdownHeadingCollapsed=true
# #### class dbs_connection()
# -

class dbs_connection():
    ''' returns a connection on stats.db wir dfr.db attached
        return: Connection object or None
    '''

    def __init__(self, msg=''):
        self._conn = self.create_conn()
        if self._conn is not None:
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


# ###  clean_sql(sql: str) -> str:

def clean_sql(sql: str) -> str:
    ''' Returns an sql uery formatted as a long string (God know what for...)'''
    return " ".join(sql.split())


# ## Queries

# ### vw_base (UNION posts & comments)

def create_vw_base(conn)-> str:
    conn.execute( '''
        CREATE VIEW IF NOT EXISTS vw_base AS
        SELECT
            title,
            body,
            rid_post,
            NULL AS rid_comment
        FROM posts
        UNION
        SELECT
            NULL AS title,
            body,
            rid_post,
            rid_comment
        FROM comments
        ORDER BY rid_post, rid_comment;
    ''')
    return "vw_base"


# ### Extract records to tokenize from vw_base

SELECT title, body, rid_post, rid_comment 
FROM vw_base w
WHERE NOT EXISTS (
SELECT 1 FROM posts_base
WHERE rid_post = w.rid_post
AND rid_comment = w.rid_comment
AND tbl = 'S'
)
LIMIT 50000;


# ## Create vw_base(s: str):

def tmp_vw_base_x(s: str, conn) -> str:

    s = s.upper()
    qry_name = f'''vw_base_{s} ''' 
    
    conn.execute(f'''
        SELECT 
            w.title, 
            w.body, 
            w.rid_post, 
            w.rid_comment, 
            w.tbl
        FROM 
            vw_base w 
            LEFT OUTER JOIN posts_base p ON p.rid_post = w.rid_post 
            AND p.rid_comment = w.rid_comment 
            AND p.tbl = "{s}" 
        WHERE 
            p.rid_post IS NULL 
            AND p.rid_comment IS NULL 
            AND p.tbl IS NULL;
        WHERE 
            p.rid_post IS NULL 
            LEFT OUTER JOIN posts_base c ON c.rid_comment = w.rid_comment 
            LEFT OUTER JOIN posts_base t ON t.tbl = "{s}"
        WHERE 
            p.rid_post IS NULL 
            AND c.rid_comment IS NULL 
            AND t.tbl IS NULL
        ORDER BY
            rid_post,
            rid_comment,
            tbl;
    ''')

    return qry_name


 print(tmp_vw_base_x("n"))   


# ### Count records returned by a query

# def sel_to_cnt(qry, conn) -> str:
def sel_to_cnt(qry, conn) -> str:
    '''returns a count query from a select one
       ignoring the LIMIT clause '''
    pos = qry.lower().find("limit")
    qry_part = qry[0: pos - 1]
    qry = f"SELECT COUNT (*) FROM ({qry_part})"
    return qry
    # num_recs = conn.execute(qry).fetchone()[0]
    # return num_recs


# ### qry_sel_posts_2_tokenize()

# see: [Python Set difference_update() Method](https://www.w3schools.com/python/ref_set_difference_update.asp)  
# Use Counter to return number of non stopwords in sentence?

def qry_sel_posts_2_tokenize(qry_type: str) -> str:
    ''' Returns a query for table post_base. qry_type can be:
            O -> no stopwords, original order, repeated tokens
            N -> no stopwords, any order, no repeated tokens
            L -> lemmas, based on N
            M -> lemmas, based on O
    '''
    return clean_sql(f'''
        SELECT 
            title, 
            body, 
            rid_post, 
            rid_comment 
        FROM 
            vw_base w 
        WHERE 
            NOT EXISTS (
                SELECT 1 
            FROM 
                posts_base 
            WHERE 
                rid_post = w.rid_post 
                AND rid_comment = w.rid_comment 
                AND tbl = '{qry_type}' ) 
        LIMIT {CHUNK};   
    ''')


# # RUN

start_time = time.perf_counter()

# ### Flush category & posts_base tables

# +
conn = sqlite3.connect(db)  
c = conn.cursor()

if FLUSH_CATEGORY_TABLE:
    c.execute("DELETE FROM category;")
    # c.execute("DELETE FROM sqlite_sequence WHERE name='category';")

if FLUSH_POSTS_BASE:
    c.execute("DELETE FROM posts_base;")
    # c.execute("DELETE FROM sqlite_sequence WHERE name='posts_base';")
    
conn.close()

# -

# ## Remove stopwords

with dbs_connection() as conn:
    # logging.warning(qry_sel_posts_2_tokenize("N"))
    num_recs = sel_to_cnt(qry_sel_posts_2_tokenize("N"), conn)
    logging.warning(num_recs)
    # num_chunks = math.ceil(num_recs / int(CHUNK2))
    num_chunks = 2
    # with tqdm(total=num_recs, unit_scale=1, desc="Remove stopwords") as pbar:
        # print(num_chunks)
    for _ in range(num_chunks):
        # print("hello")
        df = pd.read_sql(qry_sel_posts_2_tokenize("N"), conn)
        # df[['title', 'body']] = df.progress_apply(row_no_stops, axis=1)
        df[['title', 'body']] = df.apply(row_no_stops, axis=1)
        df.to_sql('posts_base', conn, if_exists='append', index = False)
        # pbar.update(len(df))
            

if False:
    with dbs_connection() as conn:
        num_recs = sel_to_cnt(qry_import_comment(), conn)
        logging.warning(num_recs)
        num_chunks = math.ceil(num_recs  / CHUNK)
        # num_chunks = 2
        with tqdm(total=num_recs, unit_scale=1, desc="dfr.post records to import") as pbar:
            # print(num_chunks)
            for _ in range(num_chunks):
                # print("hello")
                df = pd.read_sql(qry_import_comment(), conn)
                df[['body']] = df.progress_apply(clean_comment_row, axis=1)
                # df['body'] = df['body'].apply(clean_body)
                df.to_sql('comments', conn, if_exists='append', index = False)
                # print("hello")
                pbar.update(len(df))

        print("END")

conn.close()

# +
end_time = time.perf_counter()
duration = round(end_time - start_time,0)

print(f"Stopwords removal time was -> {datetime.timedelta(seconds=duration)}")
