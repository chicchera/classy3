import praw
import prawcore
from prawcore.exceptions import NotFound, ResponseException, PrawcoreException
import time
from settings import get_globs_key
from app_logger import logger

def create_praw(app=get_globs_key("REDDIT_PROFILE")):
    # ENV VARS HAVE BEEN MOVED TO ~/.config/praw.ini
    # see: https://bit.ly/3MWJSMa
    #
    # there are 5 configured apps:
    #   clistats, stupid, mines, fix_db and mix_scrape
    # the default one is "mix_scrape
    #
    # use print(reddit.user.me()) !!!!
    try:
        retObj = praw.Reddit(app)
    except ResponseException as error:
        logger.critical(f"{app}: ResponseException: {error}")
        quit()
    except PrawcoreException as error:
        print(f"{app}: PrawcoreException: {error}")
        logger.critical(f"{app}: PrawcoreException: {error}")
        quit()
    except Exception as error:
        print(f"{app}: Exception error: {error}")
        logger.critical(f"{app}: Exception: {error}")
        quit()
    logger.success(f"App: {app} "
                   f"Logged in as: {retObj.user.me()}")
    return retObj

# Function to handle Reddit API calls with retries on 429 errors and timeouts
"""
This code snippet defines a function called safe_reddit_request that takes another function func as an argument, along with any additional positional and keyword arguments. The function safe_reddit_request attempts to call func and return its result. If an exception of type praw.exceptions.RedditAPIException is raised and the error type is either 'ratelimit' or 'timeout', the function waits for a certain amount of time and then retries the function call. If any other exception is raised, the function prints an error message and breaks out of the loop. If the maximum number of retry attempts is reached, the function raises an exception.
"""
def safe_reddit_request(func, *args, **kwargs):
    """
    Executes a given function with the provided arguments and keyword arguments, while handling exceptions and retrying if necessary.

    Parameters:
        func (function): The function to be executed.
        *args: Variable length argument list to be passed to the function.
        **kwargs: Keyword arguments to be passed to the function.

    Returns:
        The return value of the executed function.

    Raises:
        praw.exceptions.RedditAPIException: If a Reddit API exception occurs.
        Exception: If the maximum number of retry attempts is reached.
    """
    retry_attempts = 5
    for attempt in range(retry_attempts):
        try:
            return func(*args, **kwargs)
        except praw.exceptions.RedditAPIException as e:
            if e.error_type == 'ratelimit' or e.error_type == 'timeout':
                wait_time = int(e.message.split(' ')[-2]) + 1
                print(f"Retrying in {wait_time} seconds...")
                time.sleep(wait_time)
            else:
                print(f"Other Reddit API exception: {e}")
                break
        except Exception as e:
            print(f"Other exception: {e}")
            break
    else:
        print("Max retry attempts reached, exiting.")
        raise Exception("Max retry attempts reached.")


def get_subreddit(subreddit_name, reddit):
    return reddit.subreddit(subreddit_name)

#subreddit_instance = safe_reddit_request(get_subreddit, subreddit_name, reddit)

# Example function to scrape a subreddit's top posts
def scrape_subreddit_top_posts(reddit, subreddit_name, limit=10):
    """
    Scrape the top posts from a specified subreddit.

    Args:
        reddit (praw.Reddit): An instance of the Reddit class.
        subreddit_name (str): The name of the subreddit to scrape.
        limit (int, optional): The maximum number of posts to scrape. Defaults to 10.

    Returns:
        None
    """
    subreddit = reddit.subreddit(subreddit_name)
    for submission in subreddit.top(limit=limit):
        print(submission.title)

if __name__ == "__main__":
    reddit = initialize_reddit()

    subreddit_name = "python"  # Replace with the subreddit you want to scrape
    posts_limit = 5  # Number of top posts to retrieve

    try:
        safe_reddit_request(scrape_subreddit_top_posts, reddit, subreddit_name, posts_limit)
    except Exception as e:
        print(f"Error: {e}")

