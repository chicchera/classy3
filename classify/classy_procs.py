from rich.prompt import Confirm

import db_utils.dbutils as dbu
import db_utils.db_functions as dbf
import classify.text_tokenize as ttk
from settings import get_GLOBS

GLOBS = get_GLOBS()


def categorize(cat_all) -> bool:
    """Categorizes all submissions and comments

    Args:
        cat_all (boolean): whether to classify all the submisisons or only the new ones.
        This routine is called from two places: durinig records import only the new records are classifies otherwise, if called directly from the menu, all the existing classifications, tokens, lemmas and stems are deleted and the classificatioon is repeated for all the database..
        If the classification is complete also a backup is recoommended.
    Returns:
        bool: True if the operation was successful.
    """
    # if we are reclassifying the whole lot ask if a backup is needed
    if cat_all in locals():
        if cat_all:
            if Confirm.ask("Do you wish to make a backup?"):
                file2zip = GLOBS["DB"].get("local")
                backup_path = GLOBS["DB"].get("local_bak_path")
                dbf.zip_file(file2zip, backup_path)
    # we are going to classify the whole lot so delete all
    if cat_all:
        dbu.empty_table("category")
        dbu.empty_table("cats_base")


def cl_classify(cat: bool, tok: bool, notok: bool):
    """
    This is just the dispatcher for the menu options

    Args:
    cat (bool): True if the program has to  classify all the entries that are not already catgorized
    tok (bool): Tokenize all entries that are not already tokenize: Lemmas, stems & stopwords
    notok (bool): Use it before a complete reclassification to clear basic terms, such as lemmas, stems & stopwords or simply to  save space in the database
    """

    if cat:
        categorize(True)

    elif tok:
        ttk.tokenize_posts()
    elif notok:
        pass
    else:
        exit(1)
