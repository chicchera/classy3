import spacy
import string

# Load the language models
nlp_en = spacy.load("en_core_web_sm")
nlp_es = spacy.load("es_core_news_sm")
nlp_it = spacy.load("it_core_news_sm")

def count_sentences(text, language):
    if language == "english":
        nlp = nlp_en
    elif language == "spanish":
        nlp = nlp_es
    elif language == "italian":
        nlp = nlp_it
    else:
        raise ValueError("Unsupported language")

    # Process the text
    doc = nlp(text)

    # Count the number of sentences
    return len(list(doc.sents))

# Example usage:
# text = "This is a sample paragraph. It contains multiple sentences. Can you count them?"
# language = "english"
# sentence_count = count_sentences(text, language)
# print("Number of sentences:", sentence_count)


def count_sentences_and_words(text, language):
    if language == "english":
        nlp = nlp_en
    elif language == "spanish":
        nlp = nlp_es
    elif language == "italian":
        nlp = nlp_it
    else:
        raise ValueError("Unsupported language")

    # Process the text
    doc = nlp(text)

    sentence_count = 0
    word_count_per_sentence = []

    for sentence in doc.sents:
        sentence_count += 1
        words = [token.text for token in sentence if not token.is_punct]
        word_count_per_sentence.append(len(words))

    return sentence_count, word_count_per_sentence

# Example usage:
# text = "This is a sample paragraph. It contains multiple sentences. Can you count them?"
# language = "english"
# sentence_count, word_count_per_sentence = count_sentences_and_words(text, language)

# print("Number of sentences:", sentence_count)
# print("Word count per sentence:", word_count_per_sentence)


def count_punctuation_per_sentence(text, language):
    if language == "english":
        nlp = nlp_en
    elif language == "spanish":
        nlp = nlp_es
    elif language == "italian":
        nlp = nlp_it
    else:
        raise ValueError("Unsupported language")

    # Process the text
    doc = nlp(text)

    punctuation_count_per_sentence = []

    for sentence in doc.sents:
        punctuation_count = sum(1 for token in sentence if token.text in string.punctuation)
        punctuation_count_per_sentence.append(punctuation_count)

    return punctuation_count_per_sentence

# Example usage:
# text = "This is a sample paragraph. It contains multiple sentences! Can you count them?"
# language = "english"
# punctuation_count_per_sentence = count_punctuation_per_sentence(text, language)

# print("Punctuation count per sentence:", punctuation_count_per_sentence)

def read_words_and_punctuation(file_path, num_words):
    with open(file_path, 'r', encoding='utf-8') as file:
        word_count = 0
        paragraph = ''
        prev_line_empty = False

        for line in file:
            line = line.strip()
            if not line:
                if not prev_line_empty:
                    paragraph += '\n\n'
                prev_line_empty = True
                continue
            prev_line_empty = False

            words = line.split()
            for word in words:
                paragraph += word + ' '
                word_count += 1
                if word_count >= num_words:
                    return paragraph.rstrip(), word_count

    return paragraph.rstrip(), word_count


def read_words_from_file(file_path, num_words):
    with open(file_path, 'r', encoding='utf-8') as file:
        word_count = 0
        for line in file:
            words = line.split()
            for word in words:
                yield word
                word_count += 1
                if word_count >= num_words:
                    return
