import nltk
from nltk.corpus import stopwords
import string
import os
import re

import linecache
from symspellpy import SymSpell, Verbosity
from rich import print
import inspect

from collections import Counter
from utils.file_utils import file_validate, diy_file_validate

# nltk.data.path = ['/home/silvio/miniconda3/envs/classy3/nltk_data']
nltk.data.path.append('/home/silvio/miniconda3/envs/classy3/nltk_data')
# nltk.download('punkt')

# nltk.data.path.append('nltk.data.path.append('/home/silvio/miniconda3/envs/classy3/nltk_data)
# nltk.download('punkt')

stop_words = list(stopwords.words('spanish'))
# print(top_words)

from typing import List



def count_words(text: str) -> int:
    """
    Counts the number of words in a given text.

    Args:
        text (str): The text to be processed.

    Returns:
        int: The number of words in the text.
    """
    # Define a custom translation table to remove all punctuation, including ¡ and ¿
    custom_translation = str.maketrans('', '', string.punctuation + '¡¿')

    # Remove all punctuation and convert to lowercase
    text = text.translate(custom_translation).lower()

    # Split the text into words and count them
    words: List[str] = text.split()
    word_count: int = len(words)

    return word_count

class Stopwords:
    def __init__(self, language, stopwords):
        self._lang = None
        self._stopwords = set()
        self._c_stopwords = Counter()
        self._files = []
        self._disabled = False
        self._custom_translation = str.maketrans('', '', string.punctuation)
        self._text = None
        self._len_text = None

        if language := language.strip().lower():
            if language in ["es", "es_ES", "español", "spanish"]:
                self._lang = "spanish"
                self._custom_translation = str.maketrans('', '', string.punctuation + '¡¿')
            elif language in ["en", "en_US", "english"]:
                self._lang = "english"
            elif language in ["it", "italiano", "it_IT"]:
                self._lang = "italian"
            else:
                self._lang = None
                print("Language not  set")
                exit(0)

    def len_string(self, text):
        # Remove all punctuation and convert to lowercase
        tmp = text.translate(self._custom_translation)
        # Split the text into words and count them
        words = tmp.split()
        return len(words)

    def load_stopwords(self, files):
        if files:
            self._files = files
        # self._lang = lang

        def validate_files_argument(files):
            if files is None:
                return False  # Argument is None, not valid

            if isinstance(files, str):
                # If it's a single string, convert it to a list
                self._files = [files]
                return True

            if isinstance(files, list):
                # Check if the list is empty
                if not files:
                    return False

                # Check that all elements are of type string
                if all(isinstance(item, str) for item in files):
                    self._files = files
                    return True  # Valid list of strings

            return False  # Invalid

        if not validate_files_argument(files):
            self._disabled = True

        if not self._disabled:
            new_stopwords = []
            for filename in self._files:

                success, message = diy_file_validate(filename)
                if not success:
                    print(message)
                    continue

                with open(filename, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                    for line in lines:
                        if word := line.strip():
                            new_stopwords.append(word)
            self._c_stopwords = Counter(new_stopwords)
            self._stopwords = set(new_stopwords)
            print(self._c_stopwords)
            print("=" * 30)
        print(f"{self._stopwords=}")
        print(f"{self._c_stopwords=}")

    @property
    def language(self):
        return self._lang

    # @language.setter
    # TODO: ADD A SECOND LANGUAGE VALIDATOR
    # def language(self, val):
    #     self.validate_language(val)

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, val):
        self._text = val
        self._len_text = self.len_string(val)

    @property
    def len_text(self):
        return self._len_text
        # if self._text:
        #     self._len_text = self.len_string(self._text)
        # # # Remove all punctuation and convert to lowercase
        # tmp = self._text.translate(self._custom_translation)
        # # Split the text into words and count them
        # words = tmp.split()
        # return len(words)

    @property
    def files(self) -> list:
        return self._files

    @property
    def stopwords(self):
        return self._stopwords

    @property
    def c_stopwords(self):
        return self._c_stopwords

    def count_stopwords(self, text=None):
        if text is None:
            if not self._text:
                return 0
            text = self._text
        text = text.translate(self._custom_translation).lower()
        words = nltk.word_tokenize(text, self._lang)
        count = sum(1 for word in words if word in stopwords.words(self._lang))
        return count

    def count_stopwords_2(self, text=None):
        if text is None:
            if not self._text:
                return 0
            text = self._text
        text = text.translate(self._custom_translation).lower()
        words = set(nltk.word_tokenize(text, self._lang))
        count = len(words.intersection(self._stopwords))
        return count

    def count_stopwords_3(self, text=None):
        if text is None:
            if not self._text:
                return 0
            text = self._text
        total_stopwords = 0

        text = text.translate(self._custom_translation).lower()
        words = nltk.word_tokenize(text, self._lang)
        #stopword_counter = Counter(words)

        for word in words:
            if word in self._c_stopwords:
                total_stopwords += 1

        # total_stopwords = sum(stopword_counter[word] for word in self._c_stopwords)

        return total_stopwords