import sys
import time
import praw
import prawcore
from loguru import logger

from praw.models import MoreComments
from rich import print
from rich import inspect
import db_utils.dbutils as dbu
from utils.misc import GracefulExiter
from scraper.redutils import createPRAW
from test_procs.test_many_downloads import test_many_downloads

R_COMMENT = 't1_'
R_USER = 't2_'
# R_SUBMISSION = 't3_' # submissions don't need prefixes
R_MESSAGE = 't4_'
R_SUBREDDIT = 't5_'
R_AWARD = 't6_'

TEST_ID = None

"""
SEE:
https://www.reddit.com/r/redditdev/comments/aoe4pk/praw_getting_multiple_submissions_using_by_id/

https://www.google.com/search?q=site%3Awww.reddit.com+%22praw%22+%22reddit.info%22+-pushshift
"""

# Configure the logger with the desired log levels and sinks
logger.remove()  # Remove any default sinks (stdout, etc.)

# Add a new sink for logging to the console
logger.add(sys.stdout, level="DEBUG")

# Set the logging level for specific modules
# log_modules = ("praw", "prawcore")
# for module in log_modules:
#     logger.bind(module=module).debug("Setting up logger for module: {module}")
#     logger.opt(bind=True, record=True).debug("Setting up logger for module: {module}")

def test_info(TEST_ID, num_comments, output_file):

    try:
        reddit = createPRAW()

        with dbu.DbsConnection() as conn:
            conn.row_factory = lambda cursor, row: row[0]
            c = conn.cursor()

            if TEST_ID is not None:
                submission_ids = [TEST_ID]
            else:
                submission_ids_query = 'SELECT id_submission FROM submissions INDEXED BY submissions_created_utc_DESC_idx LIMIT 1;'
                submission_ids = c.execute(submission_ids_query).fetchall()
            for id_sub in submission_ids:
                submission = reddit.submission(id=id_sub)
                with open(output_file, "w") as f:
                    if submission:
                        print(f"Submission Title: {submission.title}", file=f)
                        print(f"Submission URL: {submission.url}", file=f)
                        print(f"author full name: {submission.author_fullname}", file=f)
                    else:
                        print("Submission retrieval failed.",file=f )

                    print("(Click) Inspect submissions ".ljust(80, "="), file=f)
                    inspect(submission, methods=True, docs=True, value=True)
                    print("Vars ".ljust(80, "*"),file=f )
                    print(vars(submission),file=f)

                    assert num_comments > 0

                    if num_comments > 0:
                        print("Comments ".ljust(80, "#"),file=f)
                        submission.comments.replace_more(limit=0)
                        all_comments = submission.comments.list()
                        sorted_comments = sorted(all_comments, key=lambda comment: comment.created_utc, reverse=True)

                        cnt = 0
                        for comment in sorted_comments:

                            cnt += 1
                            print("Comment ".ljust(80, "#"),file=f)
                            print(vars(comment),file=f)
                            if cnt >= num_comments:
                                break





    except Exception as e:
        print(f"An error occurred: {e}")


def submission_structure():

    pass


# function to test many calls using error management
def many_calls():
    pass


def menu_tests(test_reddit_info: bool, test_submission_structures: bool, submission_id: str = None, num_comments: int = 0, output_file: str = None, long_test: bool = False):
    print(f"menu_tests() {test_reddit_info=}, {test_submission_structures=}, {submission_id=}")
    TEST_ID = submission_id
    print(TEST_ID)
    if test_reddit_info:
        test_info(submission_id, num_comments, output_file)
    elif test_submission_structures:
        submission_structure()
    elif long_test:
        test_many_downloads("asklatinamerica")

