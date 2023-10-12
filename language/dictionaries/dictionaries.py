import linecache
from rich import print

from utils.file_utils import diy_file_validate

class Dictionaries:

    def __init__(self, filename=None, steps=10):
        self._file = filename
        self._steps = steps
        self._block_size = 0
        self._auxiliary_dictionaries = []  # List of tuples (filename, position)
        # self._words = None
        self._num_words = 0
        self._steps_thresholds = []
        self._steps_lines = []

        self.set_dictionary(filename, steps)


    def get_line_frequency(self,line_num):
        """
            When splitting the dictionary for creating the steps,
            it reads a specific line of the dictionary and returns the
            frequency of the associated word.
            SymSpell returns the original word, or the correction, toghether
            with the frequency: this number will be usde to classify the difficulty
            of a word.
        """
        second_word_as_int = None
        line = linecache.getline(self._file, line_num)
        if line:
            words = line.split()
            if len(words) >= 2:
                second_word = words[1]
                print(f"[{second_word=}]")
                try:
                    second_word_as_int = int(second_word)
                except ValueError:
                    print("Second word is not an integer.")
            else:
                print("Line doesn't contain at least two words.")
        return second_word_as_int

    def divide_dictionary(self):
        self._block_size = self._num_words // self._steps
        extra_words = self._num_words % self._steps

        self._steps_lines = []
        self._steps_thresholds = []

        start = 0  # Starting line is always 1
        for i in range(self._steps):
            if i == 0:
                # First block, include the extra words
                end = start + self._block_size + extra_words
            else:
                end = start + self._block_size

            self._steps_lines.append(end)
            self._steps_thresholds.append(self.get_line_frequency(end))

            start = end


    def set_dictionary(self, filename=None, steps=10):
        success, message = diy_file_validate(filename)
        if success:
            self._file = filename
        else:
            exit(0, f"File {filename}: {message}")

        if not steps:
            print("Steps must be greater than 0. Assigned 10 as default.")
            steps = 10
        self._steps = steps

        with open(self._file, "rbU") as f:
            self._num_words = sum(1 for _ in f)

        self.divide_dictionary()

    @property
    def file(self):
        return self._file

    @property
    def steps(self):
        return self._steps

    @property
    def auxiliary_dictionaries(self):
        return self._auxiliary_dictionaries

    @auxiliary_dictionaries.setter
    def auxiliary_dictionaries(self, dictionaries_list):
        self._auxiliary_dictionaries = dictionaries_list

    @property
    def num_words(self):
        return self._num_words

    @property
    def steps_thresholds(self):
        return self._steps_thresholds

    @property
    def steps_lines(self):
        return self._steps_lines
