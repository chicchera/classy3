import pandas as pd
import numpy as np
import inspect
import traceback
import time
import sqlite3
import demoji
import sys, traceback
import inspect
from app_logger import logger
from db_utils.dbutils import open_sqlite_database, attach_db
from db_utils.queries import clean_sql
from rich import print
from settings import get_globs_key
from txtutils.spellers import symspell_correct_return_errors
from legibility.legibilidad import *
from utils.txt_utils import validate_non_empty_string, no_html_emojis
from scraper.scraper_functions import update_subreddits



def check_df(df):
    callerframerecord = inspect.stack()[1]    # 0 represents this line
                                            # 1 represents line at caller
    frame = callerframerecord[0]
    info = inspect.getframeinfo(frame)
    print("v" * 80)
    print(f"File: {info.filename}")
    print(f"Function: {info.function} Line: {info.lineno}")
    print()
    print("HEAD")
    print(df.head())
    print()
    print("DESCRIBE")
    print(df.describe())
    print()
    print("COLUMNS")
    print(df.columns)
    print("^" * 80)


def save_ot_corrected(df, conn: sqlite3.Connection, kind='PTC'):
    # correct the original title

    df_work = df[['id_submission', 'old_title',  'corrected', 'errors', 'which_kind']].copy()
    df_work.dropna(inplace=True, subset=['old_title'])
    # df_work.apply(lambda row: symspell_correct_return_errors(row['old_title'],"corrected", "errors"), axis=1)
    df_work[['corrected', 'errors']] = df_work.apply(lambda row: symspell_correct_return_errors(row, 'old_title', 'corrected', 'errors'), axis=1)


    df_work['which_kind'] = kind

    df_save = df_work[['id_submission', 'corrected', 'which_kind']].copy()
    df_save.dropna(inplace=True, subset=['corrected'])
    new_names = {'corrected': 'content', 'which_kind': 'kind'}
    df_save.rename(columns=new_names, inplace=True)
    df_save.to_sql('txt_transforms', conn, if_exists='append', index=False)
    del df_save


    df_save = df_work[['id_submission', 'errors', 'which_kind']].copy()
    df_save.dropna(inplace=True, subset=['errors'])
    df_save['which_kind'] = 'PTM'
    new_names = {'errors': 'content', 'which_kind': 'kind'}
    df_save.rename(columns=new_names, inplace=True)
    df_save.to_sql('txt_transforms', conn, if_exists='append', index=False)
    del df_save

    return

    # df_txt[['title', 'misspells']] = df_txt.apply(lambda row: pd.Series(symspell_correct_return_errors(row['old_title'], keep_case=True)),axis=1)
    # df_txt.apply(lambda row: symspell_correct_return_errors(row['old_title'],"title", "misspells"), axis=1)
    df_work = df_work.apply(lambda row: symspell_correct_return_errors(row, 'old_title', 'corrected', 'errors'), axis=1)

    # print(df_txt.head())
    # print(df_txt.describe())
    # print(df_txt.columns)

    df_save = df_txt[['id_submission', 'content']].copy()
    df_save.dropna(inplace=True, subset=['content'])
    df_save['kind'] = kind
    df_save.to_sql('txt_transforms', conn, if_exists='append', index=False)

    df_txt.drop('content', axis=1, inplace=True)
    df_txt.rename(columns={'misspells': 'content'}, inplace=True)
    df_txt.dropna(inplace=True, subset=['content'])
    df_txt['kind'] = 'PTM'

    df_txt.to_sql('txt_transforms', conn, if_exists='append', index=False)

    # df_txt.drop(['content', 'old_title'], axis=1, inplace=True)
    # df_txt.rename(columns={'misspells': 'content'}, inplace=True)
    # df_txt.dropna(inplace=True, subset=['content'])
    # df_txt['kind'] = "PTM"
    # df_txt.to_sql('txt_transforms', conn, if_exists='append', index=False)

    # print(df_txt.head())
    # print(df_txt.describe())
    # print(df_txt.columns)
    # exit(0)
    # df_misspells = df_txt[['id_submission', 'misspells']].copy()
    # df_misspells.drop('content', axis=1, inplace=True)


    # df_txt.rename(columns={'misspells': 'content'}, inplace=True)
    # df_txt['kind'] = 'PTM'
    # df_txt.to_sql('txt_transforms', conn, if_exists='append', index=False)

    # df_txt['misspells'] = np.nan
    # df_txt['kind'] = kind

    # df_txt.apply(correct_original, args=("content", "misspells"), axis=1)
    # df_txt.dropna(inplace=True, subset=['content'])

    # df_result = df_txt.copy()
    # df_otc = df_result.drop('misspells', inplace=False)
    # df_otc.to_sql('txt_transforms', conn, if_exists='append', index=False)

    # df_otm = df_result.drop(['content', 'kind'], inplace=False)
    # df_otm.rename(columns={'misspells': 'content'}, inplace=True)
    # df_otm['kind'] = 'PTM'
    # df_otm.dropna(inplace=True, subset=['content'])
    # df_otm.to_sql('txt_transforms', conn, if_exists='append', index=False)


def save_original_title(df: pd.DataFrame, conn: sqlite3.Connection, kind: str = 'PT') -> None:
    """
    Save the original title of a DataFrame to a SQL table.
    Args:
        df (pd.DataFrame): The DataFrame containing the original title.
        kind (str, optional): The kind of title. Defaults to 'PT'.
    Returns:
        None
    """
    # print(df.head())
    # print(df.describe())
    # print(df.columns)
    # exit(0)

    df_txt = df[['id_submission', 'old_title']].copy()
    df_txt.rename(columns={'old_title': 'content'}, inplace=True)
    df_txt.dropna(inplace=True, subset=['content'])
    df_txt['kind'] = kind
    df_txt.to_sql('txt_transforms', conn, if_exists='append', index=False)

    # save_ot_corrected(df_txt, conn, kind='PTC')


def _save_original_body(df: pd.DataFrame, conn: sqlite3.Connection, kind: str = 'ON') -> None:
    pass

def save_ot_misspells(df, conn: sqlite3.Connection, kind='PTM'):
	pass


def save_ot_normalized(df, conn: sqlite3.Connection, kind='TN'):
	pass


def save_tn_no_stopwords(df, conn: sqlite3.Connection, kind='TNS'):
	pass


def save_tn_single_stopwords(df, conn: sqlite3.Connection, kind='TSS'):
	pass


def save_original_body(df, conn: sqlite3.Connection, kind='PB'):
    df_txt = df[['id_submission', 'old_body_html']].copy()
    df_txt.rename(columns={'old_body_html': 'content'}, inplace=True)
    df_txt.dropna(inplace=True, subset=['content'])
    # df_txt.content = df_txt.content.apply(no_html)
    df_txt['kind'] = kind
    df_txt.content = df_txt['content'].apply(no_html_emojis)
    # Filter out rows containing "view polo" in the 'content' column
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
            sr.id_subreddit,
            u.name AS redditor,
            p.title,
            p.self_text AS body,
            post.title AS old_title,
            post.text AS old_body,
            post.text_html AS old_body_html,
            Null as corrected,
            Null as errors,
            Null as which_kind,
            p.score,
            p.nsfw AS over_18,
            p.ama,
            p.serio,
            p.tonto_index,
            p.date_posted AS created_utc,
            COALESCE(u.id_red, '000') AS id_redditor
        FROM
            remote.posts AS p,
            subreddits AS sr,
            dfr.post AS post
        LEFT JOIN
            remote.objects AS u
            ON u.id_dfr = p.id_user AND u.kind = 'U'
        LEFT JOIN
            remote.objects AS s
            ON s.id_dfr = p.id_sub AND s.kind = 'S'
        WHERE
            s.name = sr.name
            AND post.reddit_id = p.id_red
            AND sr.id_subreddit IS NOT NULL
            AND post.reddit_id IS NOT NULL
            AND p.id_red NOT IN
            (SELECT id_submission FROM submissions)
            AND p.date_posted <= 1695553192
        LIMIT 10000;

    """

    conn = open_sqlite_database(new_db)
    # attach_db(conn, file=old_db, alias=old_alias)

    attach_db(conn,file=get_globs_key("DB,remote"),alias="remote")
    attach_db(conn,file=get_globs_key("DB,dfr_db"),alias="dfr")

    try:
        for df in pd.read_sql(qry_import_submissions, conn, chunksize=chunk):
            # Remove duplicates from the DataFrame based on the primary key or unique constraint columns
            df_nodups = df.drop_duplicates(subset=['id_submission']).copy()
            df_nodups['title'] = df_nodups['title'].apply(no_html_emojis)
            #df_nodups.loc[:, 'title'] = df_nodups['title'].apply(no_html_emojis)
            df_nodups['body'] = df_nodups['body'].apply(no_html_emojis)
            df_nodups["is_poll"] = df_nodups['old_body_html'].str.contains("View Poll", case=False)
            # Fill missing values in 'is_poll' with False
            df_nodups['is_poll'].fillna(False, inplace=True)
            # Set None to 'body', 'old_body', 'old_body_html' where 'is_poll' is True
            df_nodups.loc[df_nodups['is_poll'], ['body', 'old_body', 'old_body_html']] = None


            df_ot = df_nodups.drop(['title','body','old_title','old_body','old_body_html','corrected', 'errors', 'which_kind'],
                                   axis=1).copy()

            df_ot.to_sql('submissions', conn, if_exists='append', index=False)
            del df_ot

            df_work = df_nodups[['id_submission','title', 'body', 'old_title', 'old_body', 'old_body_html', 'corrected', 'errors', 'which_kind']].copy()

            save_original_title(df_work.copy(), conn)
            save_original_body(df_work.copy(), conn)
            save_ot_corrected(df_work.copy(), conn)

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

    #import_submissions(new_db , old_db=old_db, old_alias="remote", chunk=CHUNK, cut_date=cut_date)
    # def import_submissions(new_db=get_globs_key("DB,local"), old_db=get_globs_key("DB,remote"), old_alias=get_globs_key("DB,remote_alias"), dfr_db=get_globs_key("DB,dfr_db"),dfr=get_globs_key("DB,dfr_alias"),chunk=10000, cut_date=2):
    import_submissions(chunk=10)
