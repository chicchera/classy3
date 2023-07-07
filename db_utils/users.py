# Importing datetime modules
import datetime as dt
from datetime import timezone

# Importing time module
import time

# Importing traceback module
import traceback

# Importing requests.exceptions module for HTTPError
from requests.exceptions import HTTPError

# Importing rich module and aliasing print as rprint
from rich import print as rprint

# Importing tqdm module
from tqdm import tqdm

# Importing prawcore module and exceptions
import prawcore
from prawcore.exceptions import NotFound, ResponseException, PrawcoreException

# Importing custom modules
from utils.misc import GracefulExiter
import db_utils.queries as dbq
import db_utils.dbutils as dbu

# Importing settings module
from settings import get_GLOBS

GLOBS = get_GLOBS()

WAIT_TIME = 1  # seconds

reddit = red.createPRAW("SilvioWcloud")


def get_redditor_data(reddit, username):
    try:
        redditor = reddit.redditor(username)
        data = {
            "id": redditor.id,
            "has_verified_email": redditor.has_verified_email,
            "created_utc": redditor.created_utc,
            "is_suspended": redditor.is_suspended,
        }
        return data
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None


# QRY_SEL = dbq.qry_sel_users_to_update()
QRY_COUNT = dbu.query_will_return


def valid_user(username):
    """
    Return False if user is banned or deleted.
    """

    try:
        redditor = reddit.redditor(username)
        redditor.id  # Check if redditor has an id
    except (AttributeError, prawcore.exceptions.NotFound, HTTPError):
        return False, None

    try:
        redditor.unblock()
    except PrawcoreException:
        return False, None

    return True, redditor


def update_users(chunk_size: int) -> None:
    """
    Imports new submissions from the remote database.
    This function retrieves the data in chunks to avoid memory errors.
    Args:
        chunk_size (int): max records to be returned at the same time
    """
    if chunk_size is None:
        chunk_size = GLOBS["MISC"].get("CHUNK") / 100

    qry = dbq.qry_sel_users_to_update(chunk_size, 0)
    with dbu.DbsConnection() as conn:
        num_recs = dbu.query_will_return(qry, conn)
        blocks = int(num_recs / chunk_size)
        if num_recs % chunk_size > 0:
            blocks += 1

        current_offset = 0

        rprint()
        rprint("[Cyan]Press [bright_yellow]Ctrl-C[Cyan] to break this routine.")
        rprint(f"Completing user data of {num_recs:,.0f} records")

        exit_flag = GracefulExiter()

        start = time.time()

        for _ in tqdm(
            range(blocks), desc="Ctrl-c to suspend", colour="cyan", leave=False
        ):
            current_offset = 0
            c = conn.cursor()
            c.execute("BEGIN TRANSACTION;")
            c.execute(dbq.qry_sel_users_to_update(chunk_size, current_offset))
            rows = c.fetchall()
            if not rows:
                break
            current_offset += chunk_size
            conn.execute("BEGIN TRANSACTION;")
            with tqdm(
                rows, desc="Users data extraction", colour="cyan", leave=False
            ) as pbar:
                for row in rows:
                    c.execute(dbq.qry_update_user(row))

            conn.execute("COMMIT;")
