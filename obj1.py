#################################### ORIGINAL
#!/usr/bin/env python3


import sys
import os
import re
import glob
import spacy
import pyphen
import time
import csv
from rich import print
from yaspin import yaspin
from textstat.textstat import textstat
from utils.txt_utils import count_letters
from utils.file_utils import diy_file_validate

textstat.set_lang("es_ES")

# def process_books(input_file):
#     categorized_entries = []
#     invalid_entries = []

#     if os.path.isfile(input_file):
#         # Case 1: Input is a file path
#         book_name = os.path.basename(input_file)
#         categorized_entries.append((book_name, input_file))
#     else:
#         # Case 2: Input is a text containing paths or a list of file paths
#         items = input.strip().split('\n')

#         for item in items:
#             book_path = item.strip()
#             book_name = os.path.basename(book_path)

#             if os.path.isfile(book_path):
#                 categorized_entries.append((book_name, book_path))
#             else:
#                 invalid_entries.append(book_path)

#     if not categorized_entries:
#         # Case 3: No paths found, process the input as a book
#         categorized_entries.append(("Input Book", input))

#     return categorized_entries, invalid_entries


class TextProcessor:
    def __init__(self):
        self._lang = None
        self._nlp = None
        self._hyphen = None
        self._syllabize = False
        self._detailed = False
        self._cut_percent  = 5

        self._input = None
        self._input_files = []
        self._files2process = []
        self._output_csv = None
        self._output_screen = True
        self._requested_words = None
        self._paragraphs_chunk = 1000
        self._paragraphs = 0
        self._paragraphs_dropped = 0
        self._paragraph_avg_len = 0
        self._paragraph_min_len = float('inf')
        self._paragraph_max_len = 0
        self._paragraph_min_len_w = float('inf')
        self._paragraph_max_len_w = 0
        self._paragraph_len_list = []
        self._sentences = 0
        self._sentence_min_len = float('inf')
        self._sentence_max_len = 0
        self._words = 0
        self._words_stats = False
        self._word_min_len = float('inf')
        self._word_max_len = 0
        self._letters = 0
        self._punctuation = 0
        self._syllables = 0

        self._text_save = False
        self._text = None

        self._f_huerta = 0
        self._g_polini = 0
        self._s_pazos = 0

    def reset_properties_to_defaults(self):
        # Reset properties to their default values
        # This allows to have batch runs
        self._input = None
        self._input_files = []
        self._files2process = []
        self._output_csv = None
        self._output_screen = True
        self._paragraphs_chunk = 1000
        self._paragraphs = 0
        self._paragraphs_dropped = 0
        self._paragraph_avg_len = 0
        self._paragraph_min_len = float('inf')
        self._paragraph_max_len = 0
        self._paragraph_min_len_w = float('inf')
        self._paragraph_max_len_w = 0
        self._paragraph_len_list = []
        self._sentences = 0
        self._sentence_min_len = float('inf')
        self._sentence_max_len = 0
        self._words = 0
        self._words_stats = False
        self._word_min_len = float('inf')
        self._word_max_len = 0
        self._letters = 0
        self._punctuation = 0
        self._syllables = 0

        # self._text_save = False
        self._text = None
        self._f_huerta = 0
        self._g_polini = 0
        self._s_pazos = 0


    def write_csv(self):


        # Create a list of book data where each inner list represents a row.
        book_data = [
            ["Book 1 Title", 12, 34, 56, ...],  # Data for the first book
            ["Book 2 Title", 23, 45, 67, ...],  # Data for the second book
            ["Book 3 Title", 34, 56, 78, ...],  # Data for the third book
            # Add more books as needed
        ]

        # Open the CSV file for writing
        with open('books.csv', 'w', newline='') as file:
            writer = csv.writer(file)

            # Write all the book data at once
            writer.writerows(book_data)

        # Close the CSV file
        file.close()

    def process_file(self, file_path, max_word_count):
        def count_sentences(text):
            doc = self._nlp(text)
            return len(list(doc.sents))


        def count_syllables(word):
            return len(self._hyphen.inserted(word).split("-"))


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
                for word in words:
                    syllables_count += count_syllables(word)

            return len(words), syllables_count


        word_count = 0
        syllables_count = 0
        chunk_count = 0
        chunk = ""
        num_paragraphs = 0
        num_sentences = 0
        num_letters = 0

        with yaspin().white.bold.shark.on_blue as spinner:
            spinner.text = "Processing file..."
            with open(file_path, 'r', encoding='utf-8') as file:
                self._text = ""
                for line in file:
                    if line.strip():
                        num_paragraphs += 1

                        chunk += line + "\n\n"
                        chunk_count += 1
                        num_words, num_syllables = count_words(line)
                        word_count += num_words

                        self._paragraph_len_list.append(num_words)
                        # self._paragrah_min_len = min(self._paragrah_min_len, num_words)
                        # self._paragraph_max_len = max(self._paragraph_max_len, num_words)

                        syllables_count += num_syllables
                        num_letters += count_letters(line)
                        if word_count >= max_word_count:
                            break

                        if chunk_count >= self._paragraphs_chunk:
                            num_sentences += count_sentences(chunk)
                            if self._text_save:
                                self._text += chunk
                            chunk = ""
                            chunk_count = 0

                if chunk.strip():
                    if self._text_save:
                        self._text += chunk
                    num_sentences += count_sentences(chunk)

            self._paragraph_len_list = sorted(self._paragraph_len_list)
            self._paragraph_min_len = self._paragraph_len_list[0]
            self._paragraph_max_len = self._paragraph_len_list[-1]

            self._words = word_count
            self._syllables = syllables_count
            self._paragraphs = num_paragraphs
            self._sentences = num_sentences
            self._letters = num_letters


            self._paragraph_avg_len = sum(self._paragraph_len_list) / len(self._paragraph_len_list)

            #TODO:fix this
            if self._cut_percent:
                minimum_paragraphs = (self._cut_percent * 2) + 1

                if len(self._paragraph_len_list) >= minimum_paragraphs:
                    self._paragraphs_dropped = (len(self._paragraph_len_list) *
                self._cut_percent // 100)

                    print(f"{self._paragraphs_dropped * 2=}")
                    filtered_lengths = self._paragraph_len_list[self._paragraphs_dropped:-self._paragraphs_dropped]

                    self._paragraph_min_len_w = self._paragraph_len_list[self._paragraphs_dropped]
                    self._paragraph_max_len_w = self._paragraph_len_list[-self._paragraphs_dropped]


                    # self._paragraph_min_len_w = filtered_lengths[0]
                    # self._paragraph_max_len_w = filtered_lengths[-1]




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
        return self._input_files

    ############################
    @input_file.setter
    def input_file(self, filename: str):
        self._input_files = []
        self._files2process = []

        def has_extensions(text: str) -> bool:
            return bool(re.search(r'\.\w+', text))

        def has_file_path(text: str) -> bool:
            return bool(re.search(r'(\w:/|/|\w:\\)', text))

        def could_be_file(text: str) -> bool:
            return has_extensions(text) or has_file_path(text)

        def base_name(filename: str) -> str:
            if not filename:
                raise ValueError("Filename cannot be empty")

            base_filename = os.path.basename(filename)
            root, _ = os.path.splitext(base_filename)

            return root

        def is_list_of_files(filename: str) -> bool:
            line_counter = 0
            files_found = 0
            with open(filename, 'r', encoding='utf-8') as file:
                for line in file:
                    line_counter += 1
                    if line.strip() and could_be_file(line):
                        files_found += 1
                    if line_counter >= 10 or files_found >= 3:
                        break
            return files_found > 1

        def extract_files(file: str) -> list:
            files = []
            with open(file, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if is_list_of_files(line):
                        files.extend(extract_files(line))
                    elif line and could_be_file(line):
                        parts = line.split(",")
                        if len(parts) == 2:
                            files.append([[parts[0], parts[1]]])
                        else:
                            files.append([[base_name(line), line]])
            return files

        work_list = []
        if filename:
            if not isinstance(filename, list):
                filename = [filename]

            for file in filename:
                if is_list_of_files(file):
                    work_list.extend(extract_files(file))
                else:
                    work_list.append([base_name(file), file])

        # self._input_files.extend([[base_name(file), file] for file in work_list])

        # print(self._input_files)
        print(work_list)
        exit(0)

        # Validate the file
        success, message = diy_file_validate(filename)
        if not success:
            raise ValueError(f"File {filename}: {message}")

        # check if the file contains a list of files
        if is_list_of_files(filename):
            pass
        else:
            pass
    ############################


    @property
    def requested_words(self):
        return self._requested_words

    @requested_words.setter
    def requested_words(self, value):
        self._requested_words = value

    @property
    def cut_percent(self):
        return self._cut_percent

    @cut_percent.setter
    def cut_percent(self, value):
        self._cut_percent = value

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
    def paragraph_avg_len(self):
        return self._paragraph_avg_len

    @property
    def paragraph_min_len(self):
        return self._paragraph_min_len

    @property
    def paragraph_min_len_w(self):
        return self._paragraph_len_list[0]

    @property
    def paragraph_max_len(self):
        return self._paragraph_max_len

    @property
    def paragraph_max_len_w(self):
        return self._paragraph_max_len

    @property
    def sentences(self):
        return self._sentences

    @sentences.setter
    def sentences(self, value):
        self._sentences = value

    @property
    def min_sentence_length(self):
        return self._sentence_min_len

    @min_sentence_length.setter
    def min_sentence_length(self, value):
        self._sentence_min_len = value

    @property
    def max_sentence_length(self):
        return self._sentence_max_len

    @max_sentence_length.setter
    def max_sentence_length(self, value):
        self._sentence_max_len = value

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
        return self._word_min_len

    @min_word_length.setter
    def min_word_length(self, value):
        self._word_min_len = value

    @property
    def max_word_length(self):
        return self._word_max_len

    @max_word_length.setter
    def max_word_length(self, value):
        self._word_max_len = value

    @property
    def paragraph_len_list(self):
        return self._paragraph_len_list

    @property
    def paragraphs_dropped(self):
        return self._paragraphs_dropped

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

    @property
    def save_text(self):
        return self._text_save

    @save_text.setter
    def save_text(self, value):
        self._text_save = value

    @property
    def saved_text(self):
        return self._text

    @saved_text.setter
    def saved_text(self, value):
        self._text = value

    @property
    def fernandez_huerta(self):
        # https://legible.es/blog/lecturabilidad-fernandez-huerta/
        try:
            p = self._syllables / self._words
            f = self._words / self._sentences
            self._f_huerta = round(206.84 - (60 * p) - (1.02 * f),2)
        except ZeroDivisionError:
            self._f_huerta = 0.0
        return self._f_huerta
    @property
    def fernandes_huerta_meaning(self):
        ranges = [
            (-float('inf'), 0, "no calculado"),
            (0, 30, "muy difícil"),
            (30, 50, "difícil"),
            (50, 60, "bastante difícil"),
            (60, 70, "normal"),
            (70, 80, "bastante fácil"),
            (80, 90, "fácil"),
            (90, float('inf'), "muy fácil")
        ]
        for min_val, max_val, label in ranges:
            if min_val <=  self._f_huerta < max_val:
                return label
        return "No label found"

    @property
    def gutierrez_polini(self):
        letters = self._letters
        words = self.words
        sentences = self._sentences
        try:
            self._g_polini = round(
                95.2 - 9.7 * (letters / words)
                - 0.35 * (words / sentences)
            ,2)
        except ZeroDivisionError:
            self._g_polini = 0.0
        return self._g_polini

    @property
    def gutierrez_polini_meaning(self):
        ranges = [
            (-float('inf'), 0, "no calculado"),
            (0, 33.33, "muy difícil"),
            (33.34, 66.66, "normal"),
            (66.67, float('inf'), "muy fácil")
        ]
        for min_val, max_val, label in ranges:
            if min_val <=  self._g_polini < max_val:
                return label
        return "No label found"


    @property
    def szigriszt_pazos(self):
        try:
            self._s_pazos  = round((
                206.84 -
                62.3 * (self._syllables / self._words)
                - (self._words / self._sentences)
            ),2)
        except ZeroDivisionError:
            self._s_pazos = 0.0
        return self._s_pazos


    @property
    def szigriszt_pazos_meaning(self):
        ranges = [
            (-float('inf'), 0, "no calculado"),
            (0, 15, "muy difícil"),
            (15, 35, "árido"),
            (35, 50, "bastante difícil"),
            (50, 65, "normal"),
            (65, 75, "bastante fácil"),
            (75, 85, "fácil"),
            (85, float('inf'), "muy fácil")

        ]
        for min_val, max_val, label in ranges:
            if min_val <=  self._s_pazos < max_val:
                return label
        return "No label found"


    def crawford(self):
        pass
################################################################
BOOkS_PATH = "/home/silvio/miniconda3/envs/classy3/prg/books/"

SOLEDAD = BOOkS_PATH + "Cien Anos De Soledad.txt"
CATEDRAL = BOOkS_PATH + "Conversación en La Catedral.txt"
JULIA = BOOkS_PATH + "La tia Julia.txt"
JULIA_TEST_1 = BOOkS_PATH + "julia_test_1.txt"
SUPREMO = BOOkS_PATH + "Yo el Supremo - Augusto Roa Bastos.txt"
################################################################


tp = TextProcessor()
tp.lang = "es"

t = time.perf_counter()
tp.save_text = False
tp.syllabize = True
tp.cut_percent = 5
# tp.input = (SOLEDAD, 30000)
# print(SOLEDAD)
tp.input_file = [SOLEDAD, JULIA]
term_size = os.get_terminal_size()
print()
print('─' * term_size.columns)

print(f"[yellow1]{os.path.basename(tp.input_file)}")
print()
print("Metric data")
print("───────────")
print()
print(f"[dark_orange]{tp.requested_words:>{10},} [yellow1]requested words")

print(f"[dark_orange]{tp.paragraphs:>{10},} [yellow1]paragraphs")
print("    Real paragraphs")
print(f"     [dark_orange]{tp.paragraph_avg_len:>6.2f} [yellow1]avg. words")

print(f"     [dark_orange]{tp.paragraph_min_len:>10,}[yellow1] min. words")
print(f"     [dark_orange]{tp.paragraph_max_len:>{10},} [yellow1]max. words")

xmin = tp.paragraph_len_list[tp.paragraphs_dropped]
xmax = tp.paragraph_len_list[-tp.paragraphs_dropped]
print(f"{xmin=}")
print(f"{xmax=}")
print(f"    Weighted paragraphs ({tp.paragraphs_dropped}  paragraphs dropped)")
# print(f"     [dark_orange]{tp.paragraph_min_len_w:>{10},} [yellow1]min. words")
print(f"     [dark_orange]{xmin:>{10},} [yellow1]min. words")

# print(f"     [dark_orange]{tp.paragraph_max_len_w:>{10},} [yellow1]max. words")
print(f"     [dark_orange]{xmax:>{10},} [yellow1]min. words")

print(f"[dark_orange]{tp.paragraphs:>{10},} [yellow1]paragraphs")
print(f"[dark_orange]{tp.sentences:>{10},} [yellow1]sentences")

print(f"[dark_orange]{tp.words:>{10},} [yellow1]counted words")
print(f"[dark_orange]{tp.syllables:>{10},} [yellow1]syllables")

print(f"[dark_orange]{tp.letters:>{10},} [yellow1]letters")

print()

# Define a common format string
format_string = "[yellow1]{:<26} [dark_orange]{:>6.2f}"
format_index = "[yellow1]{:<26} [dark_orange]{:>6.2f} [cyan1]{}"

print(format_string.format("Sentences per paragraph:", tp.sentences / tp.paragraphs))
print(format_string.format("Words per sentence:", tp.words / tp.sentences))

print(format_string.format("Syllables per word:", tp.syllables / tp.words))

print(format_string.format("Letters per word:", tp.letters / tp.words))

print()
print(format_index.format("Fernandez_huerta:", tp.fernandez_huerta, tp.fernandes_huerta_meaning))

print(format_index.format("Gutierrez di Polini:", tp.gutierrez_polini, tp.gutierrez_polini_meaning))


print(format_index.format("Szigriszt_pazos:", tp.szigriszt_pazos, tp.szigriszt_pazos_meaning))

print('─' * term_size.columns)
elapsed_time = time.perf_counter() -t
print(print(f"[yellow1]Elapsed time: [dark_orange]{elapsed_time:.2f} [yellow1]seconds"))

# print(tp.paragraph_len_list)