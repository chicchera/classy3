"model=code-davinci-002,temperature=0.2"
How can i get the logger to work in the following program? I should be enabled also in all the routines called
```


import datetime
import os
import db_utils.db_functions as dbf
import rich_click as click
import settings as settings
from classify.classy_procs import cl_classify
from loguru import logger
from rich import print as rprint
from scraper.reddit_scraper import scrape
from test_procs.menu_tests import menu_tests

click.rich_click.STYLE_OPTION_DEFAULT = "orange1 dim"
click.rich_click.USE_RICH_MARKUP = True

LOG_FILE_RETENTION = 3
PRG_VERSION = "0.0.1"
PRG_NAME = "classy3"

logger.add(f"./logs/{PRG_NAME}.log",
            level="ERROR",
            rotation="100 KB",
            backtrace=True,
            diagnose=True)

def log_session_start(program_name=PRG_NAME, program_version=PRG_VERSION):
    logger.info(f"{program_name} {program_version} session started at {datetime.datetime.now()}")

def log_session_end(program_name=PRG_NAME, program_version=PRG_VERSION):
    logger.info(f"{program_name} {program_version} session ended at {datetime.datetime.now()}")


@click.group()
def cli():
    os.system("clear")

@click.option(
    "-A",
    "--backup-all",
    is_flag=True,
    help="Make a zipped backup of all the databases."
)
@click.option(
    "-r",
    "--backup-remote",
    is_flag=True,
    help="Make a zipped backup of the remote database (dfr)."
)
@click.option(
    "-l",
    "--backup-local",
    is_flag=True,
    help="Make a zipped backup of the local database."
)
@click.option(
    "-d",
    "--import-remote",
    is_flag=True,
    help="Import data from the remote database (dfr)."
)

@cli.command("databases")
def databases(
    backup_remote: bool,
    backup_local: bool,
    backup_all: bool,
    import_remote: bool
):
    dbf.db_procs(backup_remote, backup_local, backup_all, import_remote)

@cli.command("classify")
@click.option(
    "--cat",
    "--categorize",
    is_flag=True,
    help="""Categorizes (classifies) again all the data.

    Better :point_right: [orange_red1 bold]make a backup[/] :point_left: before.
    [orange_red1](You will be prompted)[/]
    """,
)
@click.option(
    "--tok",
    "--tokenize",
    is_flag=True,
    help="Recreate stopwords, stems and lemmas.",
)
@click.option(
    "--notok",
    "--remove-tokens",
    is_flag=True,
    help="""Remove stopwords, stems and lemmas to save some space in the database.
    """
)
def classify(cat: bool, tok: bool, notok: bool):
    rprint(f"Category: {cat}")
    rprint(f"Tokens: {tok}")
    rprint(f"Not tokens: {notok}")

    cl_classify(cat, tok, notok)


@cli.command("developer")
@click.option(
    "--drop-submissions",
    is_flag=True,
    help="Empties the submission files and all that is related to the classification. It will prompt to make a backup."
)
@click.option(
    "--drop-comments",
    is_flag=True,
    help="Empties the submission files and all that is related to the classification. NOT YET DEVELOPED. It will prompt to make a backup."
)
@click.option(
    "--drop-sort-base",
    is_flag=True,
    help="Empties containing original data without stopwords."
)
@click.option(
    "--dump-schema",
    is_flag=True,
    help="Dumps to file the current database schema."
)
@click.option(
    "--zap-database",
    is_flag=True,
    help="Zaps the current database"
)
@click.option(
    "--create-db",
    is_flag=True,
    help="Create a new database. (NOT YET IMPLEMENTED)"
)
# @logger.catch
def developer(
    drop_submissions: bool,
    drop_comments: bool,
    drop_sort_base: bool,
    dump_schema: bool,
    zap_database: bool,
    create_db: bool
):
    """Various options for testing purposes."""
    rprint(f"{drop_submissions=}")
    rprint(f"{drop_comments=}")
    rprint(f"{drop_sort_base=}")
    rprint(f"{dump_schema=}")
    rprint(f"{zap_database=}")
    rprint(f"{create_db=}")
    rprint("Ciao developer CLI menu")

    dbf.developer_menu(

        drop_submissions, drop_comments, drop_sort_base, dump_schema, zap_database, create_db
    )


@click.command("tests")
@click.option(
    "--test-reddit-info",
    "--tri",
    is_flag=True,
    help="To test what is returned through the reddit.info API call."
)
@click.option(
    "--test-submission-structures",
    "--tss",
    is_flag=True,
    help="To test what is returned using the subreddits API call to get submissions and comments."
)
@click.option(
    "--submission-id",
    "--sid",
    is_flag=False, flag_value=None ,
    default=None,
    help="A submission ID to test."
)
def tests(test_reddit_info: bool, test_submission_structures: bool, submission_id: str):
    """Various options for testing purposes."""
    print(f"call tests() {test_reddit_info=}, {test_submission_structures=}, {submission_id=}")
    menu_tests(test_reddit_info, test_submission_structures, submission_id)

def getred():
    """
    Get all new data from Reddit
    """

    print("Getting data from Reddit")
    scrape()
    exit(0)

cli.add_command(getred)
cli.add_command(classify)
cli.add_command(databases)
cli.add_command(developer)
cli.add_command(getred)
cli.add_command(tests)

if __name__ == "__main__":
    log_session_start()
    cli()

```