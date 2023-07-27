import praw
import prawcore
from praw.models import MoreComments
import configparser
from datetime import datetime
import time
from scraper.redutils import createPRAW
from rich import print
from tqdm import tqdm

from utils.misc import GracefulExiter
import db_utils.dbutils as dbu
from scraper.structures import Submission, Comment, Redditor, Subreddit, init_tables

from settings import get_GLOBS
GLOBS = get_GLOBS()
reddit = createPRAW()

subreddits_list = init_tables()

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
    print(GLOBS)
    posts_chunk_size = GLOBS['MISC'].get('POSTS_CHUNK')

    # print(subreddit.id, subreddit.name, subreddit.display_name)

    with dbu.DbsConnection() as conn:
        c = conn.cursor()

        pbar = tqdm(total=len(subreddits_list), leave=True)
        for i in tqdm(range(len(subreddits_list))):
            current_subreddit = subreddits_list[i]
            pbar.set_description(current_subreddit['name'])

            subreddit = reddit.subreddit(current_subreddit['name'])

            submissions = subreddit.new(limit=None)
            submissions_list = []
            comments_list = []
            print(submissions)
            for submission in submissions:
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
    return

