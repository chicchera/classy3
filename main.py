""""
Program to import data from Reddit and classify it
"""

# standard library imports
import os

import rich_click as click
from loguru import logger

# third-party importsimport os
# from rich.click import click
from rich import print as rprint

import db_utils.db_functions as dbf

# self imports
import settings as settings

from classify.classy_procs import cl_classify

from reddit.reddit import scrape

# click.rich_click.MAX_WIDTH = 100
click.rich_click.STYLE_OPTION_DEFAULT = "orange1 dim"
click.rich_click.USE_RICH_MARKUP = True

# global constants
LOG_FILE_RETENTION = 3
VERSION = "0.0.1"
NAME = "classyred"


@click.group()
@logger.catch
def cli():
    """
    Creates a command line interface group using the `click` library. The group is decorated with the `logger.catch` decorator to handle any exceptions and log them. The function takes no parameters and returns nothing. It simply clears the terminal using the `os.system()` function.
    """
    os.system("clear")


# @cli.command()
# @logger.catch
# @click.option(
#     "-u/-n",
#     "--users/--no-users",
#     is_flag=True,
#     default=True,
#     show_default=True,
#     help="Update also users (saves time later)",
# )
# @click.option(
#     "--chunk",
#     default=100_000,
#     show_default=True,
#     help="The number of records to process at the same time. A number too high can cause out of memory problems, while too low impacts performance.",
# )
# @logger.catch
# def get_data(users: bool, chunk: int) -> None:
#     """Imports data from the remote database, in this case dfr."""
#     dbf.import_data(chunk, users)


@click.option(
    "-A",
    "--backup-all/--no-backup-all",
    is_flag=True,
    default=False,
    show_default=True,
    help="Make a zipped backup of all the databases.",
)
@click.option(
    "-r",
    "--backup-remote",
    is_flag=True,
    default=False,
    show_default=False,
    help="Make a zipped backup of the remote database (dfr).",
)
@click.option(
    "-l",
    "--backup-local",
    is_flag=True,
    default=False,
    show_default=False,
    help="Make a zipped backup of the local database.",
)

@cli.command("databases")
@logger.catch
def databases(
    backup_remote: bool, backup_local: bool, backup_all: bool):
    """
    Create a database and set up backup routines.

    :param backup_remote: bool, whether to backup to remote server
    :param backup_local: bool, whether to backup locally
    :param backup_all: bool, whether to backup all databases
    :param create_db: bool, whether to create a new database
    """
    dbf.db_procs(backup_remote, backup_local, backup_all)


@cli.command("classify")
@click.option(
    "--cat",
    "--categorize",
    is_flag=True,
    default=False,
    show_default=True,
    help="""Categorizes (classifies) again all the data.

    Better :point_right: [orange_red1 bold]make a backup[/] :point_left: before.
    [orange_red1](You will be prompted)[/]
    """,
)
@click.option(
    "--tok",
    "--tokenize",
    is_flag=True,
    default=False,
    show_default=False,
    help="Recreate stopwords, stems and lemmas.",
)
@click.option(
    "--notok",
    "--remove-tokens",
    is_flag=True,
    default=False,
    show_default=True,
    help="""Remove stopwords, stems and lemmas to save some space in the database.

    This routine calls also VACUUM so better :point_right: [orange_red1]make a backup[/] :point_left: [orange_red1](You will be prompted later)[/].
    """,
)
@logger.catch
def classify(cat: bool, tok: bool, notok: bool):
    """classify alll the data (slow).

    Args:
        cat (bool): categorize the data
        tok (bool): tokenize the data
        notok (bool): not tokenize the data
    """
    rprint(f"Category: {cat}")
    rprint(f"Tokens: {tok}")
    rprint(f"Not tokens: {notok}")

    cl_classify(cat, tok, notok)


# ##############
@cli.command("developer")
@click.option(
    "--drop-submissions",
    is_flag=True,
    default=False,
    show_default=True,
    help="""Empties the submission files and all that is related to the classification.


    It will prompt to make a backup.
    """,
)
@click.option(
    "--drop-comments",
    is_flag=True,
    default=False,
    show_default=False,
    help="""Empties the submission files and all that is related to the classification. NOT YET DEVELOPED


    It will prompt to make a backup.
    """,
)
@click.option(
    "--drop-sort-base",
    is_flag=True,
    default=False,
    show_default=False,
    help="""Empties containing original data without stopwords, lemmatized and stemmed"


    It will NOT prompt to make a backup.
    """,
)
@click.option(
    "--dump-schema",
    is_flag=True,
    default=False,
    show_default=False,
    help="""Dumps to file the current database schema.
    """,
)
@click.option(
    "--zap-database",
    is_flag=True,
    default=False,
    show_default=False,
    help="""Zaps the current database schema and recreates using the same schema. NO DATA IS SAVED.
    """,
)
@click.option(
    "-c",
    "--create-db",
    is_flag=True,
    default=False,
    show_default=False,
    help="Create a new database. (NOT YET IMPLEMENTED)",
)
@logger.catch
def developer(
    drop_submissions: bool,
    drop_comments: bool,
    drop_sort_base: bool,
    dump_schema: bool,
    zap_database: bool,
    create_db: bool
):
    """Empties the submission files and all that is related to the classification."""
    dbf.developer_menu(
        drop_submissions, drop_comments, drop_sort_base, dump_schema, zap_database, create_db
    )


@click.command("getred")
# @click.option(
#     "-A",
#     "--get-all/--no-get-all",
#     is_flag=True,
#     default=False,
#     show_default=True,
#     help="gets the most recent data from Reddit.",
# )
# @click.option(
#     "--simulation",
#     is_flag=True,
#     default=False,
#     show_default=True,
#     help="gets the most recent data from Reddit.",
# )
def getred():
    """
    Get all new data from Reddit
    """

    print("Getting data from Reddit")
    scrape()
    exit(0)


# ##############


# cli.add_command(get_data)
cli.add_command(classify)
cli.add_command(databases)
cli.add_command(developer)
cli.add_command(getred)


if __name__ == "__main__":
    cli()
