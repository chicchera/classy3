from rich import print
from collections import Counter

from utils.file_utils import diy_file_validate

class Stopwords:
    def __init__(self):
        self._stopwords = Counter()
        self._files = []

    def load_stopwords(self):
        if not self._files:
            return

        self._stopwords = Counter()

        for filename in self._files:
            success, message = diy_file_validate(filename)
            if not success:
                print(message)
                continue

            with open(filename, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                for line in lines:
                    if word := line.strip():
                        self._stopwords.update({word.lower(): 1})