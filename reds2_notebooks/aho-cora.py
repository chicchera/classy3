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

# # Test Aho-Corasick
#
# - [SEE Keyword matching with Aho-Corasick | ieva.rocks](http://ieva.rocks/2016/11/24/keyword-matching-with-aho-corasick/)  
# - [enum — Support for enumerations — Python 3.10.10 documentation](https://docs.python.org/3.10/library/enum.html)
#   - [enum — Basic tutorial](https://docs.python.org/3.12/howto/enum.html#enum-basic-tutorial)  
#   - [enum — Advanced tutorial](https://docs.python.org/3.12/howto/enum.html#enum-advanced-tutorial)  
#   - [enum — Cookbook](https://docs.python.org/3.12/howto/enum.html#enum-cookbook)
# ### To add support for enums at the db level see:  
# [How to create ENUM type in SQLite? - Stack Overflow](https://stackoverflow.com/a/10811837/18511264)

# +
# pylint: disable=undefined-variable
# from typing importstr
import json
import os
import pathlib
import ipykernel
from platform import python_version
import ahocorasick as ahc
from typing import Union, Any, Optional, TYPE_CHECKING, cast
from collections import Counter

print(f"Python version:  {python_version()}")
print(f"Number of processors: {os.cpu_count()}")


# -

def make_aho_automaton(kwds: list) -> ahc.Automaton:
    """Makes an automaton from a list of tuples(keywords, num_category"""
    automaton = ahc.Automaton()  # initialize
    for key, cat in kwds:
        automaton.add_word(key, (cat, key))  # add keys and categories
    automaton.make_automaton()  # generate automaton
    return automaton


def find_keywords___(s: str, automaton) -> list[str]:
    """Returns pairs of keywords, codes"""
    found_keywords = []
    for _, (cat, keyw) in automaton.iter(s):
        found_keywords.append((keyw.strip(), cat))

    return found_keywords


# ## WIA  

def find_keywords(s: str, automaton) -> list[str]:
    """Returns counter object with tuples made of the category code
    and the number of times it was found"""
    found_keywords = []
    for _, (cat, keyw) in automaton.iter(s):
        found_keywords.append(cat)

    return Counter(found_keywords)


# +
wdir: str = os.getcwd()
data_dir: str = wdir + "/data/"
json_file: str = "class2_dict.json"
file_name: str = data_dir + json_file

with open(file_name, "r", encoding="UTF-8") as f:
    classy: dict = json.load(f)
# -

# pylint: disable=invalid-name
categories: dict = {}
kwds: list = []
for num_cat, (str_cat, cats_list) in enumerate(classy.items(), 1):
    categories[str_cat] = num_cat
    for _ in cats_list:
        kwds.append((" " + _ + " ", num_cat))
# print(kwds)

automa = make_aho_automaton(kwds)
print(type(automa))

ss = """
tendrían un noviazgo con una chica chico con onlyfanspor que si y por que no y dale con la chica
"""

x = find_keywords___(ss, automa)
print(x)

x = find_keywords(ss, automa)
print(x)
