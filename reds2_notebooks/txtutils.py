import traceback
import re
import os
import demoji
import unidecode
import pprint
from inscriptis import get_text
# from GLOBS import lg
from spellchecker import SpellChecker
from reds_utils.txtlists import (reddit_es_words, saludos_words, unwanted_words_es,
                            wc_stopwords_es, replace_saludos_words, ama_wrds,
                            no_ama_wrds, re_ama_wrds, lbls_patterns_,
                            re_patterns, es_stopwords)
from reds_utils.reds_utils import src_divider

spell_es = SpellChecker(language='es')

# #####################
# SymSpell
import pkg_resources
from symspellpy import SymSpell, Verbosity

pp = pprint.PrettyPrinter(indent=4)

# ATTN: for portability put es-100l.txt in a dir easily accesible by the app
dictionary_path = os.path.dirname(__file__) + "/es-100l.txt"
ss = SymSpell(max_dictionary_edit_distance=1, prefix_length=7)
ss.load_dictionary(dictionary_path, term_index=0, count_index=1)
#
# #####################

# TODO: labels/classification routine
# TODO: https://stackoverflow.com/questions/3271478/check-list-of-words-in-another-string
# TODO: !!!!! https://stackoverflow.com/a/21718896/18511264

# NO DIGITS: s = re.sub("^\d+\s|\s\d+\s|\s\d+$", " ", s)

re_nums_only = re.compile(r"^[0-9]*$")
re_nums_mix = re.compile(
    r"([A-Za-z\u00C0-\u017F]+[\d@]+[\w@]*|[\d@]+[A-Za-z]+[\w@]*)")

salutation_words = saludos_words()
salutation_replc = replace_saludos_words()

ama_words = ama_wrds()
no_ama_words = no_ama_wrds()
re_ama_words = re_ama_wrds()
stopwords = es_stopwords()

# with src_divider("Classification routines"):
#labels = classification_labels()
# master_patterns = lbls_patterns(labels)
master_patterns = re_patterns()

LABELS_TITLE_MULTIPLIER = 2
LABELS_TEXT_MULTIPLIER = 1

LABELS_MULTIPLIERS = [2, 1]


def classify_1(s1, s2) -> list:
    totals = {}
    retval = list()

    for lbl in master_patterns:
        cnt = 0
        cnt += (len(re.findall(master_patterns[lbl],
                               s1))) * LABELS_TITLE_MULTIPLIER
        if s2 is not None:
            cnt += len(re.findall(master_patterns[lbl],
                                  s2)) * LABELS_TEXT_MULTIPLIER
        totals[lbl] = cnt

    # sort the total by values descending
    x = dict(sorted(totals.items(), key=lambda item: item[1], reverse=True))

    # check if the top value is > 0, otherwise return None
    if next(iter(x)) == 0:
        #return list([[None]])
        return None

    keys = list(x)
    retval = list()
    if x[keys[0]] > 0:
        #retval = retval.extend([keys[0],x[keys[0]]])
        retval.append(list((keys[0], x[keys[0]])))
    else:
        return None

    if False: # The instruction below was causing to have two cats per post
        if x[keys[1]] > 0:
            # retval = retval.extend([keys[1],x[keys[1]]])
            retval.append(list((keys[1], x[keys[1]])))

    return retval


def classify_cnt(title, self_text) -> list:
    totals = {}
    retval = [None, 0, None, 0]

    for lbl in labels:
        cnt = 0
        cnt += (len(re.findall(master_patterns[lbl],
                               title))) * LABELS_TITLE_MULTIPLIER
        if self_text is not None:
            cnt += len(re.findall(master_patterns[lbl],
                                  self_text)) * LABELS_TEXT_MULTIPLIER
        totals[lbl] = cnt

    # sort the total by values descending
    x = dict(sorted(totals.items(), key=lambda item: item[1], reverse=True))

    # check if the top value is > 0, otherwise return None
    if next(iter(x)) == 0:
        return retval

    keys = list(x)

    if x[keys[0]] > 0:
        retval[0] = keys[0]
        retval[1] = x[keys[0]]

        if x[keys[1]] > 0:
            retval[2] = keys[1]
            retval[3] = x[keys[1]]

    return retval


def classify(title, self_text) -> str:
    totals = {}

    for lbl in labels:
        cnt = 0
        cnt += (len(re.findall(master_patterns[lbl],
                               title))) * LABELS_TITLE_MULTIPLIER
        if self_text is not None:
            cnt += len(re.findall(master_patterns[lbl],
                                  self_text)) * LABELS_TEXT_MULTIPLIER
        totals[lbl] = cnt

    # sort the total by values descending
    x = dict(sorted(totals.items(), key=lambda item: item[1], reverse=True))

    # check if the top value is > 0, otherwise return None
    if next(iter(x)) == 0:
        return None

    keys = list(x)
    retval = ''

    if x[keys[0]] > 0:
        retval += f"{keys[0]}-{x[keys[0]]}"
        # if the second value in the list is also grater than 0 add it to the return value
        if x[keys[1]] > 0:
            retval += f",{keys[1]}-{x[keys[1]]}"
            # if the first ana seconda values are equal add "CHECK" to the return value
            if x[keys[0]] == x[keys[1]]:
                retval += ' !CHECK'

    return retval


def no_digits(s) -> str:
    if not s is None:
        return re.sub(r"^\d+\s|\s\d+\s|\s\d+$", " ", f" {s} ").strip()


def no_html(s) -> str:
    if s is None:
        return ''
    return get_text(s).strip()


def clean_text(s) -> str:
    if s is None:
        return None
    elif s.startswith('View Poll'):
        return None

    s = s.strip()
    s = no_html(s)

    s = s.replace('/', ' ')
    # replace the "at @" character with an o
    s = s.replace('@', 'o')
    # remove multiple white spaces
    s = ' '.join(s.split())
    # remove punctuation
    s = re.sub(r'[^\w\s]', '', s)
    # remove all the emojis, if any
    return demoji.replace(s, '').lower()


def fast_clean_text(s) -> str:
    if s is None:
        None
    elif s.startswith('<!--'):
        s = no_html(s)
    # replace the "at @" character with an o
    s = s.replace('@', 'o')
    # remove all the emojis, if any
    return demoji.replace(s, '')


def spell_wrd(w) -> str:
    if re_nums_only.match(w):
        return w
    if re_nums_mix.match(w):
        w = w.replace("1", "i").replace("3", "e").replace("4", "a").replace(
            "5", "s").replace("7", "t").replace("0", "o")
    suggestions = ss.lookup(w,
                            Verbosity.CLOSEST,
                            max_edit_distance=1,
                            include_unknown=True,
                            transfer_casing=False)
    return str(suggestions[0]).split(',')[0]


def wrd_exists(w) -> bool:
    if re_nums_only.match(w):
        return True
    suggestions = ss.lookup(w,
                            Verbosity.TOP,
                            max_edit_distance=1,
                            include_unknown=False,
                            transfer_casing=False)
    suggested = str(suggestions[0]).split(',')[0]
    plain = unidecode.unidecode(suggested)
    if len(w) > 1:
        if plain != w:
            return False
    return True
    # print(f"[{w=} ] [{suggested=} ]")
    # return str(suggestions[0]).split(',')[0]


def fast_correct_spelling(s):
    if s is not None:
        return ' '.join(spell_wrd(w) for w in s.split())
    # s = clean_text(s)


def correct_spelling(s) -> str:
    if s is None:
        return ''
    return ' '.join(spell_es.correction(w) for w in s.split())


def find_misspellings(s) -> str:
    if s is None:
        return ''
    return ' '.join(spell_es.unknown(s.split()))


def misspellings(original, corrected) -> str:
    '''Returns the differences between two string,
       the seconda onebeing the corrected one.
    '''

    return ' '.join(
        set(xstr(original).split()).difference(set(xstr(corrected).split())))


def xstr(s) -> str:
    '''Returns an empy string if the value is null.'''
    if s is None:
        return ''
    return str(s)


def snone(s) -> None:
    '''Returns none for en empy string'''
    if s is not None:
        if len(s.strip()) == 0:
            return None
    return s


def fast_check_txt_fields(s1, s2) -> str:
    s1_original = clean_text(s1)
    s2_original = clean_text(s2)
    ss1 = fast_correct_spelling(s1_original)
    ss2 = fast_correct_spelling(s2_original)

    original = xstr(s1_original) + ' ' + xstr(s2_original)
    corrected = xstr(ss1) + ' ' + xstr(ss2)

    err = misspellings(original, corrected)
    if not err.strip():
        err = None
    else:
        err = no_digits(err)

    return [no_pregunta_seria(ss1), ss2, err]


def no_pregunta_seria(s):
    return s.replace('pregunta seria', '').replace('serio', '').replace('pregunta súper seria','')


def is_ama(s) -> bool:
    if (s is None):
        return 0
    for words in no_ama_words:
        if re.search(r'\b' + words + r'\b', s):
            return 1
    for words in re_ama_words:
        if re.search(r'\b' + words + r'\b', s):
            return 1
    return 1 if (len([w for w in ama_words if w in s]) > 0) else 0


def replace_salutations(s) -> str:
    s = s.strip()

    for check in salutation_words:
        if s.startswith(check):
            rep = re.findall(r"(?=(" + '|'.join(salutation_replc) + r"))",
                             check)
            if len(rep) > 0:
                return s.replace(check, rep[0], 1)
            else:
                if len(s) == 0:
                    return 'sin título'

            return s


def no_stopwords(s: str) -> str:
    return ' '.join(filter(lambda word: word not in stopwords, s.split()))

def remove_leading_digits_and_spaces(input_string: str):
    pattern = r'^[\d\s]+'
    result = re.sub(pattern, '', input_string)
    return result if result else None

