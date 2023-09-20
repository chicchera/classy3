from db_utils.dbutils import DbsConnection
from rich import print
from settings import get_globs_key
from scraper.praw_functions import create_praw, get_subreddit
from app_logger import logger


reddit = create_praw()

# with DbsConnection as conn:
#     cursor = conn.cursor()
#     cursor.execute("SELECT * FROM subreddits")
#     subreddits_records = cursor.fetchall()
#     print(subreddits_records)
#     exit(0)


def update_subreddits() -> dict:
    subreddits_list = get_globs_key('SUBREDS')

    with DbsConnection() as conn:
        c = conn.cursor()
        for subred in subreddits_list:
            c.execute("SELECT name FROM subreddits WHERE name=?", (subred,))
            result = c.fetchone()

            if result is None:
                subreddit = get_subreddit(subred, reddit)
                print(subreddit)
                exit(0)
