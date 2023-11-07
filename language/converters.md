
import sys
import os
import re
import tempfile
import subprocess
import glob
import spacy
import pyphen
import time
import csv
from rich import print
from collections import namedtuple
from yaspin import yaspin
from textstat.textstat import textstat
from utils.txt_utils import count_letters
from utils.file_utils import diy_file_validate


Book = namedtuple('Book', ['title','file_path'])
class TextProcessor:
    def __init__(self):
        self._lang = None
        self._nlp = None
        self._hyphen = None
        self._syllabize = False
        self._detailed = False
        self._cut_percent  = 5
        self._csv_headers = ['title','f_huerta', 'g_polini', 's_pazos', 'crawford', 'paragrpahs', 'sentences', 'words', 'letters', 'punctuation', 'syllables']
        self.csv_data = {}

        self._input = None
        self._input_files = []
        self._files2process = []
        self._output_csv = None
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
        self._punctuation = 0
        self._syllables = 0

        self._text_save = False
        self._text = None

        self._f_huerta = 0
        self._g_polini = 0
        self._s_pazos = 0
        self._crawford = 0

    def process_file(self, book):
        book_path = book.path
        book_name = book.name

        def count_sentences(text):
            doc = self._nlp(text)
            return len(list(doc.sents))

        def count_syllables(word):
            return len(self._hyphen.inserted(word).split("-"))

        def count_words(text: str) -> tuple[int, int]:
             word_pattern = r'\w+'
            words = re.findall(word_pattern, text, re.UNICODE)

            syllables_count = 0
            if self._syllabize:
                for word in words:
                    syllables_count += count_syllables(word)

            return len(words), syllables_count


<<<<<<< HEAD
Certainly, using a predefined list of headers is a valid and practical shortcut, especially for ease of maintenance. This approach ensures that your CSV headers are consistent and easily modifiable. You can define the headers separately, and then if you update your data structure, you won't need to modify the headers each time.

Here's how you can use predefined headers in your code:

```python
import csv

# Define the file name for your CSV
csv_file_name = "book_data.csv"

# Define the headers for your CSV
headers = ["Title", "Paragraphs", "Sentences_Per_Paragraph", "Words_Per_Sentence"]

# Your book data with potentially varying keys
book_data = [
    {"Title": "Book 1", "Paragraphs": 10},
    {"Title": "Book 2", "Sentences_Per_Paragraph": 4},
]

# Open the CSV file in write mode and write the headers
with open(csv_file_name, mode="w", newline='') as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=headers)
    writer.writeheader()

    # Write the data for each book
    for book in book_data:
        writer.writerow(book)
```

With this approach, you have a clear separation between your headers and data, making it easier to update or maintain your program in the future. If you add or remove keys from your data dictionaries, you only need to update the `headers` list accordingly.
=======
        word_count = 0
        syllables_count = 0
        chunk_count = 0
        chunk = ""
        num_paragraphs = 0
        num_sentences = 0
        num_letters = 0

        with yaspin().white.bold.shark.on_blue as spinner:
            spinner.text = f"Processing file {book_name}..."

            with open(book_path, 'r', encoding='utf-8') as file:
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


            self._paragraph_avg_len = sum(self._paragraph_len_list) / len(self._paragraph_len_list)
>>>>>>> fcd9dd114ace658f762c7ea7b73fcfb33167b903

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

        def is_ebook(file_path: str) -> bool:
            # Get the file extension
            ebook_extensions = ['.azw3', '.docx', '.epub', '.fb2', '.html', '.htmlz', '.lit', '.lrf', '.mobi', '.oeb', '.pdb', '.pdf', '.pml', '.rb', '.rtf', '.snb', '.tcr']
            file_extension = os.path.splitext(file_path)[1]
            return file_extension in ebook_extensions or file_extension == '.txtz'
            # Check if the file extension is in the list of ebook extensions
            # if file_extension in ebook_extensions or file_extension == '.txtz':
            #     return True
            # elif file_extension.startswith('.txt') and file_extension != '.txtz':
            #     return False
            # else:
            #     return False

        def could_be_file(text: str) -> bool:
            return has_extensions(text) or has_file_path(text)

        def base_name(filename: str) -> str:
            if not filename:
                raise ValueError("Filename cannot be empty")

            base_filename = os.path.basename(filename)
            root, _ = os.path.splitext(base_filename)

            return root

        def is_list_of_files(filename: str) -> bool:

            if is_ebook(filename):
                return False

            line_counter = 0
            files_found = 0
            print(f"{filename=}")
            valid,_ = diy_file_validate(filename)
            if not valid:
                return False
            with open(filename, 'r', encoding='utf-8') as file:
                for line in file:
                    if line := line.strip():
                        line_counter += 1
                        if (line and could_be_file(line) or is_ebook(line)):
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
                            files.append(Book(parts[0], parts[1]))
                        else:
                            files.append(Book(base_name(line), line))
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

        temp_dir = tempfile.TemporaryDirectory()

        for book in work_list:
            temp_text_file = f"{temp_dir.name}/temp.txt"
            subprocess.run(["ebook-convert", book.file_path, temp_text_file])
            Book = Book(book.title, temp_text_file)
            self.process_file(book)


        temp_dir.cleanup()

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

    @property
    def crawford(self):
        try:
            sentences_per_words = 100 * (self._sentences / self._words)
            syllables_per_words = 100 * (self._syllables / self._words)
        except ZeroDivisionError:
            return 0.0
        return (round(
            -0.205 * sentences_per_words
            + 0.049 * syllables_per_words - 3.407
            ),2)

    @property
    def crawford_meaning(self):
        return "años de escolarización"