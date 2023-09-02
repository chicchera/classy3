"""
A minimal routine to create the database without program dependencies
"""
import os
import sqlite3

from rich import print
from rich.panel import Panel
from rich.prompt import Confirm, Prompt
import db_utils.db_functions as dbf
from settings import get_GLOBS
GLOBS = get_GLOBS()


def create_local_db(always: bool) -> bool:
    """
    Creates a local database.

    Args:
        not_db (bool): Indicates whether to create the database or not. Default is True.

    Returns:
        bool: True if the local database is created successfully, False otherwise.

    Explanation:
        This code snippet defines a function create_local_db() that creates a local database. It takes an optional argument not_db which indicates whether to create the database or not. The function returns a boolean value indicating whether the local database was created successfully or not. The function performs the following steps:

        It obtains the path for the local database from a global variable GLOBS["DB"].get("local").
        If not_db is True, it checks if the local database file already exists. If it does, it prompts the user to confirm if they want to overwrite it. If the user confirms, it creates a backup of the existing database file, removes the file, and sets a variable is_localdb to False.
        It extracts the directory path from the local database file path and creates the directory if it doesn't already exist.

        It constructs the file path for a schema file (db_classy_schema.sql) by combining a global variable GLOBS["PRG"]["PATHS"].get("CONFIG_PATH") with the filename.

        If the schema file does not exist, it checks for an alternative file path (.db_classy_schema.sql) and if that file also doesn't exist, it prints an error message and exits.

        It establishes a connection to the local database using SQLite and creates a cursor object.
        It reads the contents of the schema file and executes the SQL script on the database using the cursor.
        It commits the changes to the database, closes the connection, and returns True to indicate successful creation of the local database.

        Note: Please note that the code snippets referenced (Confirm.ask(f"[yellow3]{LOCAL_DB}\n[orange3]already exists: [cyan bold]overwrite?"), dbf.ask_backup(), and Confirm.ask(f"[yellow3]{LOCAL_DB}\n[orange3]already exists: [cyan bold]overwrite?")) are not defined in the provided code snippet.
    """

    if not always:
        return True

    LOCAL_DB = GLOBS["DB"].get("local")
    if always:
        print(f"Creating {LOCAL_DB}")
        if os.path.isfile(LOCAL_DB):
            if Confirm.ask(f"[yellow3]{LOCAL_DB}\n[orange3]already exists: [cyan bold]overwrite?"):
                dbf.ask_backup()
                os.remove(LOCAL_DB)
                is_localdb = False
            else:
                return

    db_path, _ = os.path.split(LOCAL_DB)
    try:
        os.makedirs(db_path, exist_ok=True)
    except OSError:
        print(f"Could not create directory {db_path}")
        exit(0)

    schema_path = GLOBS["PRG"]["PATHS"].get("CONFIG_PATH")
    schema_file = os.path.join(schema_path, "db_classy_schema.sql")
    print(f"{schema_file=}")
    if not os.path.isfile(schema_file):
        print(f"first check {filename=}")
        filename = os.path.join(schema_path, ".db_classy_schema.sql")
        if not os.path.isfile(schema_file):
            print(f"[cyan bold]{schema_file=}[/] not found. [cyan bold]Impossible to create {filename}[/]")
            exit(0)

    conn = sqlite3.connect(LOCAL_DB)
    c = conn.cursor()
    with open(schema_file) as f:
        script = f.read()
    c.executescript(script)
    conn.commit()
    conn.close()
    return True
