import os
from os.path import expanduser
from symspellpy import SymSpell, Verbosity
import re

# from ../../settings import get_GLOBS
from settings import get_GLOBS

GLOBS = get_GLOBS()

# DIC_PATH = GLOBS["PRG"]["PATHS"].get("CONFIG_PATH")
# DIC_NAME = GLOBS["MISC"]["DICTIONARY"]
# DICTIONARY = expanduser(os.path.join(DIC_PATH, DIC_NAME))
DICTIONARY = expanduser(
    os.path.join(
        GLOBS["PRG"]["PATHS"].get("CONFIG_PATH"), GLOBS["MISC"].get("DICTIONARY")
    )
)

SS_DISTANCE = 1
SS_VERBOSITY = Verbosity.TOP
SS_PREFIX_LEN = 7
sym_spell = SymSpell(
    max_dictionary_edit_distance=SS_DISTANCE, prefix_length=SS_PREFIX_LEN
)
sym_spell.load_dictionary(DICTIONARY, term_index=0, count_index=1)


def spell_text(text: str) -> str:
    """
    Cleans up text by converting to lowercase, removing punctuation and emojis, and correcting spelling errors.
    Args:
        text (str): the text to clean
    Returns:
        str: a plain string
    """
    if text is None:
        return None

    if text.startswith("view poll"):
        return None

    # check if there are digits in the string
    # TODO: move the number check to the result of the spelling
    # TODO: BEFORE ANY CLASSIFICATION!
    if re.search(r"\d", text):
        suggestions = sym_spell.lookup_compound(
            text.replace("@", "o")
            .replace("1", "i")
            .replace("3", "e")
            .replace("4", "a")
            .replace("5", "s")
            .replace("7", "t")
            .replace("0", "o"),
            max_edit_distance=SS_DISTANCE,
            ignore_term_with_digits=True,
            ignore_non_words=True,
        )
    else:
        suggestions = sym_spell.lookup_compound(
            text,
            max_edit_distance=SS_DISTANCE,
            ignore_term_with_digits=True,
            ignore_non_words=True,
        )
    return "".join(suggestions[0].term)
