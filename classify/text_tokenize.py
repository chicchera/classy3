import time
import re
import db_utils.dbutils as dbu
import db_utils.queries as dbq
import utils.txt_utils as tu
from nltk.stem.snowball import SnowballStemmer

import spacy
from rich import print as rprint
from settings import get_GLOBS
from tqdm import tqdm
from utils.misc import GracefulExiter, get_random_string
from settings import get_GLOBS
GLOBS = get_GLOBS()

stemmer = SnowballStemmer("spanish")
# GLOBS = get_GLOBS()
stopwords = tu.stopwords

NoSw_Dups = "NS"
NoSw_NoDups = "ND"
Lemma_Dups = "LD"
Stemma_Dups = "SD"

QRY_CHUNK = GLOBS["MISC"].get("CHUNK") * 3

# Load Spacy's small spanish model
# nlp = spacy.load("es_core_news_sm")
nlp = spacy.load("es_core_news_sm", disable=["parser", "ner"])


def lemmatize_sentence(sentence: str) -> str:
    """
    Lemmatizes a given sentence using Spacy library.

    Parameters:
    sentence (str): The sentence to be lemmatized.

    Returns:
    str: The lemmatized sentence.
    """

    # Process the sentence using the loaded model
    doc = nlp(sentence)

    # Lemmatize each word in the processed sentence and join them using a space

    return " ".join([word.lemma_ for word in doc])


def no_stopwords(sentence) -> str:
    """
    Takes in a sentence and returns a new string with all stopwords removed.

    :param sentence: A string representing the sentence to be processed.
    :type sentence: str
    :return: A string representing the processed sentence with stopwords removed.
    :rtype: str
    """
    lst_sentence = sentence.split()
    return " ".join([word for word in lst_sentence if word not in stopwords])


def tokenize_content(content: str) -> dict:
    """
    Tokenizes the content of a given row using a set of stop words. Returns a dictionary with the following keys:
    - NoSw_Dups: the content with stop words removed
    - NoSw_NoDups: the content with stop words and duplicates removed
    - Stemma_Dups: the stemmed content with duplicates preserved
    - Lemma_Dups: lemmatized content with duplicates preserved

    :param row: a dictionary with "content" and "code" keys
    :type row: dict
    :return: a dictionary with the tokenized content
    :rtype: dict
    """

    if not content:
        return {}

    no_stops = no_stopwords(content)
    if not no_stops:
        return {}

    words = set(no_stops.split()).difference(stopwords)
    words = " ".join(words) if words else None
    if re.match("^[0-9 ]+$", words):
        return {}

    return {
        "NS": no_stops,
        "ND": words,
        "SD": stemmer.stem(no_stops),
        "LD": lemmatize_sentence(no_stops),
    }


def tokenize_posts(chunk: int = QRY_CHUNK):
    """
    Imports from the remote databas all the new submissions

    Args:
        chunk (int): max records to be returned at thh same time (to avoid out of memory errors)
        As the data returned is small we double the standard chunk size.
    """
    with dbu.DbsConnection() as conn:
        # create the temptable row_data that will work
        # as base for the tokenized data
        # the table is called temp.raw_data
        # qry_raw_data = dbq.qry_create_raw_data()
        conn.execute(dbq.qry_create_raw_data())

        qry = dbq.qry_get_posts_to_tokenize()
        # get the number of records the will return
        num_recs = dbu.query_will_return(qry, conn)

        blocks = int(num_recs / QRY_CHUNK)
        if num_recs % QRY_CHUNK > 0:
            blocks += 1
        current_offset = 0

        rprint()
        rprint("[Cyan]Press [bright_yellow]Ctrl-C[Cyan] to break this routne.")
        rprint(f"Tokenizing {num_recs:,.0f} records")
        exit_flag = GracefulExiter()
        tqdm.pandas(desc="blocks", leave=False, colour="magenta")
        start = time.time()

        for _ in tqdm(
            range(blocks), desc="Ctrl-c to suspend", colour="cyan", leave=False
        ):
            # rprint(
            #     dbq.qry_get_posts_to_tokenize(chunk=QRY_CHUNK, offset=current_offset)
            # )
            c = conn.cursor()
            c.execute(
                dbq.qry_get_posts_to_tokenize(chunk=QRY_CHUNK, offset=current_offset)
            )
            # conn.execute(
            #     dbq.qry_get_posts_to_tokenize(chunk=QRY_CHUNK, offset=current_offset)
            # )

            rows = c.fetchall()
            if not rows:
                break
            with tqdm(
                rows, desc="Tokenizing posts", colour="cyan", leave=False
            ) as pbar:
                # rows_count = len(rows)
                current_offset += QRY_CHUNK
                conn.execute("BEGIN TRANSACTION;")

                for row in rows:
                    # modified_content = modify_content(content)
                    save_tokens = tokenize_content(row["content"])

                    for key, value in save_tokens.items():
                        conn.execute(
                            "INSERT OR IGNORE INTO sort_base (rid_post, rid_comment, qa, code, content) VALUES (?, ?, ?, ?, ?)",
                            (
                                row["rid_post"],
                                row["rid_comment"],
                                row["qa"],
                                key,
                                value,
                            ),
                        )
                    pbar.update(1)
                conn.execute("COMMIT;")

            if exit_flag.exit():
                break

        end = time.time()
        rprint(f"[bright_yellow]Elapsed tokenizing time: {end - start}")
