from symspellpy import SymSpell, Verbosity
import re
import os
import pandas as pd
import numpy as np

from os.path import expanduser
from utils.txt_utils import validate_non_empty_string
from settings import get_globs_key, dictionary_path
from app_logger import logger


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


def symspell_correct_return_errors(text: str,keep_case=False) -> str:
    """
    Corrects misspelled words in the given text and returns the corrected text along with a list of misspelled words.

    Parameters:
    - text (str): The input text to be corrected.

    Returns:
    - reconstructed_text (str): The corrected text with misspelled words replaced.
    - misspelled_words (list): A list of misspelled words found in the input text.
    """
    text = text.lower()

    # Define a regular expression pattern to tokenize the text into words
    word_pattern = re.compile(r'\b\w+\b')

    # Tokenize the input text into words
    words = word_pattern.findall(text)

    # Initialize lists to store misspelled words and corrected words
    misspelled_words = []
    corrected_text = []

    for word in words:
        suggestions = ss.lookup(
            word, Verbosity.CLOSEST, max_edit_distance=1, transfer_casing=keep_case
        )
        corrected_word = suggestions[0].term if suggestions else word

        # Check if the word was corrected
        if corrected_word != word:
            misspelled_words.append(word)

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

    return reconstructed_text, misspelled_words

def correct_original(col_txt: str, col_misspells: str, extra_text='') -> pd.Series:
    """
    Corrects the original text in the given column by using the symspell_correct_return_errors function.

    Args:
        col_txt (str): The name of the column containing the original text.
        col_misspells (str): The name of the column to store the misspelled words.
        extra_text (str, optional): Additional text to include. Defaults to ''.
        is used instead of col_text if thhe origin of the text is different
    Returns:
        pd.Series: A pandas Series object containing the corrected text and the misspelled words.
    """
    corrected, misspells = symspell_correct_return_errors(col_txt)
    print(corrected, misspells)
    corrected = validate_non_empty_string(corrected)
    print(corrected)
    misspells = validate_non_empty_string(misspells)
    print(misspells)
    return pd.Series({col_txt: corrected, col_misspells: misspells})