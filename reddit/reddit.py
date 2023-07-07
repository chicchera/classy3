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

from settings import get_GLOBS

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
        "date_posted",
    ],
)

GLOBS = get_GLOBS()


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

    for subreddit_name in GLOBS["SUBREDS"]:
        subreddit = reddit.subreddit(subreddit_name)
        print(subreddit.id, subreddit.name, subreddit.display_name)

        last_downloaded_timestamp = 0
        submissions = subreddit.new(limit=None)
        for submission in submissions:
            print(f"{submission.id=} - {submission.title=}")
            # check if submission.author is of type Redditor and has attribute 'id'
            if isinstance(submission.author, Redditor) and hasattr(
                submission.author, "id"
            ):
                author_id = submission.author.id
            else:
                author_id = None

            submission_dict = {
                "submission_id": submission.id,
                "author_id": author_id,
                "title": submission.title,
                "created_utc": submission.created_utc,
                "score": submission.score,
                "NSFW": submission.over_18,
                "selftext_html": submission.selftext_html,
                "comment_forest": submission.comments,
            }
            submission.comments.replace_more(limit=None)
            for comment in submission.comments.list():
                print(f"{comment.id=} - {comment.body_html=}")
            # comment_queue = submission.comments[:]  # Seed with top-level
            # # traverse_comments(submission.comments)
            # while comment_queue:
            #     comment = comment_queue.pop(0)
            #     print(f"{comment.body=}")
            #     comment_queue.extend(comment.replies)

    return


scrape()
