from symspellpy import SymSpell, Verbosity
import re
import sys
import traceback
import pandas as pd
from typing import List, Tuple

from utils.txt_utils import validate_non_empty_string
from settings import get_globs_key, dictionary_path
from app_logger import logger

def myhook(type, value, tb):
    trace = traceback.extract_tb(tb)
    caller = trace[-1]  # Get the last entry in the traceback (the caller)
    exc = traceback.format_exception_only(type, value)[0]
    print("Error in file:", caller.filename)
    print("Line:", caller.lineno)
    print("In function or method:", caller.name)
    print("Code line:", caller.line)
    print(exc)


sys.excepthook = myhook

dictionary = dictionary_path()

try:
    ss = SymSpell(max_dictionary_edit_distance=1, prefix_length=7)
    dictionary = dictionary_path()
    ss.load_dictionary(dictionary, term_index=0, count_index=1)
except Exception as e:
    logger.error(f"An error occurred while loading the dictionary: {str(e)}")

def symspell_correct(text: str,keep_case=False) -> str:
    """
    Tokenizes the input text into words, corrects misspelled words, and reconstructs the corrected text while maintaining original punctuation.

    Args:
        text (str): The input text to be corrected.

    Returns:
        str: The corrected text with misspelled words replaced.

    """
     # Define a regular expression pattern to tokenize the text into words
    word_pattern = re.compile(r'\b\w+\b')
    text = text.lower()
    # Tokenize the input text into words
    words = word_pattern.findall(text)

    # Correct misspelled words and build the corrected text
    corrected_text = []
    for word in words:
        suggestions = ss.lookup(
            word, Verbosity.CLOSEST, max_edit_distance=1, transfer_casing=keep_case
        )
        corrected_word = suggestions[0].term if suggestions else word
        corrected_text.append(corrected_word)

    # Reconstruct the corrected text while maintaining original punctuation
    reconstructed_text = ""
    for i, match in enumerate(word_pattern.finditer(text)):
        word_start, word_end = match.start(), match.end()
        reconstructed_text += text[word_start:word_end].replace(match.group(), corrected_text[i])

        # Add any punctuation or spaces between words
        if i < len(corrected_text) - 1:
            next_match = word_pattern.search(text[word_end:])
            if next_match:
                reconstructed_text += text[word_end:word_end + next_match.start()]

    return reconstructed_text


import re
from typing import List, Tuple


def symspell_correct_return_errors(row, text_col, corrected_col, misspells_col, keep_case=False):
    text = row[text_col]

    if not validate_non_empty_string(text):
        row[corrected_col] = None
        row[misspells_col] = None
        return row

    word_pattern = re.compile(r'\b\w+\b')
    words = word_pattern.findall(text)

    misspelled_words = []
    corrected_text = []

    for word in words:
        suggestions = ss.lookup(
            word, Verbosity.CLOSEST, max_edit_distance=1, transfer_casing=keep_case
        )
        corrected_word = suggestions[0].term if suggestions else word

        if corrected_word != word:
            misspelled_words.append(word)

        corrected_text.append(corrected_word)

    reconstructed_text = ""
    for i, match in enumerate(word_pattern.finditer(text)):
        word_start, word_end = match.start(), match.end()
        reconstructed_text += text[word_start:word_end].replace(match.group(), corrected_text[i])

        if i < len(corrected_text) - 1:
            next_match = word_pattern.search(text[word_end:])
            if next_match:
                reconstructed_text += text[word_end:word_end + next_match.start()]

    bad_words = ' '.join(misspelled_words)
    return pd.Series({corrected_col: validate_non_empty_string(reconstructed_text), misspells_col: validate_non_empty_string(bad_words)})
    # row[corrected_col] = validate_non_empty_string(reconstructed_text)
    # row[misspells_col] = validate_non_empty_string(bad_words)
    # return row

def _symspell_correct_return_errors(text: str, corrected: str, misspells: str, keep_case: bool = False):

    if not validate_non_empty_string(text):
        return pd.Series({corrected: None, misspells: None})

    word_pattern = re.compile(r'\b\w+\b')
    words = word_pattern.findall(text)

    misspelled_words = []
    corrected_text = []

    for word in words:
        suggestions = ss.lookup(
            word, Verbosity.CLOSEST, max_edit_distance=1, transfer_casing=keep_case
        )
        corrected_word = suggestions[0].term if suggestions else word

        if corrected_word != word:
            misspelled_words.append(word)

        corrected_text.append(corrected_word)

    reconstructed_text = ""
    for i, match in enumerate(word_pattern.finditer(text)):
        word_start, word_end = match.start(), match.end()
        reconstructed_text += text[word_start:word_end].replace(match.group(), corrected_text[i])

        if i < len(corrected_text) - 1:
            next_match = word_pattern.search(text[word_end:])
            if next_match:
                reconstructed_text += text[word_end:word_end + next_match.start()]

    bad_words = ' '.join(misspelled_words)
    return pd.Series({corrected: validate_non_empty_string(reconstructed_text), misspells: validate_non_empty_string(bad_words)})
