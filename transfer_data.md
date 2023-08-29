"model=code-davinci-002,temperature=0.2". You are an expert Python programmer and your task is to write quality code.
In the following program, where should I initialize loguro logging?
How to ensure that the loggin covers all modules?
Where and when should I initialize the variable GLOBS? The variable GLOBS is a dictionary that is needed in many modules.

import datetime
import os
import sys

import db_utils.db_functions as dbf
import rich_click as click
import settings as settings
from settings import GLOBS

from classify.classy_procs import cl_classify
from loguru import logger
from rich import print as rprint
from scraper.reddit_scraper import scrape
from test_procs.menu_tests import menu_tests, submission_structure
from test_procs.test_many_downloads import test_many_downloads
from db_utils.db_structures import dump_tables_dict

#GLOBS = {}
click.rich_click.STYLE_OPTION_DEFAULT = "orange1 dim"
click.rich_click.USE_RICH_MARKUP = True

# global constants
LOG_FILE_RETENTION = 3
PRG_VERSION = "0.0.1"
PRG_NAME = "classy3"

def log_session_start(program_name=PRG_NAME, program_version=PRG_VERSION):
    logger.info(f"{program_name} {program_version} session started at {datetime.datetime.now()}")

def log_session_end(program_name=PRG_NAME, program_version=PRG_VERSION):
    logger.info(f"{program_name} {program_version} session ended at {datetime.datetime.now()}")

# Set up the logger configuration
logger_config = {
    "handlers": [
        {
            "sink": f"logs/{PRG_NAME}.log/",
            "level": "ERROR",  # Set the level to the desired level for your application
            "rotation": "100 KB",
            "backtrace": True,
            "diagnose": True,
        }
    ]
}

def setup_logger():
    logger.configure(**logger_config)

@click.group()
@click.version_option(PRG_VERSION, prog_name=PRG_NAME)
def cli():
    os.system("clear")

@click.option(
    "-A", "--backup-all", is_flag=True,
    help="Make a zipped backup of all the databases."
)
@click.option(
    "-r", "--backup-remote", is_flag=True,
    help="Make a zipped backup of the remote database (dfr)."
)
@click.option(
    "-l", "--backup-local", is_flag=True,
    help="Make a zipped backup of the local database."
)
@click.option(
    "-d", "--import-remote", is_flag=True,
    help="Import data from the remote database (dfr)."
)

@cli.command("databases")
def databases(
    backup_remote: bool, ackup_local: bool,
    backup_all: bool, import_remote: bool
):
    dbf.db_procs(backup_remote, backup_local, backup_all, import_remote)

@cli.command("classify")
@click.option(
    "-cat", "--categorize", s_flag=True,
    help="""Categorizes (classifies) again all the data.

    Better :point_right: [orange_red1 bold]make a backup[/] :point_left: before.
    [orange_red1](You will be prompted)[/]
    """
)
@click.option(
    "-tok", "--tokenize", is_flag=True,
    help="Recreate stopwords, stems and lemmas.",
)
@click.option(
    "-notok", "--remove-tokens", is_flag=True,
    help="Remove stopwords, stems and lemmas to save some space in the database."
)

def classify(cat: bool, tok: bool, notok: bool):

    rprint(f"Category: {cat}")
    rprint(f"Tokens: {tok}")
    rprint(f"Not tokens: {notok}")
    setup_logger()
    cl_classify(cat, tok, notok)

@cli.command("developer")
@click.option(
    "--drop-submissions", is_flag=True,
    help="Empties the submission files and all that is related to the classification. It will prompt to make a backup."
)
@click.option(
    "--drop-comments", is_flag=True,
    help="Empties the submission files and all that is related to the classification. NOT YET DEVELOPED. It will prompt to make a backup."
)
@click.option(
    "--drop-sort-base", is_flag=True,
    help="Empties containing original data without stopwords, lemmatized and stemmed. It will NOT prompt to make a backup."
)
@click.option(
    "--dump-schema", is_flag=True,
    help="Dumps to file the current database schema."
)
@click.option(
    "-dtd", "--dump-tables-dictionaries", is_flag=True, help="Dumps to screen and / or file the current database structures as dictionaries."
)
@click.option(
    "-of", "--output-file", default='./logs/structures_dump.txt',
    show_default=True, help="Where the output will be written."
)
@click.option(
    "--zap-database", is_flag=True,
    help="Zaps the current database schema and recreates using the same schema. NO DATA IS SAVED."
)
@click.option(
    "--create-db", is_flag=True, help="Create a new database. (NOT YET IMPLEMENTED)"
)
# @logger.catch
def developer(
    drop_submissions: bool,
    drop_comments: bool,
    drop_sort_base: bool,
    dump_schema: bool,
    zap_database: bool,
    create_db: bool,
    dump_tables_dictionaries: bool,
    output_file: str
):
    if dump_tables_dictionaries:
        dump_tables_dict(output_file)
        return
    dbf.developer_menu(
        drop_submissions, drop_comments, drop_sort_base, dump_schema, dump_tables_dictionaries, output_file, zap_database, create_db
    )

@click.command("tests")
@click.option(
    "-tri", "--test-reddit-info", is_flag=True,
    help="To test what is returned through the reddit.info API call."
)
@click.option(
    "-tss", "--test-submission-structures", is_flag=True,
    help="To test what is returned using the subreddits API call to get submissions and comments."
)
@click.option(
    "-sid", "--submission-id",
    help="A submission ID to test."
)
@click.option(
    "-nc", "--num-comments", default=0,
    help="Number of comments to retrieve from each submission."
)
@click.option(
    "-o", "--output-file", default="./logs/structures.txt",
    help="A file to save the output to."
)
@click.option(
    "-lt", "--long-test", is_flag=True, default=False,
    help="Used to test reddit limits."
)
def tests(
    test_reddit_info: bool,
    test_submission_structures: bool,
    submission_id: str,
    num_comments: int,
    output_file: str,
    long_test: bool
):
    """
    Various options for testing purposes.
    """
    print(f"call tests() {test_reddit_info=}, {test_submission_structures=}, {submission_id=}")
    setup_logger()  # Call the logger setup function
    logger.info("Starting 'tests' command")
    if long_test:
        test_many_downloads("asklatinamerica")
        return

    if test_submission_structures:
        submission_structure()
        return

    menu_tests(test_reddit_info, test_submission_structures, submission_id, num_comments, output_file, long_test)
    menu_tests(test_reddit_info, test_submission_structures, submission_id, num_comments, output_file, long_test)
    logger.info("'  tests' command completed")

@click.command("getred")

def getred():
    print("Getting data from Reddit")
    setup_logger()
    logger.info("Starting 'getred' command")
    scrape()
    logger.info("'getred' command completed")
    exit(0)


# ##############


cli.add_command(classify)
cli.add_command(databases)
cli.add_command(developer)
cli.add_command(getred)
cli.add_command(tests)

if __name__ == "__main__":
    global GLOBS
    cli()
