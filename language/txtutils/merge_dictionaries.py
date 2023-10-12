def load_dictionary(file_path):
    dictionary = {}
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            parts = line.strip().split()  # Split each line into word and frequency
            if len(parts) == 2:
                word, frequency = parts[0], int(parts[1])

                dictionary[word] = frequency
    return dictionary

def scale_word_frequencies(symspell_dictionary, subtitle_dictionary):
    # Calculate the sum of word frequencies in each dictionary
    symspell_freq1 = sum(symspell_dictionary.values())
    subtitle_freq2 = sum(subtitle_dictionary.values())

    # Calculate the scaling factor
    scaling_factor = symspell_freq1 / subtitle_freq2
    scaled_subtitle_dictionary = {word: int(freq * scaling_factor) for word, freq in subtitle_dictionary.items()}

    return scaled_subtitle_dictionary


def merge_and_write_dictionaries(dictionary1, dictionary2, output_file_path):
    # Merge the dictionaries, overwriting values from dictionary2 for duplicate keys
    merged_dictionary = {**dictionary1, **dictionary2}

    # Sort the merged dictionary by keys in alphabetical order
    # sorted_merged_dictionary = dict(sorted(merged_dictionary.items()))
    sorted_merged_dictionary = dict(sorted(merged_dictionary.items(), key=lambda item: item[1], reverse=True))

    # Write the sorted merged dictionary to a file
    with open(output_file_path, 'w', encoding='utf-8') as output_file:
        for key, value in sorted_merged_dictionary.items():
            output_file.write(f"{key} {value}\n")


config_path = "/home/silvio/miniconda3/envs/classy3/prg/config/"
symspell_dictionary_path = config_path + 'es-100l-dic.txt'
subtitle_dictionary_path = config_path + 'subtl_es.txt'
new_dic = config_path + 'new_dic.txt'

symspell_dictionary = load_dictionary(symspell_dictionary_path)
subtitle_dictionary = load_dictionary(subtitle_dictionary_path)

scaled_subtitle_dictionary = scale_word_frequencies(symspell_dictionary, subtitle_dictionary)

merge_and_write_dictionaries(symspell_dictionary, scaled_subtitle_dictionary, new_dic)
