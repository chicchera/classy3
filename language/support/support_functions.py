import spacy
import string
import pyphen

# Load the language models
nlp_en = spacy.load("en_core_web_sm")
nlp_es = spacy.load("es_core_news_sm")
nlp_it = spacy.load("it_core_news_sm")

def count_sentences_and_punctuation(text, language):
    if language == "en":
        nlp = nlp_en
    elif language == "es":
        nlp = nlp_es
    elif language == "it":
        nlp = nlp_it
    else:
        raise ValueError("Unsupported language")

    # Process the text
    doc = nlp(text)

    sentence_count = 0
    punctuation_count = 0

    for sentence in doc.sents:
        sentence_count += 1
        punctuation_count += sum(1 for token in sentence if token.text in string.punctuation)

    return sentence_count, punctuation_count

def count_syllables(word, language):
    if language == "en":
        dic = pyphen.Pyphen(lang='en_US')
    elif language == "es":
        dic = pyphen.Pyphen(lang='es')
    elif language == "it":
        dic = pyphen.Pyphen(lang='it_IT')
    else:
        raise ValueError("Unsupported language")

    return len(dic.inserted(word).split("-"))

def get_text_with_paragraph(file_path, num_words, language):
    def paragraphs_generator(file_path):
        with open(file_path, 'r') as file:
            paragraph = []
            for line in file:
                line = line.strip()
                if line:
                    paragraph.append(line)
                elif paragraph:
                    yield ' '.join(paragraph)
                    paragraph = []
            if paragraph:
                yield ' '.join(paragraph)

    selected_paragraphs = []
    word_count = 0
    paragraph_count = 0
    syllables_count = 0

    for paragraph in paragraphs_generator(file_path):
        words = paragraph.split()
        paragraph_word_count = len(words)

        if word_count + paragraph_word_count <= num_words:
            selected_paragraphs.append(paragraph)
            word_count += paragraph_word_count
            paragraph_count += 1

            # Count syllables in words within the paragraph
            for word in words:
                syllables_count += count_syllables(word, language)
        else:
            break

    final_text = '\n\n'.join(selected_paragraphs)

    sentence_count, punctuation_count = count_sentences_and_punctuation(final_text, language)

    return final_text, word_count, paragraph_count, sentence_count, punctuation_count, syllables_count
