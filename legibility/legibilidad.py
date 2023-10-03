# Legibilidad 2 (beta)
# Averigua la legibilidad de un texto
# Spanish readability calculations
# © 2016 Alejandro Muñoz Fernández

#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#any later version.

#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.

#You should have received a copy of the GNU General Public License
#along with this program.  If not, see <http://www.gnu.org/licenses/>.




import re
import statistics
from collections import defaultdict
from legibility.nal import to_word
from legibility.separasilabas import silabizer


def is_non_empty_string(parameter):
    """
    Check if a parameter is a non-empty string, considering spaces, tabs, and newline characters as empty.

    Args:
    parameter (any): The parameter to check.

    Returns:
    bool: True if the parameter is a non-empty string, False otherwise.
    """
    if not isinstance(parameter, str):
        return False  # Not a string
    return not parameter.strip() == ''  # Check if the string is empty after trimming

def count_letters(text):
    '''
    Text letter count
    '''
    if is_non_empty_string(text):
        return sum(1 for char in text if char.isalpha())
    return 0

def letter_dict(text):
    text = text.lower()
    replacements = {'á': 'a','é': 'e','í': 'i','ó': 'o','ú': 'u','ü': 'u'}
    for i, j in replacements.items():
        text = text.replace(i, j)
    letterdict = {}
    for letter in text:
        if letter.isalpha():
            letterdict[letter] = letterdict.get(letter, 0) + 1
    return letterdict



import re

def count_words(text):
    '''
    Text word count
    '''
    if is_non_empty_string(text):
        clean_text = re.sub(r'\d+', '', text)
        clean_text = re.sub(r'\W+', ' ', clean_text).strip()
        word_count = len(clean_text.split())
        return max(0, word_count)
    return 0


def textdict(wordlist):
    '''
    Dictionary of word counts
    '''
    wordlist = re.sub(r'\d+', '', wordlist)
    wordlist = re.sub(r'\W+', ' ', wordlist)
    wordlist = wordlist.strip().split()

    worddict = defaultdict(int)
    for word in wordlist:
        worddict[word.lower()] += 1

    return dict(worddict)




def count_sentences(text):
    '''
    Sentence count
    '''
    if is_non_empty_string(text):
        text = text.replace("\n", "")
        sentences = re.split('[.:;!?\)\()]', text)
        sentences = list(filter(None, sentences))
        return len(sentences) if sentences else 1


def count_paragraphs(text):
    '''
    Paragraph count
    '''
    if is_non_empty_string(text):
        text = re.sub('<[^>]*>', '', text)
        text = list(filter(None, text.split('\n')))
        if len(text) == 0:
            return 1
        else:
            return len(text)
    return 0


def numbers2words(text):
    '''
    Converts figures into words (e.g. 2 to two)
    '''
    digit_pattern = r'\d'
    if re.search(digit_pattern, text):
        new_text = []
        for word in text.split():
            if re.match(r"^[\-]?[1-9][0-9]*\.?[0-9]+$", word):
                if word.isdigit():
                    word = int(word)
                else:
                    word = float(word)
                word = to_word(word)
            new_text.append(word.lower())
        text = ' '.join(new_text)
    return text




def count_syllables(word):
    if is_non_empty_string(word):
        word = re.sub(r'\W+', '', word)
        syllables = silabizer()
        return len(syllables(word))
    return 0

def count_all_syllables(text):
    '''
    The whole text syllable count
    '''
    if is_non_empty_string(text):
        text = ''.join(filter(lambda x: not x.isdigit(), text))
        clean = re.compile('\W+')
        text = clean.sub(' ', text).strip()
        text = text.split()
        text = filter(None, text)
        total = 0
        for word in text:
            total += count_syllables(word)
        if total == 0:
            return 1
        else:
            return total
    return 0

def Pval(text):
    '''
    Syllables-per-word mean (P value)
    '''
    if is_non_empty_string(text):
        syllables = count_all_syllables(numbers2words(text))
        words = count_words(numbers2words(text))
        return round(syllables / words,2)
    return 0

def Fval(text):
    '''
    Words-per-sentence mean (F value)
    '''
    if is_non_empty_string(text):
        sencences = count_sentences(text)
        words = count_words(numbers2words(text))
        return round(words / sencences,2)
    return 0


def fernandez_huerta(text):
    '''
    Fernández Huerta readability score
    '''
    if is_non_empty_string(text):
        fernandez_huerta = 206.84 - 60*Pval(text) - 1.02*Fval(text)
        return round(fernandez_huerta,2)
    return -1


def szigriszt_pazos(text):
    '''
    Szigriszt Pazos readability score (1992)
    '''
    if is_non_empty_string(text):
        return round(206.835 - 62.3 * ( count_all_syllables(numbers2words(text)) / count_words(numbers2words(text))) - (count_words(numbers2words(text)) / count_sentences(text)),2)
    return -1

def gutierrez(text):
    '''
    Gutiérrez de Polini's readability score (1972)
    '''
    if is_non_empty_string(text):
        legibguti = 95.2 - 9.7 * (count_letters(text) / count_words(text)) - 0.35 * (count_words(text) / count_sentences(text))
        return round(legibguti, 2)
    return -1

def mu(text):
    '''
    Muñoz Baquedano and Muñoz Urra's readability score (2006)
    '''
    if is_non_empty_string(text):
        n = count_words(text)
        # Delete all digits
        text = ''.join(filter(lambda x: not x.isdigit(), text))
        # Cleans it all
        clean = re.compile('\W+')
        text = clean.sub(' ', text).strip()
        text = text.split() # word list
        word_lengths = []
        for word in text:
            word_lengths.append(len(word))
        # The mean calculation needs at least 1 value on the list, and the variance, two. If somebody enters only one word or, what is worse, a figure, the calculation breaks, so this is a 'fix'
        try:
            mean = statistics.mean(word_lengths)
            variance = statistics.variance(word_lengths)
            mu = (n / (n - 1)) * (mean / variance) * 100
            return round(mu, 2)
        except:
            return 0
    return -1

def crawford(text):
    '''
    Crawford's readability formula
    '''
    if is_non_empty_string(text):
        sentences = count_sentences(text)
        words = count_words(numbers2words(text))
        syllables = count_all_syllables(numbers2words(text))
        SeW = 100 * sentences / words # number of sentences per 100 words (mean)
        SiW = 100 * syllables / words # number of syllables in 100 words (mean)
        years = -0.205 * SeW + 0.049 * SiW - 3.407
        years = round(years,1)
        return years
    return -1


def interpretaP(P):
    '''
    Szigriszt-Pazos score interpretation
    '''
    if P < 0:
        return "no calculado"
    elif P <= 15:
        return "muy difícil"
    elif P > 15 and P <= 35:
        return "árido"
    elif P > 35 and P <= 50:
        return "bastante difícil"
    elif P > 50 and P <= 65:
        return "normal"
    elif P > 65 and P <= 75:
        return "bastante fácil"
    elif P > 75 and P <= 85:
        return "fácil"
    else:
        return "muy fácil"



# Interpreta la fernandez_huerta
def interpretaL(L):
    if L < 0:
        return "no calculado"
    elif L < 30:
        return "muy difícil"
    elif L >= 30 and L < 50:
        return "difícil"
    elif L >= 50 and L < 60:
        return "bastante difícil"
    elif L >= 60 and L < 70:
        return "normal"
    elif L >= 70 and L < 80:
        return "bastante fácil"
    elif L >= 80 and L < 90:
        return "fácil"
    else:
        return "muy fácil"


# Interpretación Inflesz

def inflesz(P):
    if P < 0:
        return "no calculado"
    elif P <= 40:
        return "muy difícil"
    elif P > 40 and P <= 55:
        return "algo difícil"
    elif P > 55 and P <= 65:
        return "normal"
    elif P > 65 and P <= 80:
        return "bastante fácil"
    else:
        return "muy fácil"


def gutierrez_interpret(G):
    if G < 0:
        return "no calculado"
    if G <= 33.33:
        return "difícil"
    if G > 33.33 and G < 66.66:
        return "normal"
    else:
        return "fácil"

def mu_interpret(M):
    if M < 0:
        return "no calculado"
    elif M < 31:
        return "muy difícil"
    elif M >= 31 and M <= 51:
        return "difícil"
    elif M >= 51 and M < 61:
        return "un poco difícil"
    elif M >= 61 and M < 71:
        return "adecuado"
    elif M >= 71 and M < 81:
        return "un poco fácil"
    elif M >= 81 and M < 91:
        return "fácil"
    else:
        return "muy fácil"

# See ejemplo.py to see how it works!


