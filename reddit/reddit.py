"""
    this file contains all the routines to access reddit directly without going throug an external program to retrieve the data
"""
from collections import namedtuple
import praw
import prawcore
from praw.models import Redditor
from praw.models import MoreComments
import configparser
from datetime import datetime
import time
from reddit.redutils import createPRAW
from rich import print
from tqdm import tqdm

from utils.misc import GracefulExiter
import db_utils.dbutils as dbu


from settings import get_GLOBS
GLOBS = get_GLOBS()

Subreddit = namedtuple(
    "Subreddit",
        [
            "id_subreddit",
            "name" ,
            "created_utc",
            "display_name",
            "description",
            "over_18",
            "last_submission_id",
            "last_submission_utc",
            "last_scraped_utc"
        ]
)
Submission = namedtuple(
    "Submission",
        ['id_submission',
        'id_redditor',
        'id_subreddit',
        'title',
        'selftext',
        'score',
        'over_18',
        'ama',
        'serio',
        'tonto_index',
        'created_utc',
        'num_comments'
    ]
)
Comment = namedtuple(
    "Comment",
    [
        "id",
        "author_id",
        "body_html",
        "score",
        "is_submitter",
        "parent_id",
        "submission_id",
        "date_posted"
    ]
)
Redditor = namedtuple(
    "Redditor",
    [
        'id_redditor',
        'name',
        'has_verified_mail',
        'created_utc',
        'bad_record'
    ]
)


def traverse_comments(comments):
    """
    Traverses through a list of the comments of a Reddit post and prints the body of each comment.

    Args:
        comments (list): A list of comments to traverse through.

    Returns:
        None: This function does not return anything.
    """
    all_comments = []
    for top_level_comment in comments:
        if isinstance(top_level_comment, MoreComments):
            continue
        if top_level_comment.stickied:
            continue
        all_comments.append(
            Comment[
                top_level_comment.id,
                top_level_comment.author.id,
                top_level_comment.body_html,
                top_level_comment.score,
                top_level_comment.is_submitter,
                top_level_comment.parent_id,
                top_level_comment.submission.id,
                top_level_comment.created_utc,
            ]
        )
        print(f"{top_level_comment.body=}")
        traverse_comments(top_level_comment.replies)
    return all_comments


def scrape():
    reddit = createPRAW()
    last_downloaded_timestamp = 0
    max_retries = 3
    retry_delay = 5

    subreddit_exit = False
    submission_exit = False
    author_exit = False

    abort = False

    # print(subreddit.id, subreddit.name, subreddit.display_name)

    with dbu.DbsConnection() as conn:
        c = conn.cursor()
        # Add a dummy user for deleted redditors
        c.execute("INSERT OR IGNORE INTO redditors (id_redditor, name, has_verified_mail, created_utc, bad_record) VALUES('000','nn',False,1689850792,True);")

        for subreddit_name in GLOBS["SUBREDS"]:

            c.execute(f"SELECT name FROM subreddits WHERE name = '{subreddit_name}';")
            result = c.fetchone()
            if result is None:
                subreddit = reddit.subreddit(subreddit_name)
                c.execute(f"""
                    INSERT INTO subreddits(
                        id_subreddit,
                        name,
                        created_utc,
                        last_submission_id,
                        last_submission_utc,
                        last_scraped_utc,
                        description,
                        display_name)
                    VALUES
                        (
                        '{subreddit.id}',
                        '{subreddit_name}',
                        {subreddit.created_utc},
                        '000',
                        {subreddit.created_utc},
                        {subreddit.created_utc},
                        '{subreddit.description}',
                        '{subreddit.display_name}');""")
        conn.commit()
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


