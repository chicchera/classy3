"""
    Utilities related to the handling of the databases

    # DbsCursor has been replaced by

    # import sqlite3
    # from contextlib import closing

    # conn = sqlite3.connect(':memory:')

    # with closing(conn.cursor()) as cursor:
    #     cursor.execute(...)
"""
import os
import sqlite3
import zipfile

from loguru import logger
from rich import print as rprint
from rich.panel import Panel
from rich.prompt import Confirm, Prompt
from yaspin import yaspin

from settings import get_GLOBS
from utils.misc import uname
import db_utils.db_functions as dbf

GLOBS = get_GLOBS()

LOCAL_DB = GLOBS["DB"].get("local")
REMOTE_DB = GLOBS["DB"].get("remote")
ATTACH_DFR = f"ATTACH DATABASE '{REMOTE_DB}' AS dfr"


class DbsConnection:
    """
    Makes a connection to the local db
    and attaches the remote db

    return: Connection object or None
    """

    conn = None

    def __init__(self):
        """
        Create a new connection to the local database
        It also attaches the remote db

        Args:
            msg (str, optional): _description_. Defaults to "".
        """
        if self.conn is None:
            try:
                self.conn = sqlite3.connect(LOCAL_DB)
                # DbsConnection.cursor = DbsConnection.conn.cursor()
            except sqlite3.Error as e:
                print(f"""Error: Connection to {LOCAL_DB} not established {e}""")
            else:
                self.conn.execute("pragma foreign_keys=ON")
                self.conn.row_factory = sqlite3.Row
                self.conn.execute(ATTACH_DFR)

    def __enter__(self):
        """
        Returns:
             _type_: a connection to the local database
        """
        return self.conn

    def __exit__(self, exc_type, exc_value, exc_tb):
        """
        Commits and closes the connection

        Args:
            type (_type_): _description_
            value (_type_): _description_
            traceback (_type_): _description_
        """
        self.conn.commit()
        self.conn.close()


def query_will_return(qry: str, conn: sqlite3.Connection) -> int:
    """
    Returns the number of records that will return aquery
    so that progress bars make sense.
    Args:
        qry (str): the string that containes the query
        conn (conn): the connection to the database
    Returns:
        int: the number of records that will be returned.
        it discards the LIMI clause if it exists.
    """

    qry_count = qry.lower().partition("limit")[0]
    qry_count = "SELECT COUNT (*) FROM " + qry_count.partition("from")[2]
    return conn.execute(qry_count).fetchone()[0]


def empty_table(table_name: str, clear_counter: bool = True):
    with DbsConnection() as conn:
        c = conn.cursor()
        c.execute(f"DELETE FROM {table_name};")
        if clear_counter:
            c.execute(f"DELETE FROM sqlite_sequence WHERE name = '{table_name}';")
        c.execute("VACUUM")


def is_remote_db():
    if not os.path.isfile(REMOTE_DB):
        rprint(
            f"""Remote database [orange3]{REMOTE_DB}not found.[/]\n [cyan bold]
            Impossible to conrinue"""
        )
        exit(1)
        return False
    return True


def is_local_db():
    """Cheks for the existance of the local database
    Returns:
        boolean: True if the database exits, False otherwise.
    """
    return os.path.isfile(LOCAL_DB)


def ask_for_backup(msg: str) -> bool:
    """Asks if if a backup of the db database is desired. Defaulte to the local db
    Args:
    msg (str): the message to display (it will be in the format of "Do you wish to make a backup of {db}?")
    db (str): the full path and name of the databas. Defaults to the local database.
    Returns:
    bool: True if the backup is desired, False otherwise.
    """
    return Confirm.ask(msg)


def ask_for_local_backup() -> bool:
    """Ask if a backup is wanted for the local db

    Returns:
        bool: True if the backup is desired, False otherwise.
    """
    msg = f"Backup the [cyan bold]local[/] database [cyan bold]{LOCAL_DB}[/]?"
    return ask_for_backup(msg)


def ask_for_remote_backup() -> bool:
    """Ask if a backup is wanted for the remote db

    Returns:
        bool: True if the backup is desired, False otherwise.
    """
    msg = f"Backup the [cyan bold]local[/] database [cyan bold]{REMOTE_DB}[/]?"
    return ask_for_backup(msg)


# TODO: REMOVE THIS FUNCTION as it is not used anymore
# The function either  checkss or creates the database, BUT NOT BOTH
# FIXME: creation of the database cannot be done from with a checking function.
def check_dbs() -> bool:
    """Checks if bothe databases exist. If the remote doesn't it hals the program with a message. If the local doesnt, then it offers to create it.
    If the rmote database doesn't existe the programa aborts, without returning to this routine, otherwise if the local db doesn't exits triess to create and retuns the result.
    Returns:
        bool: True if both databases exist.
    """
    if not is_remote_db:
        return False
    if not is_local_db:
        dbf.createdb()


def zip_file(filename: str, zip_path: str):
    """
    Performs the backup (zip) of "filename" in the specified "path".
    If the directory doesn't exist, it will be created. The zipped file
    will have a unique name.

    Args:
        filename (str): the file to be backed up.
        zip_path (str): the destination path of the backup.
    """
    try:
        # Create the directory if it doesn't exist.
        os.makedirs(os.path.dirname(zip_path), exist_ok=True)

        # Get a unique name.
        newzip = uname(filename, zip_path)

        # Display a message.
        rprint(Panel(f"[yellow3]Backing up {filename}\n[cyan bold]to {newzip}"))

        # Create the zip file.
        with yaspin().white.bold.shark.on_blue as sp:
            sp.text = f"Creating {newzip}"
            fzip = zipfile.ZipFile(newzip, "w", zipfile.ZIP_DEFLATED)
            fzip.write(newzip)
            fzip.close()
    except Exception as e:
        # Log the error.
        logger.exception(e)
        raise


def zip_local():
    zip_file(LOCAL_DB, GLOBS["DB"].get("local_bak_path"))


def zip_remote():
    zip_file(REMOTE_DB, GLOBS["DB"].get("remote_bak_path"))

