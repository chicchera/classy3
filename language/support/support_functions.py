import os


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

def ____read_words_and_punctuation(file_path, num_words):
    with open(file_path, 'r', encoding='utf-8') as file:
        word_count = 0
        paragraph = ''
        prev_line_empty = False  # Track if the previous line was empty

        for line in file:
            line = line.strip()  # Remove leading/trailing white space
            if not line:  # Check if the line is empty
                if not prev_line_empty:
                    paragraph += '\n\n'  # Add a paragraph break if it's not consecutive empty lines
                prev_line_empty = True
                continue
            prev_line_empty = False

            words = line.split()
            for word in words:
                paragraph += word + ' '  # Include spaces to preserve punctuation
                word_count += 1
                if word_count >= num_words:
                    return paragraph.rstrip(), word_count

    return paragraph.rstrip(), word_count

def __read_words_and_punctuation(file_path, num_words):
    with open(file_path, 'r', encoding='utf-8') as file:
        word_count = 0
        paragraph = ''
        for line in file:
            words = line.split()
            for word in words:
                paragraph += word + ' '  # Include spaces to preserve punctuation
                word_count += 1
                if word_count >= num_words:
                    return paragraph.rstrip(), word_count
    return paragraph.rstrip(), word_count  # In case the file ends before reaching the word count

"""
# Example usage:
file_path = 'your_novel.txt'
num_words_to_read = 50000
text, actual_word_count = read_words_and_punctuation(file_path, num_words_to_read)

# Print the text and the actual word count
print(text)
print("Actual Word Count:", actual_word_count)
"""

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

"""
This function if fast as is based on a generetor
but it doesn't preserve punctuation
# Example usage:
file_path = 'your_novel.txt'
num_words_to_read = 50000
word_generator = read_words_from_file(file_path, num_words_to_read)

for word in word_generator:
    # Process the word here
    print(word)
"""
