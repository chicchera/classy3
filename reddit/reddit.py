"""
    this file contains all the routines to access reddit directly without going throug an external program to retrieve the data
"""
# from collections import namedtuple
import praw
import prawcore
from praw.models import MoreComments
import configparser
from datetime import datetime
import time
from reddit.redutils import createPRAW
from rich import print
from tqdm import tqdm

from utils.misc import GracefulExiter
import db_utils.dbutils as dbu
from reddit.structures import Submission, Comment, Redditor, Subreddit, init_tables

from settings import get_GLOBS
GLOBS = get_GLOBS()
reddit = createPRAW()

init_tables()

def scrape():
    """
    Scrapes data from Reddit using the PRAW library and saves it into a database.

    Parameters:
    None

    Returns:
    None
    """


    last_downloaded_timestamp = 0
    max_retries = 3
    retry_delay = 5

    subreddit_exit = False
    submission_exit = False
    author_exit = False

    abort = False

    # print(subreddit.id, subreddit.name, subreddit.display_name)

    init_tables()

    with dbu.DbsConnection() as conn:
        c = conn.cursor()
        for subreddit_name in (pbar := tqdm(GLOBS["SUBREDS"])):
            pbar.set_description(subreddit_name)

            subreddit = reddit.subreddit(subreddit_name)
            with dbu.DbsConnection() as conn:
                c = conn.cursor()
                # Execute the query to retrieve the highest created_utc and id_submission
                c.execute(f"""SELECT last_submission_utc, last_submission_id FROM subreddits WHERE name = '{subreddit_name}';""")
                result = c.fetchone()
                # Store the values in variables
                oldest_submission_utc = result[0]
                oldest_submission_id = result[1]

            submissions = subreddit.new(limit=None)
            submissions_list = []
            comments_list = []

            for submission in submissions:
                # assert submission is not None, "Submission is None!"
                # assert submission.id is not None, "Submission.id is None!"

                if submission is None:
                    continue
                if submission.stickied:
                    continue
                print(submission)
                print('#' * 50)

                print(f"{submission.id=} - {submission.title=}, {submission.created_utc=},{oldest_submission_utc=}")
                # exit(0)

                if submission.created_utc > oldest_submission_utc:
                    S = Submission(
                        id_submission = submission.id,
                        id_redditor = getattr(submission.author, "id", '000'),
                        id_subreddit = subreddit.id,
                        title = submission.title,
                        score = submission.score,
                        over_18 = submission.over_18,
                        ama = False,
                        serio = False,
                        tonto_index = 0,
                        created_utc = submission.created_utc,
                        selftext = submission.selftext,
                        num_comments = submission.num_comments
                    )
                    submissions_list.append(S)
                else:
                    update_subreddits_qry = f"UPDATE subreddits SET "
                    last_downloaded_timestamp = submission.created_utc


                submission.comments.replace_more(limit=None)
                """
                all_comments = submission.comments.list()
                sorted_comments = sorted(all_comments, key=lambda comment: comment.created_utc, reverse=True)
                """
                for comment in submission.comments.list():
                    SC = Comment(
                        id = comment.id,
                        author_id = comment.author.id,
                        body_html = comment.body_html,
                        score = comment.score,
                        is_submitter = comment.is_submitter,
                        parent_id = comment.parent_id,
                        submission_id = submission.id,
                        date_posted = comment.created_utc
                    )
                    print(f"{comment.id=} - {comment.body_html=}")
                    # if GracefulExiter:
                    #     exit(1)

            with dbu.DbsConnection() as conn:
                c = conn.cursor()
                c.executemany(
                    "insert or ignore into submissions values (?,?,?,?,?,?,?,?,?,?,?,?)",submissions_list
                )
                c.executemany(
                "insert or ignore into comments values (?,?,?,?,?,?,?,?)", comments_list)


