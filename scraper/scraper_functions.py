from app_logger import logger
from db_utils.dbutils import DbsConnection
from rich import print
from scraper.praw_functions import create_praw, get_subreddit
from settings import get_globs_key

reddit = create_praw()

def update_subreddits() -> dict:
    qry_update_subreddits = """
    INSERT INTO subreddits (id_subreddit, name, created_utc, display_name, description, over_18) VALUES (?, ?, ?, ?, ?, ?);
    """
    subreddits_list = get_globs_key('SUBREDS')

    with DbsConnection() as conn:
        c = conn.cursor()
        for subred in subreddits_list:
            c.execute("SELECT name FROM subreddits WHERE name=?", (subred,))
            result = c.fetchone()

            if result is None:
                subreddit = get_subreddit(subred, reddit)
                c.execute(qry_update_subreddits,(subreddit.id, subred, subreddit.created_utc, subreddit.display_name, subreddit.description, subreddit.over18))



