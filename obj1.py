
import csv
import glob
import os
import re
import subprocess
import sys
import tempfile
import time
from collections import namedtuple

import pyphen
import spacy
from rich import print
from yaspin import yaspin

from textstat.textstat import textstat
from utils.file_utils import diy_file_validate
from utils.txt_utils import count_letters


# TODO: use glob to look for files in a given name file

Book = namedtuple('Book', ['title', 'file_path'])


class TextProcessor:
    def __init__(self):
        """
        Initializes the object with default values for various attributes.
        """
        self._lang = None
        self._nlp = None
        self._hyphen = None
        self._syllabize = False
        self._detailed = False
        self._cut_percent = 5

        self._csv_headers = ['title', 'f_huerta', 'fhd', 'g_polini', 'gpd', 's_pazos', 'spd', 'crawford', 'crd', 'paragraphs', 'sentences', 'words', 'letters', 'punctuation', 'syllables']

        self._csv_list = []

        self._csv_data = {}
        self._input = None
        self._input_files = []
        self._files2process = []
        self._output_csv = None
        self._csv_output_file = None
        self._output_screen = True
        self._requested_words = float("inf")
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
        self._stop_words = 0

        self._words_stats = False
        self._word_min_len = float('inf')
        self._word_max_len = 0
        self._letters = 0
        self._syllables = 0

        self._text_save = False
        self._text = None

        self._f_huerta = 0
        self._g_polini = 0
        self._s_pazos = 0
        self._crawford = 0

    def reset_properties_to_defaults(self):
        """
        Reset properties to their default values.

        This function resets all the properties of the class to their default values. This allows for batch runs, where the properties can be reset before each run.

        Parameters:
            None

        Returns:
            None
        """
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
        self._stop_words = 0
        self._words_stats = False
        self._word_min_len = float('inf')
        self._word_max_len = 0
        self._letters = 0
        self._syllables = 0

        # self._text_save = False
        self._text = None
        self._f_huerta = 0
        self._g_polini = 0
        self._s_pazos = 0
        self._crawford = 0

    def write_csv(self):
        # Open the CSV file for writing
        print(f"{self._csv_output_file=}")
        with open(self._csv_output_file, mode="w", newline='', encoding='utf-8') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=self._csv_headers)
            writer.writeheader()
            for book in self._csv_list:
                writer.writerow(book)


    def process_file(self, book):
        self._csv_data = {}
        self._csv_data["title"] = book.title
        book_path = book.file_path
        book_name = book.title

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

        # sys.stdout.flush()
        with yaspin().white.bold.shark.on_blue as spinner:

            spinner.text = f"Processing file {book_name}..."
            self._csv_data = {}

            with open(book_path, 'r', encoding='utf-8') as file:
                self._text = ""
                for line in file:
                    if line.strip():
                        num_paragraphs += 1

                        chunk += line + "\n\n"
                        chunk_count += 1
                        num_words, num_syllables = count_words(line)
                        word_count += num_words
                        # TODO: count punctuation
                        self._paragraph_len_list.append(num_words)
                        # self._paragrah_min_len = min(self._paragrah_min_len, num_words)
                        # self._paragraph_max_len = max(self._paragraph_max_len, num_words)

                        syllables_count += num_syllables
                        num_letters += count_letters(line)
                        if word_count >= self._requested_words:
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
            self._csv_data['title'] = book_name
            self._csv_data['paragraphs'] = num_paragraphs
            self._csv_data['sentences'] = num_sentences
            self._csv_data['words'] = word_count
            self._csv_data['letters'] = num_letters
            self._csv_data['syllables'] = syllables_count
            self._csv_data['f_huerta'] = self.fernandez_huerta
            self._csv_data['fhd'] = self.fernandes_huerta_meaning
            self._csv_data['g_polini'] = self.gutierrez_polini
            self._csv_data['gpd'] = self.gutierrez_polini_meaning
            self._csv_data['s_pazos'] = self.szigriszt_pazos
            self._csv_data['spd'] = self.szigriszt_pazos_meaning
            self._csv_data['crawford'] = self.crawford
            self._csv_data['crd'] = self.crawford_meaning

            self._csv_list.append(self._csv_data)


            self._paragraph_avg_len = sum(self._paragraph_len_list) / len(self._paragraph_len_list)

            #TODO:fix this
            if self._cut_percent:
                minimum_paragraphs = (self._cut_percent * 2) + 1

                if len(self._paragraph_len_list) >= minimum_paragraphs:
                    self._paragraphs_dropped = (len(self._paragraph_len_list) *
                self._cut_percent // 100)

                    filtered_lengths = self._paragraph_len_list[self._paragraphs_dropped:-self._paragraphs_dropped]

                    self._paragraph_min_len_w = self._paragraph_len_list[self._paragraphs_dropped]
                    self._paragraph_max_len_w = self._paragraph_len_list[-self._paragraphs_dropped]
            sys.stdout.flush()



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

        def is_ebook(file_path: str) -> bool:
            # Get the file extension
            ebook_extensions = ['.azw3', '.docx', '.epub', '.fb2', '.html', '.htmlz', '.lit', '.lrf', '.mobi', '.oeb', '.pdb', '.pdf', '.pml', '.rb', '.rtf', '.snb', '.tcr']
            file_extension = os.path.splitext(file_path)[1]

            if file_extension:
                return file_extension in ebook_extensions or file_extension == '.txtz'

        def could_be_file(text: str) -> bool:
            return has_extensions(text) or has_file_path(text)

        def base_name(filename: str) -> str:
            if not filename:
                raise ValueError("Filename cannot be empty")

            base_filename = os.path.basename(filename)
            root, _ = os.path.splitext(base_filename)

            return root

        def is_list_of_files(filename: str) -> bool:
            """
            The function `is_list_of_files` checks if a given file contains multiple file
            names.

            :param filename: The `filename` parameter is a string that represents the name
            or path of a file
            :type filename: str
            :return: a boolean value. It returns True if there are more than one file found
            in the given filename, and False otherwise.
            """
            if is_ebook(filename):
                return False

            line_counter = 0
            files_found = 0

            with open(filename, 'r', encoding='utf-8') as file:
                for line in file:
                    if line := line.strip():
                        line_counter += 1
                        if (could_be_file(line) or is_ebook(line)):
                            files_found += 1
                        if line_counter >= 10:
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
                            files.append(Book(parts[0], parts[1]))
                        else:
                            files.append(Book(base_name(line), line))
                return files

        t = time.perf_counter()
        work_list = []
        if filename:
            if not isinstance(filename, list):
                filename = [filename]

            for file in filename:
                if is_list_of_files(file):
                    work_list.extend(extract_files(file))
                else:
                    work_list.append([base_name(file), file])

            print(f"{filename=}")
            print(f"{work_list=}")
            # exit()
        temp_dir = tempfile.TemporaryDirectory()

        print(work_list)
        for book in work_list:
            temp_text_file = f"{temp_dir.name}/temp.txt"
            _ = subprocess.run(["ebook-convert", book.file_path, temp_text_file], stdout=subprocess.DEVNULL,stderr=subprocess.STDOUT, check=False)
            temp_book = Book(book.title, temp_text_file)
            self.process_file(temp_book)
        temp_dir.cleanup()
        self.write_csv()

        elapsed_time = time.perf_counter() -t
        print(print(f"[yellow1]Elapsed time: [dark_orange]{elapsed_time:.2f} [yellow1]seconds"))
        exit(0)

    ############################

    @property
    def output_file(self):
        return self._csv_output_file

    @output_file.setter
    def output_file(self,val):
        _, ext = os.path.splitext(val)

        # If it has an extension, keep it, otherwise add ".csv"
        if not ext:
            val += ".csv"

        self._csv_output_file = val

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
    def max_word_length(self) -> int:
        """
        Get the maximum length of a word.

        Returns:
            int: The maximum length of a word.
        """
        return self._word_max_len

    @max_word_length.setter
    def max_word_length(self, value):
        """
        Setter method for the max_word_length attribute.

        Parameters:
            value (int): The new value for the max_word_length attribute.

        Returns:
            None
        """
        self._word_max_len = value

    @property
    def paragraph_len_list(self):
        """
        Get the length of the paragraph list.

        Returns:
            int: The length of the paragraph list.
        """
        return self._paragraph_len_list

    @property
    def paragraphs_dropped(self):
        """
        Returns the value of the private variable _paragraphs_dropped.

        :return: The value of the private variable _paragraphs_dropped.
        """
        return self._paragraphs_dropped

    @property
    def letters(self):
        """
        Get the letters property.

        Returns:
            The letters property.
        """
        return self._letters

    @letters.setter
    def letters(self, value):
        """
        Setter method for the 'letters' attribute.

        Parameters:
            value (any): The new value for the 'letters' attribute.

        Returns:
            None
        """
        self._letters = value


    @property
    def fernandez_huerta(self) -> float:
        """
        Calculates the Fernandez-Huerta readability score.

        Args:
            self: The current instance of the class.

        Returns:
            float: The Fernandez-Huerta readability score.
        """
        try:
            p = self._syllables / self._words
            f = self._words / self._sentences
            self._f_huerta = round(206.84 - (60 * p) - (1.02 * f), 2)
        except ZeroDivisionError:
            self._f_huerta = 0.0
        return self._f_huerta

    @property
    def fernandes_huerta_meaning(self) -> str:
        """
        Returns the Fernandes-Huerta meaning based on the value of self._f_huerta.

        Args:
            self: The instance of the class.

        Returns:
            str: The meaning of the Fernandes-Huerta value.
        """
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
            if min_val <= self._f_huerta < max_val:
                return label
        return "No label found"

    @property
    def gutierrez_polini(self) -> float:
        """
        Calculates the Gutierrez-Polini readability score for the given text.

        Returns:
            float: The Gutierrez-Polini readability score.
        """
        letters = self._letters
        words = self.words
        sentences = self._sentences

        try:
            self._g_polini = round(
                95.2 - 9.7 * (letters / words) - 0.35 * (words / sentences), 2
            )
        except ZeroDivisionError:
            self._g_polini = 0.0

        return self._g_polini

    @property
    def gutierrez_polini_meaning(self) -> str:
        """
        Calculates the meaning of the Gutierrez Polini score.

        Returns:
            str: The meaning of the Gutierrez Polini score based on the value of self._g_polini.
        """
        ranges = [
            (-float('inf'), 0, "no calculado"),
            (0, 33.33, "muy difícil"),
            (33.34, 66.66, "normal"),
            (66.67, float('inf'), "muy fácil")
        ]

        for min_val, max_val, label in ranges:
            if min_val <= self._g_polini < max_val:
                return label

        return "No label found"


    @property
    def szigriszt_pazos(self) -> float:
        """
        Calculates the Szigriszt-Pazos readability score.

        Returns:
            float: The Szigriszt-Pazos readability score.
        """
        try:
            syllables_per_word = self._syllables / self._words
            words_per_sentence = self._words / self._sentences
            self._s_pazos = round(206.84 - 62.3 * syllables_per_word - words_per_sentence, 2)
        except ZeroDivisionError:
            self._s_pazos = 0.0
        return self._s_pazos


    @property
    def szigriszt_pazos_meaning(self) -> str:
        """
        Calculates the meaning of the Szigriszt Pazos score.

        Returns:
            str: The meaning of the Szigriszt Pazos score.
        """
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
            if min_val <= self._s_pazos < max_val:
                return label

        return "No label found"

    @property
    def crawford(self) -> float:
        """
        Calculates the Crawford score for the text.

        Args:
            self (object): The object instance.

        Returns:
            float: The calculated Crawford score, rounded to 2 decimal places.
        """
        try:
            sentences_per_words = 100 * (self._sentences / self._words)
            syllables_per_words = 100 * (self._syllables / self._words)
        except ZeroDivisionError:
            return 0.0
        return round(
            -0.205 * sentences_per_words
            + 0.049 * syllables_per_words - 3.407,
            2
        )


    @property
    def crawford_meaning(self) -> str:
        """
        Get the crawford meaning.

        :return: The crawford meaning.
        :rtype: str
        """
        return "años de escolarización"

################################################################
BOOkS_PATH = "/home/silvio/miniconda3/envs/classy3/prg/books/"

SOLEDAD = BOOkS_PATH + "Cien Anos De Soledad.txt"
CATEDRAL = BOOkS_PATH + "Conversación en La Catedral.txt"
JULIA = BOOkS_PATH + "La tia Julia.txt"
JULIA_TEST_1 = BOOkS_PATH + "julia_test_1.txt"
SUPREMO = BOOkS_PATH + "Yo el Supremo - Augusto Roa Bastos.txt"
INFANTIL = BOOkS_PATH + "infantil"
BOOKS_LIST = "/home/silvio/miniconda3/envs/classy3/prg/books/lista1"
################################################################


tp = TextProcessor()
tp.lang = "es"

t = time.perf_counter()
# tp.save_text = False
tp.syllabize = True
tp.cut_percent = 5
# tp.input = (SOLEDAD, 30000)
# print(SOLEDAD)
tp.output_file = "/home/silvio/miniconda3/envs/classy3/prg/books/test.csv"
tp.input_file = INFANTIL

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
