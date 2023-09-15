from symspellpy import SymSpell, Verbosity
import re
import os
from os.path import expanduser

from settings import get_globs_key


if not get_globs_key("MISC.DICTIONARY.use_alternate"):
    dictionary = get_globs_key("MISC.DICTIONARY.symspell")
else:
    dictionary = get_globs_key("MISC.DICTIONARY.subtitle")

# DIC_PATH = GLOBS["PRG"]["PATHS"].get("CONFIG_PATH")
# DIC_NAME = GLOBS["MISC"]["DICTIONARY"]
# DICTIONARY = expanduser(os.path.join(DIC_PATH, DIC_NAME))
DICTIONARY = expanduser(
    os.path.join(
        get_globs_key("PRG.PATHS.CONFIG_PATH"), dictionary)
    )

if DEFAULT_DICTIONARY:
    dictionary_es = "/home/silvio/miniconda3/envs/classy3/prg/config/es-100l-dic.txt"
else:
    dictionary_es = "/home/silvio/miniconda3/envs/classy3/prg/config/subtl_es.txt"

ss = SymSpell(max_dictionary_edit_distance=1, prefix_length=7)
ss.load_dictionary(dictionary_es, term_index=0, count_index=1)