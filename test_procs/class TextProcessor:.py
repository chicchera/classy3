class TextProcessor:
    def __init__(self):
        self._lang = None
        self._nlp = None
        self._hyphen = None
        self._input_file = None
        self._requested_words = None
        self.paragraphs = []
        self.min_paragraph_length = float('inf')
        self.max_paragraph_length = 0
        self.sentences = []
        self.min_sentence_length = float('inf')
        self.max_sentence_length = 0
        self.words = []
        self.min_word_length = float('inf')
        self.max_word_length = 0
        self.letters = []
        self.punctuation = []

    @property
    def lang(self):
        return self._lang

    @lang.setter
    def lang(self, value):
        self._lang = value

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
    def input_file(self, value):
        self._input_file = value

    @property
    def requested_words(self):
        return self._requested_words

    @requested_words.setter
    def requested_words(self, value):
        self._requested_words = value

    def get_paragraphs(self):
        return self.paragraphs

    def set_paragraphs(self, value):
        self.paragraphs = value

    def get_min_paragraph_length(self):
        return self.min_paragraph_length

    def set_min_paragraph_length(self, value):
        self.min_paragraph_length = value

    def get_max_paragraph_length(self):
        return self.max_paragraph_length

    def set_max_paragraph_length(self, value):
        self.max_paragraph_length = value

    def get_sentences(self):
        return self.sentences

    def set_sentences(self, value):
        self.sentences = value

    def get_min_sentence_length(self):
        return self.min_sentence_length

    def set_min_sentence_length(self, value):
        self.min_sentence_length = value

    def get_max_sentence_length(self):
        return self.max_sentence_length

    def set_max_sentence_length(self, value):
        self.max_sentence_length = value

    def get_words(self):
        return self.words

    def set_words(self, value):
        self.words = value

    def get_min_word_length(self):
        return self.min_word_length

    def set_min_word_length(self, value):
        self.min_word_length = value

    def get_max_word_length(self):
        return self.max_word_length

    def set_max_word_length(self, value):
        self.max_word_length = value

    def get_letters(self):
        return self.letters

    def set_letters(self, value):
        self.letters = value

    def get_punctuation(self):
        return self.punctuation

    def set_punctuation(self, value):
        self.punctuation = value
