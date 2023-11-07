from language.dictionaries.dictionaries import Dictionaries
from language.stopwords.stopwords import Stopwords
from language.support.support_functions import read_words_and_punctuation

from utils.file_utils import diy_file_validate

"""
for passing code:
# Assuming you have a Dictionaries instance called self._dc
self._dc.set_text(self._very_long_text)

"""


class Texteval:
    def __init__(self, lang="es", steps=10):
        self._lang = lang
        self._dc = Dictionaries()
        self._sw = Stopwords()
        self._input_file = None
        self._content = None

    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, content):
        self._content = content

    @property
    def input_file(self):
        return self._input_file

    @input_file.setter
    def input_file(self, filename, num_words):
        success, message = diy_file_validate(filename)
        if not success:
            exit(0, f"File {filename}: {message}")
        self._input_file = filename
        self._content = read_words_and_punctuation(filename, num_words)
