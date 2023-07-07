# from enum import Enum
import os
import datetime
import inspect
import random
import string
import signal

from rich import print as rprint
from settings import get_GLOBS


# from rich import print as rprint
# from rich.prompt import Prompt

# import settings

GLOBS = get_GLOBS()


# see: https://stackoverflow.com/a/57649638/18511264
class GracefulExiter:
    def __init__(self):
        self.state = False
        signal.signal(signal.SIGINT, self.change_state)

    def change_state(self, signum, frame):
        print("exit flag set to True (repeat to exit now)")
        signal.signal(signal.SIGINT, signal.SIG_DFL)
        self.state = True

    def exit(self):
        return self.state


def uname(base_name: str, file_path: str, ext="zip") -> str:
    """Creates a unique name in "file_path"
       by taking the basename and adding todays date and the extension
       if the file already exists in the destination dictionary, then
       it adds to the basename also a consecutive number
       enclosed in parentheses

    Args:
        file_name (str): the base name of the file (or can be estracted from a full name))
        file_path (str): the destination path
        ext (str, optional): the extension of the new file. Defaults to 'zip'.
    Returns:
        The full name of a file that has the given base name and a date/time added to render the name unique in the given destination directory
    """
    if os.path.isfile(file_path):
        file_path = os.path.dirname(file_path)
    os.makedirs(file_path, exist_ok=True)
    # Just in case clean name & path
    base_name = os.path.splitext(os.path.basename(base_name))[0]
    # file_path = os.path.dirname(file_path)

    work_name = os.path.join(file_path, os.path.basename(base_name))
    dt = datetime.datetime.now().strftime("%y%m%d-%H%M%S_%f")
    return f"{work_name}-{dt}.{ext}"


def is_integer_num(n):
    if isinstance(n, int):
        return True
    if isinstance(n, float):
        return n.is_integer()
    return False


def short_dir(path: str) -> str:
    return path.replace(GLOBS["PRG"]["PATHS"].get("ROOT") + "/", "")


def autolog(message: str) -> None:
    """Prints module, function and line number for debug/tracing purposes
    Args:
        message (str): The message to be printed toghether with the function dada
    """
    # Get the previous frame in the stack, otherwise it would
    # be this function!!!
    func = inspect.currentframe().f_back.f_code
    # Dump the message + the name of this function to the log.
    rprint(
        f"[cyan bold]{message}: [/][salmon1]{short_dir(func.co_filename)}[/]/[bright_yellow]{func.co_name}:{func.co_firstlineno}[/]"
    )


def get_random_string(length=8) -> str:
    letters = string.ascii_lowercase
    result_str = "".join(random.choice(letters) for i in range(length))
    return result_str
