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


from settings import get_GLOBS
GLOBS = get_GLOBS()

Submission = namedtuple(
    "Submission",
        ['id_submission',
        'id_redditor',
        'id_subreddit',
        'title',
        'body',
        'score',
        'over_18',
        'ama',
        'serio',
        'tonto_index',
        'created_utc'
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

    last_downloaded_timestamp = 0
    for subreddit_name in (pbar := tqdm(GLOBS["SUBREDS"])):
        pbar.set_description(subreddit_name)
        subreddit = reddit.subreddit(subreddit_name)
        submissions = subreddit.new(limit=None)
        submissions_list = []
        for submission in submissions:
            # print(f"{submission.id=} - {submission.title=}")
            author_id = getattr(submission.author, "id", None)

            S = Submission(
                id_submission = submission.id,
                id_redditor = submission.author_id,
                title = submission.title,
                created_utc = submission.created_utc,
                score = submission.score,
                over_18 = submission.over_18,
                selftext_html = submission.selftext_html,
                comment_forest = submission.comments
            )
            submission.comments.replace_more(limit=None)
            for comment in submission.comments.list():
                print(f"{comment.id=} - {comment.body_html=}")

    return
