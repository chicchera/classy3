"""
A collection of function to deal with the databases
"""
import os
import sqlite3
import time
from contextlib import closing

import pandas as pd
import sqlparse

from rich import print as rprint
from rich.prompt import Confirm, Prompt
from tqdm import tqdm

from app_logger import logger
from db_utils.import_reds2 import transfer_reds
from settings import get_GLOBS
from db_utils.dbutils import zip_file
import db_utils.dbutils as dbu
import db_utils.queries as dbq
from db_utils.import_reds2 import transfer_reds
from utils.misc import autolog, is_integer_num
import utils.txt_utils as tu
from txtutils.spelling import spell_text

from settings import get_GLOBS
GLOBS = get_GLOBS()


# Optionally, you can log and handle null pointer references if applicable


tqdm.pandas()

# GLOBS = get_GLOBS()


# TODO: split this function in two: ask and make the backuo
# TODO: make two different function, one for each database.
# TODO: move this functions to dbutils
def ask_backup():
    assert False, "ask_backup"
    """Asks if a backup is required and then it makes one according to the answer"""
    file2zip = GLOBS["DB"].get("local")
    if os.path.isfile(file2zip) and Confirm.ask(
                f"001-[cyan bold]{file2zip}[/] was found\n[yellow3]Do you wish to make a backup?"
            ):
        backup_path = GLOBS["DB"].get("local_bak_path")
        zip_file(file2zip, backup_path)


def db_procs(
    backup_remote: bool, backup_local: bool, backup_all: bool,  import_old: bool
):
    """Work like a swith to perform different acctions
    Args:
        backup_remote (bool): backsup remote db (dfr)
        backup_local (bool): backups local db
        backup_all (bool): backup both databases
        create_the_db (bool): create a local database exnovo
    """
    if backup_local or backup_all:
        dbu.zip_local()
    elif backup_remote or backup_all:
        dbu.zip_remote()
    elif import_old:
        transfer_reds()
    else:
        assert False, "not implemented"


def import_submissions(chunk: int):
    """
    Imports from the remote databas all the new submissions

    Args:
        chunk (int): max records to be returned at the same time (to avoid out of memory errors)
    """
    with dbu.DbsConnection() as conn:
        # get the query to extract from dfr.post
        qry = dbq.qry_import_chunk_from_remote_post()
        # get the number of records the will return
        num_recs = dbu.query_will_return(qry, conn)

        blocks = int(num_recs / chunk)
        restant_recs = num_recs % chunk
        if restant_recs > 0:
            blocks += 1

        rprint(f"Importing {num_recs:,.0f} submissions")

        tqdm.pandas(desc="blocks", leave=False, colour="magenta")
        start = time.time()
        for _ in tqdm(range(blocks), desc="Submissions", colour="cyan"):
            # tqdm.write(recs)
            # print(qry_import_chunk_from_remote_post())
            df = pd.read_sql(qry, conn)

            # for _ in tqdm(range(df.shape[0]), colour="magenta", leave=False):
            df[["title", "body", "ama", "serio"]] = df.progress_apply(
                tu.clean_post_row, axis=1
            )
            df.to_sql("posts", conn, if_exists="append", index=False)
        end = time.time()
        rprint(f"[bright_yellow]Elapsed submissions imports time: {end - start}")


def import_comments(chunk: int):
    """
    Imports from the remote databas all the new comments

    Args:
        chunk (int): max records to be returned at thh same time (to avoid out of memory errors)
    """
    with dbu.DbsConnection() as conn:
        # get the query to extract from dfr.post
        qry = dbq.qry_import_chunk_from_remote_comment()
        # get the number of records the will return
        num_recs = dbu.query_will_return(qry, conn)

        blocks = int(num_recs / chunk)
        restant_recs = num_recs % chunk
        if restant_recs > 0:
            blocks += 1

        rprint(f"Importing {num_recs:,.0f} comments")

        tqdm.pandas(desc="blocks", leave=False, colour="magenta")
        for _ in tqdm(range(blocks), desc="Comments", colour="cyan"):
            # tqdm.write(recs)
            # print(qry_import_chunk_from_remote_post())
            df = pd.read_sql(qry, conn)

            # for _ in tqdm(range(df.shape[0]), colour="magenta", leave=False):
            df[["body"]] = df.progress_apply(tu.clean_comment_row, axis=1)
            df.to_sql("comments", conn, if_exists="append", index=False)


def complete_imports():
    """
    adds to the ids table the id of the submissione as as
    used by dfr and reddi, Thr idea es to use always the reddit
    one in case the downloader is changed
    """
    # get the queries list
    ql = dbq.after_import_queries()
    rprint()
    with dbu.DbsConnection() as conn:
        for _, named_query in enumerate(ql):
            # autolog(f"{named_query.des} - (query)")
            rprint(named_query.des)
            with closing(conn.cursor()) as cur:
                cur.execute(named_query.qry)


def import_data(chunk: int, users: bool):
    """Retrieves data from the remote db (submissions, comments & users)
        Calls import_submissions, import_comments and import_users
    Args:
        chunk (int): ow many records will be returned at thh same time (to avoid out of memory errors)
        users (bool): True if also users data is to be collected. I a slow procedure because Reddit API has to be queried and the limit is around one query per second.
    """

    chunk = chunk if is_integer_num(chunk) else GLOBS["MISC"].get("CHUNK")
    # INCOMPLETE
    import_submissions(chunk)
    import_comments(chunk)
    complete_imports()

    if users:
        pass


def developer_menu(
    drop_submissions: bool,
    drop_comments: bool,
    drop_sort_base: bool,
    dump_schema: bool,
    zap_database: bool,
    create_db: bool,
    initial_db_check: bool = False
):
    rprint(f"{drop_submissions=}")
    rprint(f"{drop_comments=}")
    rprint(f"{drop_sort_base=}")
    rprint(f"{dump_schema=}")
    rprint(f"{zap_database=}")
    rprint(f"{create_db=}")
    rprint(f"{initial_db_check=}")
    rprint("Hi from the developer menu")
    # assert False
    rprint("Hi after the assert")
    # exit(1)
    if drop_submissions:
        # ask_backup()
        dbu.zip_local()
        with dbu.DbsConnection() as conn:
            c = conn.cursor()
            c.execute("BEGIN TRANSACTION;")
            c.execute(
                "DELETE FROM cats_base WHERE rid_post IN (SELECT rid_post FROM posts);"
            )
            c.execute(
                "DELETE FROM category WHERE rid_post IN (SELECT rid_post FROM posts);"
            )
            c.execute("DELETE FROM posts;")
            c.execute("COMMIT;")
            c.execute("VACUUM;")
    elif drop_comments:
        rprint("TO BE DEVELOPED")

    elif drop_sort_base:
        with dbu.DbsConnection() as conn:
            c = conn.cursor()
            c.execute("BEGIN TRANSACTION;")
            c.execute("DELETE FROM sort_base;")
            c.execute("COMMIT;")
            c.execute("VACUUM;")

    elif dump_schema:
        with dbu.DbsConnection() as conn:
            c = conn.cursor()
            qry = dbq.qry_get_schema()

            c.execute(qry)
            records = c.fetchmany(100)
            for row in records:
                # rprint(f"{row['sql']};")
                qry = " ".join(row["sql"].split())
                print(
                    sqlparse.format(
                        qry + ";",
                        keywoard_kase="upper",
                        identifier_case="lower",
                        indent_tabs=False,
                        indent_width=2,
                        # reindent=True,
                        reindent_aligned=True,
                        use_space_around_operatos=False,
                        # comma_first=False,
                        wrap_after=30,
                    )
                )

    elif zap_database:
        with dbu.DbsConnection() as conn:
            c = conn.cursor()
            qry = (
                "SELECT sql FROM sqlite_schema WHERE sql IS NOT NULL ORDER BY rootpage;"
            )
            c.execute(qry)
            recs = c.fetchall()
            big_qry = ""
            for rec in recs:
                big_qry += rec["sql"] + ";\n"
            rprint(big_qry)

        # BUG: This backup is not working
        dbu.zip_local()
        LOCAL_DB = GLOBS["DB"].get("local")
        try:
            os.remove(LOCAL_DB)
        except OSError:
            pass

        with dbu.DbsConnection() as conn:
            c = conn.cursor()
            c.executescript(big_qry)
            c.execute(
                """INSERT INTO enum (tbl,des) VALUES
                            ('NS','NoSw_Dups'),
                            ('ND','NoSw_NoDups'),
                            ('LD','Lemma_Dups'),
                            ('SD','Stemma_Dups');
                      """
            )
            c.close()
    elif create_db:
        rprint("Prior db creation")

        dbu.create_database(ignore_if_exists=True)
    else:
        return

