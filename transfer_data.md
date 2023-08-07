def cli():
    """
    Creates a command line interface group using the `click` library. The group is decorated with the `logger.catch` decorator to handle any exceptions and log them. The function takes no parameters and returns nothing. It simply clears the terminal using the `os.system()` function.
    """
    os.system("clear")



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
@click.option(
    "-d",
    "--import-remote",
    is_flag=True,
    default=False,
    show_default=False,
    help="Import data from the remote database (dfr).",
)

@cli.command("databases")
def databases(
    backup_remote: bool, backup_local: bool, backup_all: bool, import_remote: bool):
    """
    Create a database and set up backup routines.

    :param backup_remote: bool, whether to backup to remote server
    :param backup_local: bool, whether to backup locally
    :param backup_all: bool, whether to backup all databases
    :param create_db: bool, whether to create a new database
    """
    dbf.db_procs(backup_remote, backup_local, backup_all, import_remote)


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
    help="Empties the submission files and all that is related to the classification. It will prompt to make a backup."
)
@click.option(
    "--drop-comments",
    is_flag=True,
    default=False,
    show_default=False,
    help="Empties the submission files and all that is related to the classification. NOT YET DEVELOPED. It will prompt to make a backup."
)
@click.option(
    "--drop-sort-base",
    is_flag=True,
    default=False,
    show_default=False,
    help="Empties containing original data without stopwords, lemmatized and stemmed. It will NOT prompt to make a backup."
)
@click.option(
    "--dump-schema",
    is_flag=True,
    default=False,
    show_default=False,
    help="Dumps to file the current database schema."
)
@click.option(
    "--zap-database",
    is_flag=True,
    default=False,
    show_default=False,
    help="Zaps the current database schema and recreates using the same schema. NO DATA IS SAVED."
)
@click.option(
    "--create-db",
    is_flag=True,
    default=False,
    show_default=False,
    help="Create a new database. (NOT YET IMPLEMENTED)"
)
def developer(
    drop_submissions: bool,
    drop_comments: bool,
    drop_sort_base: bool,
    dump_schema: bool,
    zap_database: bool,
    create_db: bool
):



dbf.developer_menu(
    drop_submissions, drop_comments, drop_sort_base, dump_schema, zap_database, create_db
)
