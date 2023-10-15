import linecache
from rich import print
import sys
from utils.file_utils import diy_file_validate

class Dictionaries:

    def __init__(self, filename=None, steps=10):
        """
        Initializes the instance with the given filename and steps.

        Parameters:
            filename (str): The name of the file to be processed.
            steps (int): The number of steps to be used for splitting the dictionary.

        Returns:
            None

        Raises:
            None

        Description:
            - Initializes the instance with the given filename and steps.
            - Sets the file attribute to the provided filename.
            - Sets the steps attribute to the provided number of steps.
            - Opens the file and counts the number of words to set the num_words attribute.
            - Calls the divide_dictionary() method to divide the dictionary into logical parts.
        """
        self._file = filename
        self._steps = steps
        self._block_size = 0
        self._auxiliary_dictionaries = [] # tuples(filename, position)
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
        """
        Divide the dictionary into equal logical parts and calculate the thresholds (frequency) for each step.

        This function divides the dictionary into equal steps based on the given block size and number of words. Any extra words are distributed among the steps. It then calculates the threshold for each step by calling the `get_line_frequency` method.

        Parameters:
            self (object): The current instance of the class.

        Returns:
            None
        """
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
            sys.exit(f"File {filename}: {message}")

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
