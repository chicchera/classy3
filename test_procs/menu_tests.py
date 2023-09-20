import sys
import time
import praw
import prawcore
from app_logger import logger
import traceback  # Import the traceback module
from praw.models import MoreComments
from rich import print
from rich import inspect
from rich.console import Console
from settings import get_GLOBS
import db_utils.dbutils as dbu
from utils.misc import GracefulExiter
from scraper.redutils import createPRAW
# from test_procs.test_many_downloads import test_many_downloads

R_COMMENT = 't1_'
R_USER = 't2_'
# R_SUBMISSION = 't3_' # submissions don't need prefixes
R_MESSAGE = 't4_'
R_SUBREDDIT = 't5_'
R_AWARD = 't6_'

TEST_ID = '164e4z5'

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

def list_line(s):
    if s is None:
        return []
    return list(s)


def test_info(TEST_ID, num_comments, output_file):
    """
    Retrieves information from Reddit based on the given TEST_ID and saves it to the specified output file.

    Args:
        TEST_ID (int): The ID of the test to retrieve information for. If None, the ID of the latest submission will be used.
        num_comments (int): The number of comments to retrieve for each submission.
        output_file (str): The file path to save the retrieved information to.

    Returns:
        None
    """
    try:
        reddit = createPRAW()

        with dbu.DbsConnection() as conn:
            conn.row_factory = lambda cursor, row: row[0]
            c = conn.cursor()

            if TEST_ID is not None:
                submission_ids = [TEST_ID]
            else:
                submission_ids_query = (
                    'SELECT id_submission FROM submissions INDEXED BY submissions_created_utc_DESC_idx LIMIT 1;'
                )
                submission_ids = c.execute(submission_ids_query).fetchall()

            for id_sub in submission_ids:
                submission = reddit.submission(id=id_sub)
                print(submission.title)
                with open(output_file, "w") as f:
                    # print(vars(submission),file=f)
                    console = Console(force_terminal=False, file=f)

                    inspect(submission, methods=True, docs=True, value=True, console=console)

                    inspect(submission.author, methods=True, docs=True, value=True, console=console)

                    if num_comments > 0:
                        f.writelines(list_line("Comments ".ljust(80, "#") + "##"))
                        submission.comments.replace_more(limit=0)
                        all_comments = submission.comments.list()
                        sorted_comments = sorted(
                            all_comments, key=lambda comment: comment.created_utc, reverse=True
                        )

                        cnt = 0
                        for comment in sorted_comments:
                            cnt += 1
                            inspect(comment, methods=False, docs=True, value=True, console=console)
                            if cnt >= num_comments:
                                break
    except Exception as e:
        logger.error(f"An error occurred: {e}", file=sys.stderr)
        logger.debug("Stack trace:\n{}", traceback.format_exc())


def submission_structure():

    pass


# function to test many calls using error management
def many_calls():
    pass


def menu_tests(test_reddit_info: bool, test_submission_structures: bool, submission_id: str = None, num_comments: int = 0, output_file: str = None, long_test: bool = False):

    TEST_ID = submission_id
    print(TEST_ID)

    if test_reddit_info:
        test_info(submission_id, num_comments, output_file)
        return

    # if test_submission_structures:
    #     submission_structure()
    #     return

    # if long_test:
    #     test_many_downloads("asklatinamerica")

