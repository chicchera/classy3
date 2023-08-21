import praw
import time

"""
    This code defines a function scrape_reddit_data that takes two parameters: subreddit_name and num_posts. It uses the praw library to scrape data from Reddit.

    The function initializes a Reddit API client with the provided client ID, client secret, and user agent. It then specifies the subreddit to scrape and initializes an empty list to store the results.

    The function enters a loop to scrape posts from the subreddit until the desired number of posts (num_posts) is reached. It fetches a post from the subreddit, extracts the title, score, and URL, and appends them to the results list. If there are any exceptions raised during the scraping process, such as timeouts or 429 errors, it handles them by printing an error message, waiting for 5 seconds, and then retrying. If there are no more posts to fetch, the loop breaks and the function returns the results list.
"""
def scrape_reddit_data(subreddit_name, num_posts):
    """
    Scrapes Reddit data from a specified subreddit.

    Parameters:
        subreddit_name (str): The name of the subreddit to scrape.
        num_posts (int): The number of posts to scrape.

    Returns:
        list: A list of dictionaries containing the title, score, and URL of each scraped post.
    """
    # Initialize the Reddit API client
    reddit = praw.Reddit(
        client_id='YOUR_CLIENT_ID',
        client_secret='YOUR_CLIENT_SECRET',
        user_agent='YOUR_USER_AGENT'
    )

    # Specify the subreddit to scrape
    subreddit = reddit.subreddit(subreddit_name)

    # Initialize an empty list to store the results
    results = []

    # Counter to keep track of the number of posts scraped
    posts_scraped = 0

    # Set up a loop to keep scraping until we get the desired number of posts
    while posts_scraped < num_posts:
        try:
            # Fetch a post from the subreddit
            post = next(subreddit.new(limit=1))
            results.append({
                'title': post.title,
                'score': post.score,
                'url': post.url
            })
            posts_scraped += 1
        except praw.exceptions.PRAWException as e:
            # Handle PRAW exceptions (includes timeouts and 429 errors)
            print(f"Encountered PRAWException: {e}")
            print("Waiting for 5 seconds and then retrying...")
            time.sleep(5)
        except StopIteration:
            # If there are no more posts to fetch, break the loop
            break

    return results

if __name__ == "__main__":
    subreddit_name = "python"  # Replace with the subreddit you want to scrape
    num_posts_to_scrape = 10   # Replace with the number of posts you want to scrape

    scraped_data = scrape_reddit_data(subreddit_name, num_posts_to_scrape)

    # Print the scraped data
    for post_data in scraped_data:
        print(f"Title: {post_data['title']}")
        print(f"Score: {post_data['score']}")
        print(f"URL: {post_data['url']}")
        print("------------------------------")
############################################################################
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
def safe_reddit_request(func, *args, **kwargs):
    """
    Executes a given function with retry logic in case of Reddit API exceptions.

    This code snippet defines a function called safe_reddit_request that executes
    a given function with retry logic in case of Reddit API exceptions.
    It takes in a function, func, along with any additional arguments
    and keyword arguments that the function may need.

    The function attempts to execute the given function and returns its return value. If a praw.exceptions.RedditAPIException is raised, the function checks the type of error and waits for a certain amount of time before retrying. If any other exception is raised, the function breaks out of the loop and prints the exception message. If the maximum number of retry attempts is reached, the function raises an exception and exits.

    Parameters:
        func (function): The function to be executed.
        *args: Variable length argument list to be passed to the function.
        **kwargs: Arbitrary keyword arguments to be passed to the function.

    Returns:
        The return value of the executed function.

    Raises:
        praw.exceptions.RedditAPIException: If the Reddit API throws an exception.
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
    Scrape the top posts from a subreddit using the Reddit API.

    This code defines a function called scrape_subreddit_top_posts that uses the Reddit API to scrape the top posts from a given subreddit. It takes three arguments: reddit (an instance of the praw.Reddit class), subreddit_name (the name of the subreddit to scrape), and an optional argument limit (the number of top posts to scrape, defaults to 10). Inside the function, it retrieves the subreddit using reddit.subreddit(subreddit_name) and then iterates over the top posts using a for loop. It prints the title of each top post. The function doesn't return anything (None).

    Args:
        reddit (praw.Reddit): An instance of the praw.Reddit class.
        subreddit_name (str): The name of the subreddit to scrape.
        limit (int, optional): The number of top posts to scrape. Defaults to 10.

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
###############################################################################
"""
in python I have a string that contains the name of a function and some parameters, for example
"get_code('user','1243')"
Is it possible to execute it?

Yes, it is possible to execute a function whose name and parameters are stored in a string in Python. You can achieve this using the `eval()` function. However, you need to be cautious when using `eval()` as it can execute any arbitrary code and may pose security risks if the input is not properly sanitized.

Here's an example of how you can use `eval()` to execute the function from the given string:

```python
# Define the function
def get_code(param1, param2):
    return f"Code for {param1}: {param2}"

# Input string containing the function name and parameters
input_string = "get_code('user','1243')"

# Use eval() to execute the function
try:
    result = eval(input_string)
    print(result)
except Exception as e:
    print(f"Error: {e}")
```

Output:
```
Code for user: 1243
```

In this example, the `eval()` function takes the `input_string` and executes it as Python code. It calls the function `get_code` with the given parameters, and the result is stored in the `result` variable, which is then printed.

Keep in mind that using `eval()` with arbitrary user input can be dangerous, especially in situations where the input is not under your control. If you plan to use this approach, make sure to properly validate and sanitize the input to avoid potential security issues. In most cases, it is better to find alternative methods for executing functions based on user input to ensure a safer application.
"""

import sqlite3
from tqdm import tqdm

def transfer_data(source_db, target_db, table_name, batch_size=1000):
    source_conn = sqlite3.connect(source_db)
    target_conn = sqlite3.connect(target_db)

    source_cursor = source_conn.cursor()
    target_cursor = target_conn.cursor()

    try:
        # Count the total number of records in the source table
        source_cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
        total_records = source_cursor.fetchone()[0]

        # Prepare the insert query for the target table
        source_cursor.execute(f"PRAGMA table_info({table_name})")
        columns = ", ".join([col[1] for col in source_cursor.fetchall()])
        placeholders = ", ".join(["?" for _ in range(len(columns.split(', ')))])
        insert_query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"

        # Batch processing and data transfer with tqdm progress bar
        offset = 0
        with tqdm(total=total_records, desc='Data Transfer', unit='record') as pbar, target_conn:
            # Begin the transaction
            target_conn.execute("BEGIN")

            while offset < total_records:
                source_cursor.execute(f"SELECT * FROM {table_name} LIMIT {batch_size} OFFSET {offset}")
                data_to_transfer = source_cursor.fetchall()
                target_cursor.executemany(insert_query, data_to_transfer)
                offset += batch_size
                pbar.update(len(data_to_transfer))

            # Commit the transaction after successful data transfer
            target_conn.execute("COMMIT")
            print("Data transfer successful!")
    except Exception as e:
        # Rollback the transaction in case of any error
        target_conn.execute("ROLLBACK")
        print(f"Error transferring data: {e}")
    finally:
        source_conn.close()
        target_conn.close()

# Example usage with a batch size of 5000
transfer_data('path/to/source/database.db', 'path/to/target/database.db', 'your_table_name', batch_size=5000)

