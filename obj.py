#!/usr/bin/env python3


import linecache
from symspellpy import SymSpell, Verbosity
from rich import print
import inspect
import os
from collections import Counter
import re
import textstat
from icecream import ic
from utils.file_utils import file_validate, diy_file_validate

CONFIG_DIR = '/home/silvio/miniconda3/envs/classy3/prg/config/'
STOPWORD_ES = 'stopwords_es.txt'
STOPWORD_RED = 'stopwords_reddit.txt'
DICTIONARY = 'new_dic.txt'

dictionary = os.path.join(CONFIG_DIR, DICTIONARY)
stopwords_files = [os.path.join(CONFIG_DIR, STOPWORD_ES),
                  os.path.join(CONFIG_DIR,STOPWORD_RED)]


class Stopwords:
    def __init__(self):
        self._stopwords = Counter()
        self._files = []
        _stopwords_set = set()
        
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
                    word = line.strip()
                    if word:
                        self._stopwords.update({word.lower(): 1})

        self._stopwords_set = set(self._stopwords.keys())
        
    @property
    def files(self):
        return self._files

    @files.setter
    def files(self, files_list):
        self._files = files_list
        self.load_stopwords()

    @property
    def stopwords(self):
        return self._stopwords

    @property
    def stopwords_set(self):
        return self._stopwords_set    

print("Hello")
sw = Stopwords()
sw.files = stopwords_files
# print(vars(sw))
print(sw.stopwords_set)
