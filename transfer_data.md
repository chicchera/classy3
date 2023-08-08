I would like to enclose the following code in a loguru logger so that all functions called from the click menu get also to be inside the logger. The logger should write to screen and file
```
@click.group()
def cli():
    """
    Creates a command line interface group using the `click` library. The group is decorated with the `logger.catch` decorator to handle any exceptions and log them. The function takes no parameters and returns nothing. It simply clears the terminal using the `os.system()` function.
    """
    os.system("clear")

@click.option(
    "-A",
    "--backup-all",
    is_flag=True,
    default=False,
    show_default=True,
    help="Make a zipped backup of all the databases."
)
@click.option(
    "-r",
    "--backup-remote",
    is_flag=True,
    default=False,
    show_default=False,
    help="Make a zipped backup of the remote database (dfr)."
)
@click.option(
    "-l",
    "--backup-local",
    is_flag=True,
    default=False,
    show_default=False,
    help="Make a zipped backup of the local database."
)
@click.option(
    "-d",
    "--import-remote",
    is_flag=True,
    default=False,
    show_default=False,
    help="Import data from the remote database (dfr)."
)


---