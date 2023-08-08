import praw
import time

# Reddit API credentials
CLIENT_ID = 'YOUR_CLIENT_ID'
CLIENT_SECRET = 'YOUR_CLIENT_SECRET'
USER_AGENT = 'YOUR_USER_AGENT'

# Function to initialize the Reddit instance
def initialize_reddit():
    return praw.Reddit(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        user_agent=USER_AGENT,
    )

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

