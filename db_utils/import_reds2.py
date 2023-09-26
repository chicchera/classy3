import pandas as pd
import numpy as np
import inspect
import traceback
import time
import os.path
import sqlite3

from app_logger import logger
from db_utils.dbutils import open_sqlite_database, attach_db
from db_utils.queries import clean_sql
from rich import print
from settings import get_globs_key
from txtutils.spellers import correct_original
from legibility.legibilidad import *
from utils.txt_utils import validate_non_empty_string
from scraper.scraper_functions import update_subreddits

# def save_submmission_data(df: pd.DataFrame) -> None:
#     df_txt = df.copy()

#     pass



def save_ot_corrected(df, conn: sqlite3.Connection, kind='OTC'):
    df_txt = df.copy()
    df_txt['kind'] = kind
    # add a misspells column
    df_txt['misspells'] = np.nan
    print("DT_TXT")
    print(df_txt)
    # exit(0)
    df_txt.apply(correct_original("content","misspells"), axis=1)
    print(df_txt)
    content_def = result_df.drop('misspells', inplace=False)
    content_def.to_sql('txt_transforms', conn, if_exists='append', index=False)
    # Save also the mistakes
    content_def['kind'] = 'OTM'
    content_def.dropna(inplace=True, subset=['content'])
    content_def = result_df.drop('content', inplace=True)
    content_def.rename(columns={'misspells': 'content'}, inplace=True)
    content_def.dropna(inplace=True, subset=['content'])
    content

def save_original_title(df: pd.DataFrame, conn: sqlite3.Connection, kind: str = 'OT') -> None:
    """
    Save the original title of a DataFrame to a SQL table.
    Args:
        df (pd.DataFrame): The DataFrame containing the original title.
        kind (str, optional): The kind of title. Defaults to 'OT'.
    Returns:
        None
    """
    df_txt = df[['id_submission', 'title']].copy()
    df_txt.rename(columns={'title': 'content'}, inplace=True)
    df_txt.dropna(inplace=True, subset=['content'])
    df_txt['kind'] = kind
    df_txt.to_sql('txt_transforms', conn, if_exists='append', index=False)

    # save_ot_corrected(df_txt, conn, kind='OTC')


def _save_original_body(df: pd.DataFrame, conn: sqlite3.Connection, kind: str = 'ON') -> None:
    pass

def save_ot_misspells(df, conn: sqlite3.Connection, kind='OTM'):
	pass


def save_ot_normalized(df, conn: sqlite3.Connection, kind='TN'):
	pass


def save_tn_no_stopwords(df, conn: sqlite3.Connection, kind='TNS'):
	pass


def save_tn_single_stopwords(df, conn: sqlite3.Connection, kind='TSS'):
	pass


def save_original_body(df, conn: sqlite3.Connection, kind='OB'):
    df_txt = df[['id_submission', 'body']].copy()
    df_txt.rename(columns={'body': 'content'}, inplace=True)

    df_txt.dropna(inplace=True, subset=['content'])
    df_txt['kind'] = kind
    # Filter out rows containing "view polo" in the 'content' column
    if kind == 'OB':

        #filtered_df = df_txt[~df_txt['content'].str.contains("view polo")]
        #filtered_df['content'] = filtered_df['content'].apply(validate_non_empty_string)
        # df_txt['content'] = df_txt['content'].str.replace("view polo", None)
        df_txt['content'] = np.where(df_txt['content'].str.contains("view polo"), None, df_txt['content'])

        df_txt['content'] = df_txt['content'].apply(validate_non_empty_string)

        df_txt.dropna(inplace=True, subset=['content'])
        df_txt.to_sql('txt_transforms', conn, if_exists='append', index=False)



def save_ob_corrected(df, conn: sqlite3.Connection, kind='OBC'):
	pass


def save_ob_misspells(df, conn: sqlite3.Connection, kind='OBM'):
	pass


def save_ob_normalized(df, conn: sqlite3.Connection, kind='BN'):
	pass


def save_ob_no_stopwords(df, conn: sqlite3.Connection, kind='BNS'):
	pass


def save_bn_single_stopwords(df, conn: sqlite3.Connection, kind='BSS'):
	pass


def import_submissions(new_db=get_globs_key("DB,local"), old_db=get_globs_key("DB,remote"), old_alias=get_globs_key("DB,remote_alias"), dfr_db=get_globs_key("DB,dfr_db"),dfr=get_globs_key("DB,dfr_alias"),chunk=10000, cut_date=2):

    update_subreddits()

    chunk = 200_000

    qry_import_submissions = f"""
        SELECT
            p.id_red AS id_submission,
            COALESCE(u.id_red,'000') AS id_redditor,
            sr.id_subreddit,
            u.name as redditor,
            p.title,
            p.self_text as body,
            p.score,
            nsfw as over_18,
            ama,
            serio,
            tonto_index,
            date_posted as created_utc
        FROM
            {old_alias}.posts p,
            subreddits sr
        LEFT JOIN
            {old_alias}.objects u ON u.id_dfr = p.id_user AND u.kind = 'U'
        LEFT JOIN
            {old_alias}.objects s ON s.id_dfr = p.id_sub AND s.kind = 'S'
        WHERE s.name = sr.name
        AND id_subreddit IS NOT NULL
        AND p.id_red NOT IN
            (SELECT id_submission FROM submissions)
            AND p.date_posted <= {cut_date}
        LIMIT 10000;
    """

    conn = open_sqlite_database(new_db)
    # attach_db(conn, file=old_db, alias=old_alias)

    attach_db(conn,file=get_globs_key("DB,remote"),alias="remote")
    attach_db(conn,file=get_globs_key("DB,dfr_db"),alias="dfr")

    try:
        for df in pd.read_sql(qry_import_submissions, conn, chunksize=chunk):
            # Remove duplicates from the DataFrame based on the primary key or unique constraint columns
            df_nodups = df.drop_duplicates(subset=['id_submission'])

            # submissions identifiers & stats: title and body will go in txt_transforms
            df_ot = df_nodups.drop(['body','title'], axis=1)
            df_ot.to_sql('submissions', conn, if_exists='append', index=False)

            save_original_title(df_nodups.copy(), conn)
            save_original_body(df_nodups.copy(), conn)

    except Exception as e:
        print("An error occurred:")
        print(str(e))
        traceback.print_exc()
        frame = inspect.currentframe()
        if frame is not None:
            caller_frame = frame.f_back
            if caller_frame is not None:
                print("Caller function:", caller_frame.f_code.co_name)
                print("Caller line number:", caller_frame.f_lineno)
    conn.close()

def transfer_reds():

    # global GLOBS
    # GLOBS = get_GLOBS()
    # CHUNK = GLOBS["MISC"].get("CHUNK") * 4
    # skip_days = GLOBS["DOWNlOAD"].get("CUT_DATE")
    CHUNK = get_globs_key(key="MISC,CHUNK") * 4
    skip_days = get_globs_key(key="DOWNlOAD,CUT_DATE")
    cut_date = int(time.time()) - (skip_days * 86_400)

    print(f"{skip_days=}")
    print(f"{cut_date=}")
    old_db = get_globs_key(key="DB,remote")
    # new_db = GLOBS["DB"].get("local")
    new_db = get_globs_key(key="DB,local")

    import_submissions(new_db , old_db=old_db, old_alias="remote", chunk=CHUNK, cut_date=cut_date)
