import sqlite3
import json
import os
import sys
from enum import Enum

# from os.path import exists, expanduser
from pathlib import Path

# from rich import print as rprint
from rich import print
from rich.console import Console
from loguru import logger


def setup_logger():
    """
    Sets up the logger for the application.

    This function removes any default handlers from the logger and adds a new handler to log messages to a file with rotation. The logger is configured to log messages at the DEBUG level and includes backtrace and diagnose information. The logger is also bound to the module "Classy3".

    Returns:
        The logger object that has been set up.

    Available levels:
        TRACE, DEBUG, INFO, SUCCESS, WARNING, ERROR, CRITICAL
    """
    log_file = f'{GLOBS["PRG"]["PATHS"].get("LOGS_PATH")}/classy3.log'
    logger.remove()  # Remove any default handlers
    #logger.add.
    logger.add(f'{log_file}', rotation="1 MB",level="DEBUG", backtrace=True, diagnose=True)  # Log to a file with rotation
    log = logger.bind(module="Classy3")
    return log


# lg.remove(0)
# lg.add("logs/stats.log", rotation="100 KB", level="INFO", backtrace=True, diagnose=True)

GLOBS = {}
console = Console

MsgType = Enum("Type", ["MSG", "INFO", "WARNING", "ERROR", "CRITICAL"])


# Nessages defines here for convenience
def rich_msg(msg_type: Enum, message: str) -> None:
    if msg_type == MsgType.MSG:
        console.print(message, style="green bold")
    elif msg_type == MsgType.INFO:
        console.print(message, style="blue bold")
    elif msg_type == MsgType.WARNING:
        console.print(message, style="orange1 bold")
    elif msg_type == MsgType.ERROR:
        console.print(message, style="red1 bold")
    elif msg_type == MsgType.CRITICAL:
        console.print(message, style="red on hite bold")
    else:
        console.print(message, style="white")


def read_config(config_file: str) -> dict:
    """Extracts from settings.json the parts needed to run the program.

    Args:
        f_json (str): Filename of the JSON configuration file.

    Returns:
        dict: Dictionary with the necessary information extracted
        from the configuration file.
    """
    with open(config_file, mode="r", encoding="utf_8") as f:
        config = json.load(f)

        dataset_defaults = {}
        dataset_specific = {}

        if "DEFAULTS" not in config:
            raise ValueError("DEFAULTS not found in configuration file.")

        dataset_defaults = config["DEFAULTS"]
        for i in list(dataset_defaults.keys()):
            if i.lower().startswith("_note"):
                dataset_defaults.pop(i)
        # extract the dataset suffix, if it exists
        if "DATASET" in config:
            default_suffix = config["DATASET"]
            file_set = f"FILES{default_suffix}"
        else:
            file_set = "FILES"

        # raise an error if there was no dataset defined
        if file_set not in config:
            raise ValueError("Dataset not defined in config/config.json file.")

        # load into a dict the specifities of the selected dataset
        dataset_specific = config[file_set]
        # incorporate the specifc dataset data into the generic (default)
        dataset_defaults.update(dataset_specific)

        # Remove DATASET, DEFAULTS and FILES* from the tree as no more needed
        for key in ["DEFAULTS", "DATASET"]:
            if key in config:
                config.pop(key)
        for key in list(config.keys()):
            if key.startswith("FILES"):
                config.pop(key)

        ret_dic = {
            "DB": {
                "local": os.path.join(
                    dataset_defaults["db_path"], dataset_defaults["db_name"]
                ),
                "remote": dataset_defaults["dfr_db"],
                "local_bak_path": os.path.expanduser(
                    dataset_defaults["db_backup_path"]
                ),
                "remote_bak_path": os.path.expanduser(
                    dataset_defaults["dfr_backup_path"]
                ),
            }
        }
        # while we are here, let's check if the dbs exist
        # start with the remote file
        fil2chk = Path(ret_dic["DB"].get("remote"))
        if not fil2chk.is_file():
            raise ValueError("File DFR not found: impossible to continue.")

        fil2chk = Path(ret_dic["DB"].get("local"))

        # add whats left of the config file to the return dictionary
        for key, value in config.items():
            ret_dic[key] = value

        # Add what's left to ret_dic
        ret_dic.update(config)

        return ret_dic


def initialize_program(root_path):
    """
    Initialize the paths of the program.

    Parameters:
    root_path (str): The root path of the program.

    Returns:
    None.
    """
    program_paths = {
        "ROOT": root_path,
        "CONFIG_PATH": f"{root_path}/config",
        "LOGS_PATH": f"{root_path}/logs",
        "DATA_PATH": f"{root_path}/data",
        "PICKLES_PATH": f"{root_path}/pickles",
    }
    GLOBS["PRG"] = {"PATHS": program_paths}
    GLOBS['lg'] = setup_logger()
    config_path = program_paths.get("CONFIG_PATH")
    json_file = os.path.join(config_path, "config.json")
    config_data = read_config(json_file)

    for key, value in config_data.items():
        GLOBS[key] = value




def get_GLOBS():
    """
    Get the current GLOBS variable.

    Returns:
    dict: The GLOBS dictionary.
    """

    return GLOBS


def init(root_path: str):
    global GLOBS
    GLOBS = {"INITIALIZED": False}
    # GLOBS["MsgType"] = Enum("Type", ["MSG", "INFO", "WARNING", "ERROR", "CRITICAL"])
    # usage:
    # GLOBS['MsgType'].MSG returns Type.MSG
    # GLOBS['MsgType'].MSG.value returns
    program_paths = {
        "ROOT": root_path,
        "CONFIG_PATH": f"{root_path}/config",
        "LOGS_PATH": f"{root_path}/logs",
        "DATA_PATH": f"{root_path}/data",
        "PICKLES_PATH": f"{root_path}/pickles",
    }
    json_file = os.path.join(program_paths["CONFIG_PATH"], "config.json")
    GLOBS = read_config(json_file)
    GLOBS["PRG"] = {"PATHS": program_paths}
    GLOBS['lg'] = setup_logger()


fullmain = os.path.abspath(str(sys.modules[__name__].__file__))
# print(f"{fullmain=}")
main_path, _ = os.path.split(fullmain)
# print(f"{main_path=}")
init(main_path)

print(GLOBS)
exit(0)