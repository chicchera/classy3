#################################### ORIGINAL
#!/usr/bin/env python3


import sys
import re
import regex
import string
import spacy
import pyphen
import timeit
import time
from rich import print
from yaspin import yaspin
from collections import namedtuple
from utils.txt_utils import count_words, count_letters
from language.dictionaries.dictionaries import Dictionaries
from language.stopwords.stopwords import Stopwords
from utils.file_utils import diy_file_validate


BOOkS_PATH = "/home/silvio/miniconda3/envs/classy3/prg/books/"
# books
SOLEDAD = BOOkS_PATH + "Cien Anos De Soledad.txt"
CATEDRAL = BOOkS_PATH + "Conversación en La Catedral.txt"
JULIA = BOOkS_PATH + "La tia Julia.txt"

CountSentences = namedtuple("CountSentences", ["sentences", "punctuation"])


class TextProcessor:
    def __init__(self):
        self._lang = None
        self._nlp = None
        self._hyphen = None
        self._input_file = None
        self._requested_words = None
        self._paragraphs_chunk = 1000
        self._paragraphs = 0
        self._min_paragraph_length = float('inf')
        self._max_paragraph_length = 0
        self._sentences = 0
        self._min_sentence_length = float('inf')
        self._max_sentence_length = 0
        self._words = 0
        self._words_stats = False
        self._min_word_length = float('inf')
        self._max_word_length = 0
        self._letters = 0
        self._punctuation = 0
        self._syllables = 0
        self._syllabize = False


    def process_file(self, file_path, max_word_count):
        def count_sentences(text):
            doc = self._nlp(text)
            return len(list(doc.sents))


        def count_syllables(word):
            return len(self._hyphen.inserted(word).split("-"))

        # for word in words:
        #     syllables_count += self.count_syllables(word)
        #     letter_count += sum(1 for letter in word if letter.isalpha())


        def count_words(text: str) -> tuple[int, int]:
            """
            Count the number of words in a given text.

            Args:
                text (str): The input text to count the words from.

            Returns:
                tuple[int, int]: The number of words in the input text and the number of syllables if `_syllabize` is True.
            """
            word_pattern = r'\w+'
            words = re.findall(word_pattern, text, re.UNICODE)
            syllables_count = 0
            if self._syllabize:
                syllables_count = sum(count_syllables(w) for w in words)

            return len(words), syllables_count


        word_count = 0
        syllables_count = 0
        chunk_count = 0
        chunk = ""
        num_paragraphs = 0
        num_sentences = 0
        num_letters = 0

        print()
        with yaspin().white.bold.shark.on_blue as spinner:
            spinner.text = "Processing file..."
            with open(file_path, 'r', encoding='utf-8') as file:
                for line in file:
                    if line:
                        num_paragraphs += 1
                        chunk += line + "\n\n"
                        chunk_count += 1
                        num_words, num_syllables = count_words(line)
                        word_count += num_words
                        syllables_count += num_syllables
                        num_letters += count_letters(line)
                        if word_count >= max_word_count:
                            break

                        if chunk_count >= self._paragraphs_chunk:

                            num_sentences += count_sentences(chunk)


                            chunk = ""
                            chunk_count = 0

                if chunk.strip():
                    num_sentences += count_sentences(chunk)

            self._words = word_count
            self._syllables = syllables_count
            self._paragraphs = num_paragraphs
            self._sentences = num_sentences
            self._letters = num_letters

    @property
    def lang(self):
        return self._lang

    @lang.setter
    def lang(self, language):
        self._lang = language
        if language == "en":
            self._nlp = spacy.load("en_core_web_sm")
            self._hyphen = pyphen.Pyphen(lang='en_US')
        elif language == 'es':
            self._nlp = spacy.load("es_core_news_sm")
            self._hyphen = pyphen.Pyphen(lang='es_ES')
        elif language == 'it':
            self._nlp = spacy.load("it_core_news_sm")
            self._hyphen = pyphen.Pyphen(lang='it_IT')
        else:
            raise ValueError("Unsupported language")

    @property
    def nlp(self):
        return self._nlp

    @nlp.setter
    def nlp(self, value):
        self._nlp = value

    @property
    def hyphen(self):
        return self._hyphen

    @hyphen.setter
    def hyphen(self, value):
        self._hyphen = value

    @property
    def input_file(self):
        return self._input_file

    @input_file.setter
    def input_file(self, file_info):
        if isinstance(file_info, tuple) and len(file_info) == 2:
            filename, num_words = file_info
            success, message = diy_file_validate(filename)
            if not success:
                sys.exit(f"File {filename}: {message}")
            self._input_file = filename
            self._requested_words = num_words
            self.process_file(filename, num_words)
        else:
            raise ValueError("Input must be a tuple with (filename, num_words)")

    @property
    def requested_words(self):
        return self._requested_words

    @requested_words.setter
    def requested_words(self, value):
        self._requested_words = value

    @property
    def paragraphs_chunk(self):
        return self._paragraphs_chunk

    @paragraphs_chunk.setter
    def paragraphs_chunk(self, value):
        self._paragraphs_chunk = value

    @property
    def paragraphs(self):
        return self._paragraphs

    @paragraphs.setter
    def paragraphs(self, value):
        self._paragraphs = value

    @property
    def min_paragraph_length(self):
        return self._min_paragraph_length

    @min_paragraph_length.setter
    def min_paragraph_length(self, value):
        self._min_paragraph_length = value

    @property
    def max_paragraph_length(self):
        return self._max_paragraph_length

    @max_paragraph_length.setter
    def max_paragraph_length(self, value):
        self._max_paragraph_length = value

    @property
    def sentences(self):
        return self._sentences

    @sentences.setter
    def sentences(self, value):
        self._sentences = value

    @property
    def min_sentence_length(self):
        return self._min_sentence_length

    @min_sentence_length.setter
    def min_sentence_length(self, value):
        self._min_sentence_length = value

    @property
    def max_sentence_length(self):
        return self._max_sentence_length

    @max_sentence_length.setter
    def max_sentence_length(self, value):
        self._max_sentence_length = value

    @property
    def words(self):
        return self._words

    @words.setter
    def words(self, value):
        self._words = value

    @property
    def syllables(self):
        return self._syllables

    @syllables.setter
    def syllables(self, value):
        self._syllables = value

    @property
    def syllabize(self):
        return self._syllabize

    @syllabize.setter
    def syllabize(self, value):
        self._syllabize = value


    @property
    def words_stats(self):
        return self._words_stats

    @words_stats.setter
    def words_stats(self, value):
        self._words_stats = value

    @property
    def min_word_length(self):
        return self._min_word_length

    @min_word_length.setter
    def min_word_length(self, value):
        self._min_word_length = value

    @property
    def max_word_length(self):
        return self._max_word_length

    @max_word_length.setter
    def max_word_length(self, value):
        self._max_word_length = value

    @property
    def letters(self):
        return self._letters

    @letters.setter
    def letters(self, value):
        self._letters = value

    @property
    def punctuation(self):
        return self._punctuation

    @punctuation.setter
    def punctuation(self, value):
        self._punctuation = value
################################################################
tp = TextProcessor()
tp.lang = "es"

t = time.perf_counter()
tp.syllabize = True
tp.input_file = (JULIA, 200000)


print()
print(f"[dark_orange]{tp.requested_words:>{10},} [yellow1]requested words")

print(f"[dark_orange]{tp.paragraphs:>{10},} [yellow1]paragraphs")
print(f"[dark_orange]{tp.sentences:>{10},} [yellow1]sentences")

print(f"[dark_orange]{tp.words:>{10},} [yellow1]counted words")
print(f"[dark_orange]{tp.syllables:>{10},} [yellow1]syllables")

print(f"[dark_orange]{tp.letters:>{10},} [yellow1]letters")

print()
elapsed_time = time.perf_counter() -t
print(print(f"[yellow1]Elapsed time: [dark_orange]{elapsed_time:.2f} [yellow1]seconds"))
