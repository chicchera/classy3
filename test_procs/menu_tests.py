import time
import praw
import prawcore
from praw.models import MoreComments
from rich import print
from rich import inspect
import db_utils.dbutils as dbu
from utils.misc import GracefulExiter
from scraper.redutils import createPRAW

R_COMMENT = 't1_'
R_USER = 't2_'
# R_SUBMISSION = 't3_' # submissions dont need prefixes
R_MESSAGE = 't4_'
R_SUBREDDIT = 't5_'
R_AWARD = 't6_'

TEST_ID = None

"""
SEE:
https://www.reddit.com/r/redditdev/comments/aoe4pk/praw_getting_multiple_submissions_using_by_id/

https://www.google.com/search?q=site%3Awww.reddit.com+%22praw%22+%22reddit.info%22+-pushshift
"""


def test_info(TEST_ID):
    try:
        reddit = createPRAW()

        with dbu.DbsConnection() as conn:
            conn.row_factory = lambda cursor, row: row[0]
            c = conn.cursor()
            # submission_ids = ['15oe1oy']
            if TEST_ID is not None:
                submission_ids = ['TEST_ID']
            else:
                # submission_ids = c.execute('SELECT id_submission FROM submissions INDEXED BY submissions_created_utc_DESC_idx LIMIT 1;').fetchall()
                print(submission_ids)

            for  id_sub in submission_ids:
                # submission = reddit.submission(id)
                submission = reddit.submission(id=id_sub)

                if submission:
                    print(f"Submission Title: {submission.title}")
                    print(f"Submission URL: {submission.url}")
                    print(f"author full name: {submission.author_fullname}")
                else:
                    print("Submission retrieval failed.")
                print("(Click) Inspect submmsions ".ljust(80,"="))
                inspect(submission,methods=True,docs=True,value=True)
                print("Vars ".ljust(80, "*"))
                print(vars(submission))
                #print(submission)
            """
            submissions = reddit.info(submission_ids)  # Get submission objects
            count = sum(1 for _ in submissions)
            print(f"{count=}")
            for submission in submissions:
                print(submission)
                # print(f"Submission ID: {submission.id}")
                # print(f"Title: {submission.title}")
                # print(f"Author: {submission.author.name if submission.author else '[Deleted]'}")
                # print(f"Score: {submission.score}")
            """
    except Exception as e:
        print(f"An error occurred: {e}")


def submission_structure():
    pass

def menu_tests(test_reddit_info: bool, test_submission_structures: bool, submission_id: str = None):
    print(f"menu_tests() {test_reddit_info=}, {test_submission_structures=}, {submission_id=}")
    TEST_ID = submission_id
    print(TEST_ID)
    if test_reddit_info:
        test_info(submission_id)
    elif test_submission_structures:
        submission_structure()

