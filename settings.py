import sqlite3
import json

import errno
import os
import os.path
import sys
from enum import Enum

# from os.path import exists, expanduser
from pathlib import Path

# from rich import print as rprint
from rich import print
from rich.console import Console
from app_logger import logger


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
                "local": os.path.expanduser(os.path.join(
                    dataset_defaults["db_path"], dataset_defaults["db_name"]
                )),
                "remote": os.path.expanduser(dataset_defaults["remote_db"]),
                "local_bak_path": os.path.expanduser(
                    dataset_defaults["db_backup_path"]
                ),
                "remote_bak_path": os.path.expanduser(
                    dataset_defaults["remote_backup_path"]
                ),
                "dfr_db": os.path.expanduser(dataset_defaults["dfr_db"]),
                "dfr_alias": dataset_defaults["dfr_alias"],
            }
        }
        # while we are here, let's check if the dbs exist
        # start with the remote file
        # fil2chk = Path(ret_dic["DB"].get("remote"))
        # fil2chk = get_globs_key("DB,remote")
        # assert fil2chk, f"remote file ({fil2chk}) not found: \nimpossible to continue."
        # if not os.path.isfile(fil2chk):
        #     raise ValueError(f"File {fil2chk} not found: \nimpossible to continue.")

        # fil2chk = get_globs_key("DB,local")

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
        "ROOT": os.path.expanduser(root_path),
        "CONFIG_PATH": f"{root_path}/config",
        "LOGS_PATH": f"{root_path}/logs",
        "DATA_PATH": f"{root_path}/data",
        "PICKLES_PATH": f"{root_path}/pickles",
    }
    GLOBS["PRG"] = {"PATHS": program_paths}
    config_path = program_paths.get("CONFIG_PATH")
    json_file = os.path.join(config_path, "config.json")
    config_data = read_config(json_file)

    for key, value in config_data.items():
        GLOBS[key] = value



def get_GLOBS() -> any:
    """
    Get the current GLOBS variable.

    Returns:
    dict: The GLOBS dictionary.
    """

    return GLOBS

def get_globs_key(key=None, dictionary=None):
    """
    Returns the value associated with the specified key in the given dictionary.

    Parameters:
        key (str): The key to search for in the dictionary. If not provided, the entire dictionary is returned.
        dictionary (dict): The dictionary to search in. If not provided, the global variable 'GLOBS' is used.

    Returns:
        The value associated with the specified key in the dictionary. If the key is not found, None is returned.
    """
    if dictionary is None:
        dictionary = globals().get('GLOBS')
    if key is None:
        return dictionary

    assert "." not in key, "Full stops are not allowed in keys: replace with commas."

    keys = key.split(',')
    current_dict = dictionary

    for k in keys:
        if k in current_dict:
            current_dict = current_dict[k]
        else:
            return None

    return current_dict

def dictionary_path() -> str:
    which_to_select = get_globs_key("MISC,DICTIONARY,use")
    dics_available =get_globs_key("MISC,DICTIONARY,available")
    print(f"{which_to_select=}, {dics_available=}")

    try:
        dictionary = dics_available[which_to_select]
    except:
        raise "Dictionary not available."

    path = get_globs_key("PRG,PATHS,CONFIG_PATH")
    filename = os.path.expanduser(f"{path}/{dictionary}")
    if not os.path.isfile(filename):
        raise FileNotFoundError(
                errno.ENOENT, os.strerror(errno.ENOENT), filename)
    return filename

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
    if not "subreddits_data" in GLOBS:
        GLOBS["subreddits_data"] = None
    GLOBS["INITIALIZED"] = True
    # print(GLOBS)
    # exit(0)


fullmain = os.path.abspath(str(sys.modules[__name__].__file__))
# print(f"{fullmain=}")
main_path, _ = os.path.split(fullmain)
# print(f"{main_path=}")
init(main_path)


