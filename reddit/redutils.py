import datetime as dt
import string
import time
import praw
import prawcore
from prawcore.exceptions import NotFound, ResponseException, PrawcoreException

BASE36 = string.digits + string.ascii_lowercase


def base36encode(number: int) -> str:
    """
    Encodes a given number into base 36.

    :param number: The number to be encoded.
    :type number: int
    :raises TypeError: If the input number is not an integer.
    :return: The base 36 encoded string.
    :rtype: str
    """
    number = abs(number)
    if not isinstance(number, int):
        raise TypeError("number must be an integer")

    base36 = ""
    while number:
        number, i = divmod(number, 36)
        base36 = BASE36[i] + base36

    return base36


def base36decode(number: str) -> int:
    """
    Decodes a base36 number to its decimal representation.

    Parameters:
        number (str): The base36 number to be decoded.

    Returns:
        int: The decimal representation of the base36 number.
    """
    return int(number, 36)


def createPRAW(app="SilvioWcloud"):
    """
    Creates a PRAW (Python Reddit API Wrapper) object with the specified app name.
    apps are definied in the ~/.config/praw.ini file
    :param app: The name of the PRAW app to use. Defaults to "mix_scrape".
    :type app: str

    :return: A PRAW object if the app was successfully logged into, None otherwise.
    :rtype: praw.Reddit or None
    """
    try:
        retObj = praw.Reddit(app)
        print(f"Authenticated as {retObj.user.me()}")

        return retObj
    except (ResponseException, PrawcoreException) as error:
        handle_exception(app, error)
    except Exception as error:
        print(f"{app}: Exception error: {error}")
        # lg.critical(f"{app}: Exception error: {error}")


def handle_exception(app, error):
    err_msg = "Please check your praw.ini file."
    print(f"{app}: {error} {err_msg}")
    # lg.critical(f"{app}: {error} {err_msg}")
    raise error


def new_account_penalty(submission, redditor):
    """
    Returns a score based on the number of days between the creation of a
    `redditor` account and the posting of a `submission`.

    Parameters:
    submission (praw.models.Submission): The PRAW Submission object.
    redditor (praw.models.Redditor): The PRAW Redditor object.

    Returns:
    int: A score indicating the number of days between posting the submission
         and creating the redditor account.
    """
    # Convert the Unix timestamps to datetime objects
    user_created_utc = dt.datetime.fromtimestamp(int(redditor.user_created_utc))
    posted_utc = dt.datetime.fromtimestamp(int(submission.user_created_utc))

    # Calculate the number of days between the two datetime objects
    num_days = (user_created_utc - posted_utc).days

    # Determine the return value based on the number of days
    if abs(num_days) <= 1:
        return 5
    elif abs(num_days) <= 3:
        return 3
    elif abs(num_days) <= 5:
        return 1
    else:
        return 0
