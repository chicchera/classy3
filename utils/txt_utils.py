import re
import unidecode

import os
from os.path import exists, expanduser
import demoji
from unicodedata import normalize
import pandas as pd

import utils.txt_utils as tu

from settings import GLOBS, get_GLOBS
from inscriptis import get_text
from utils.spelling import spell_text
from settings import get_globs_key

# GLOBS = get_GLOBS()


re_nums_only = re.compile(r"^[0-9]*$")
re_nums_mix = re.compile(r"([A-Za-z\u00C0-\u017F]+[\d@]+[\w@]*|[\d@]+[A-Za-z]+[\w@]*)")
wrds_with_nums = re.compile(
    r"([A-Za-z\u00C0-\u017F]+[\d@]+[\w@]*|[\d@]+[A-Za-z]+[\w@]*)"
)


def read_stopwords() -> set:
    """Read stopwords from a file, one word per line."""
    # stops_file = GLOBS["PRG"]["PATHS"].get('CONFIG_PATH')
    stops_file = os.path.join(
        GLOBS["PRG"]["PATHS"].get("CONFIG_PATH"), GLOBS["MISC"].get("STOPWORDS")
    )
    with open(stops_file) as f:
        lines = f.read().splitlines()
    try:
        with open(stops_file) as f:
            lines = f.read().splitlines()
    except Exception as e:
        return None  # or handle the exception as appropriate
    return set(lines)


stopwords = read_stopwords()


ama_words = {
    "tienen preguntas",
    "pregúntenme",
    "pregúntame",
    "pregunten",
    "pregunten lo que quieran",
    "pregunte lo que quieran",
    "preguntas",
    "preguntame",
    "preguntad",
    "libres de preguntar",
    "hagan",
    "hagan sus preguntas",
    "amaa",
    "ama",
    "alguna pregunta",
}

serio_words = ["pregunta seria", "serio", "respuestas serias"]


# #####################
# SymSpell
# RECHECK: splitting the dictionary timings
# 106,959 submissions
# ss = SymSpell(max_dictionary_edit_distance=SS_DISTANCE, prefix_length=7)
# import submissions with one dictionary file = 02:34
# ss = SymSpell(max_dictionary_edit_distance=SS_DISTANCE, prefix_length=9)
# import submissions with one dictionary file = 02:14
# with just a bit of refactoring to be rechecked = 00:14


import pkg_resources
from symspellpy import SymSpell, Verbosity


# DIC_PATH = "/home/silvio/miniconda3/envs/classy3/prg/config"
# DIC_NAME = "es-100l.txt"
# DIC_PART_PREFIX = "dic_part_"
# DIC_PATH = GLOBS["PRG"]['PATHS'].get('CONFIG_PATH')
# DIC_NAME = GLOBS['MISC'].get('DICTIONARY')
# DICTIONARY = expanduser(os.path.join(DIC_PATH, DIC_NAME))
DIC_PATH = get_globs_key("PRG.PATHS.CONFIG_PATH")
DIC_NAME = get_globs_key("MISC.DICTIONARY.symspell")
DICTIONARY = f"{DIC_PATH}/{DIC_NAME}"
# -

CHECK_SPELLING = True
CHECK_SPELLING_TXT = True  ########## ATN false is used for tests only
CHECK_SPELLING_WRD = False
SS_DISTANCE = 1
SS_VERBOSITY = Verbosity.TOP

ss = SymSpell(max_dictionary_edit_distance=SS_DISTANCE, prefix_length=7)
ss.load_dictionary(DICTIONARY, term_index=0, count_index=1)


def no_html(s: str) -> str:
    """
    Returns the text without HTML tags
    Args:
        s (str): string with HTML tags
    Returns:
        str: input string without HTML tags
    """
    if s is None:
        return ""
    return re.sub(r"<.*?>", "", s)


def clean_text(text: str) -> str:
    """
    A function that takes in a string and returns a cleaned version of it. If the input string is None or starts with "view poll", the function returns None. Otherwise, it replaces all "@" with "o" and returns the result as a string.

    :param s: A string to be cleaned
    :return: A cleaned string
    """
    return spell_text(text)


def clean_body(text: str) -> str:
    """
    Takes a string `s` as input and returns a string with all HTML tags removed.
    The input string `s` is first passed to the `no_html` function, which removes all HTML tags.
    The result is then passed to the `clean_text` function, which performs additional cleaning operations such as removing extra whitespace.
    The final cleaned string is returned as output.

    :param s: A string containing HTML tags
    :type s: str
    :return: A string with all HTML tags removed and additional cleaning operations performed
    :rtype: str
    """
    return clean_text(no_html(text))


def clean_title(text: str) -> str:
    return clean_text(text)


def clean_post_row(row):
    title = clean_title(row["title"])
    body = clean_body(row["body"])
    # ama = is_ama(title)

    listy = [title, body, is_ama(title), is_serio(title)]
    return pd.Series(listy)


def clean_comment_row(row):
    return pd.Series(clean_body(row["body"]))


def is_ama(s: str) -> bool:
    '''Searches in "s" if there are terms contained in "ama_words"'''
    return any(word in s for word in ama_words)


def is_serio(s: str) -> bool:
    '''Searches in "s" if there are terms contained in "serio_words"'''
    return any(word in s for word in serio_words)


def spell_wrd(w) -> str:
    """
    Given a string `w`, this function checks if it only contains numbers. If it does, it returns the string.
    If the string contains mix of numbers and alphabets, it replaces the numbers with their corresponding
    alphabets (1 with i, 3 with e, 4 with a, 5 with s, 7 with t, and 0 with o) and returns the modified string.
    It then uses the `lookup` method of the `ss` object to suggest spelling corrections for the modified
    string. The suggestions are returned as a list of strings where the first element is the most likely
    suggestion. This function then returns the first suggestion as a string after stripping any additional
    information. The `ss` object is an instance of the SymSpell class, which is a fast and memory-efficient
    Python spell checking library. It has a `lookup` method that takes in a string, a verbosity level,
    a maximum edit distance, a flag to include unknown words, and a flag to transfer case from the input
    word to the output word. This function returns a string.
    """
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


def spell_wrd2(w) -> str:
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


def __no_stopwords(sentence) -> str:
    """
    Returns a string with all the stopwords removed from the input sentence.

    :param sentence: the input string to remove stopwords from.
    :type sentence: str
    :return: a string with all the stopwords removed.
    :rtype: str
    """
    return " ".join([word for word in sentence.split() if word not in stopwords])
