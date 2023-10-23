import nltk
import linecache
from symspellpy import SymSpell, Verbosity
from rich import print
import inspect
import os
from collections import Counter
import re
import string
from utils.file_utils import file_validate, diy_file_validate

class Stopwords:
    def __init__(self):
        self._lang = None
        self._use_nltk = True
        self._stopwords = set()
        self._files = []
        self._disabled = False

    def load_stopwords(self, files, lang="spanish", nltk=True):
        if files:
            self._files = files
        self._lang = lang
        self._use_nltk= nltk

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

        def validate_language(val):
            if val := val.strip().lower():
                if val in ["es", "es_ES", "español", "spanish"]:
                    self._lang = "spanish"
                elif val in ["en", "en_US", "english"]:
                    self._lang = "english"
                elif val in ["it", "italiano", "it_IT", "italian"]:
                    self._lang = "italian"
                else:
                    print("Language not  set")
                    exit(0)
            return True

        if not validate_files_argument(files):
            self._disabled = True

        if not validate_language(lang):
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

            self._stopwords = set(new_stopwords)
            # TODO: reenable ntlk dictionary
            # if self._use_nltk:
            #     self._stopwords = self._stopwords | set(stopwords.words(self._lang))

    @property
    def language(self):
        return self._lang

    @property
    def files(self) -> list:
        return self._files

    @property
    def stopwords(self):
        return self._stopwords

    def count_stopwords(self, text):
        # text = re.sub(f"[{string.punctuation}\n\r¡¿]", "", text).lower()

        # Tokenize the text into words as a set
        # If it doesn't work see: https://stackoverflow.com/a/74060135/18511264
        # words = set(nltk.word_tokenize(text, self._lang
        if text := text.strip().lower():
            text = re.sub(f"[{string.punctuation}\n\r¡¿]", "", text)

        print(text)
        words = nltk.word_tokenize(text, self._lang)
        len_words = len(words)
        print(f"{len_words=}")
        # Remove stopwords using set difference
        filtered_words = set(words) - self._stopwords
        len_filtered  = len(filtered_words)
        print(f"{len(words)=}")
        print(f"{len_filtered=}")

        # Reconstruct the text
        processed_text = ' '.join(filtered_words)
        print(processed_text)

        return len(words) - len(processed_text)


CONFIG_DIR = '/home/silvio/miniconda3/envs/classy3/prg/config/'
STOPWORD_ES = 'stopwords_es.txt'
STOPWORD_RED = 'stopwords_reddit.txt'
DICTIONARY = 'new_dic.txt'

dictionary = os.path.join(CONFIG_DIR, DICTIONARY)
stopwords_files = [os.path.join(CONFIG_DIR, STOPWORD_ES),
                  os.path.join(CONFIG_DIR,STOPWORD_RED)]
lang = "es"
# print(stopwords_files)
# print(dictionary)

sw = Stopwords()
sw.load_stopwords(stopwords_files, lang=(lang), nltk=True)

txt = """
EN ESE TIEMPO REMOTO, yo era muy joven y vivía con mis abuelos en una quinta de paredes  blancas de la calle Ocharán, en Miraflores. Estudiaba en San Marcos, Derecho, creo,  resignado a ganarme más tarde la vida con una profesión liberal, aunque, en el fondo, me hubiera gustado más llegar a ser un escritor. Tenía un trabajo de título pomposo, sueldo modesto, apropiaciones ilícitas y horario elástico: director de Informaciones de  Radio Panamericana. Consistía en recortar las noticias interesantes que aparecían en los
diarios y maquillarlas un poco para que se leyeran en los boletines. La redacción a mis.
"""

sw.count_stopwords(txt)