from legibilidad import *

def calculate_metrics(text: str) -> tuple:
    letters = count_letters(text)
    paragraphs = count_paragraphs(text)
    sentences = count_sentences(text)
    len_string = len(text)
    all_syllables = count_all_syllables(text)
    syllables_x_word = Pval
    syllables_x_sentence =Fval
    tmp_words = text.split
    num_words = len(tmp_words)
    distinct_words = len(set(tmp_words))


    repeated_letters_in_string = sum(c for c in text if text.count(c) > 1)
    num_words_in_string = len(text.split())
    return len_string, num_letters_in_string, repeated_letters_in_string, num_words_in_string


def calc_df(df):
       # has at least the following structure
    # df['id_submission', 'content', 'kind', 'id_comment']df
    # if the number of errors is relevant, the column "misspells" arrives already populated

    # df[['paragraphs', 'sentences', 'syllables', 'num_words', 'distinct_words', 'unique_words', 'misspells', 'enthropy' 'redundancy' 'density']]  = np.nan



    """

    To create a new DataFrame or extend the existing one with additional columns based on calculations from the 'content' column and then save it to SQLite, you can follow these steps using the pandas library in Python:

    Calculate the Desired Metrics: Calculate the various metrics you want to add as new columns to the DataFrame. You can use Python functions to compute these metrics for each row in the 'content' column.

    Create a New DataFrame or Extend the Existing One: You can either create a new DataFrame with the calculated columns or extend the existing one by adding new columns.

    Save the DataFrame to SQLite: Use the to_sql method to save the DataFrame to an SQLite database.

    Here's a code example to illustrate these steps:

    import pandas as pd
    import sqlite3

    # Sample DataFrame with 'id_submission' and 'content' columns
    data = {'id_submission': [1, 2, 3],
            'content': ["This is a sample text.", "Another text here.", "Yet another example."]}
    df = pd.DataFrame(data)

    # Function to calculate desired metrics
    def calculate_metrics(text):
        letters
        len_string = len(text)
        num_letters_in_string = sum(c.isalpha() for c in text)
        repeated_letters_in_string = len([c for c in set(text.lower()) if text.lower().count(c) > 1])
        num_words_in_string = len(text.split())
        # Add more metrics as needed
        return len_string, num_letters_in_string, repeated_letters_in_string, num_words_in_string

    # Calculate metrics and add them as new columns
    df['len_string'], df['num_letters'], df['repeated_letters'], df['num_words'] = zip(*df['content'].apply(calculate_metrics))

    # Now, 'df' contains the original columns along with the calculated columns

    # Save the DataFrame to an SQLite database
    conn = sqlite3.connect('your_database.db')  # Replace with your database path
    df.to_sql('your_table_name', conn, if_exists='replace', index=False)

    # Close the database connection
    conn.close()
    """