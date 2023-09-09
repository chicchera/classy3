import os
import sqlite3
import time
from contextlib import closing
from collections import namedtuple
from typing import List
import sqlparse
import inspect

import pandas as pd
import utils.txt_utils as tu
from utils.spelling import spell_text

import db_utils.dbutils as dbu
from db_utils.dbutils import query_will_return,open_sqlite_database
from settings import get_GLOBS
from db_utils.queries import clean_sql
# from db_utils.queries import que
from rich import print
from tqdm import tqdm
# from main import GLOBS
# GLOBS = get_GLOBS()
# GLOBS = get_GLOBS
# CHUNK = GLOBS["MISC"].get("CHUNK") * 4



# old_conn = sqlite3.connect(old_db)

# new_conn = sqlite3.connect(new_db)


named_query = namedtuple("named_qry",
                         ["qry",
                         "destination_table"])

import_queries_list = []


def import_submissions(old_db, new_db, chunk):

    qry_import_submissions = """
SELECT
    p.id_red AS id_submission,
    COALESCE(u.id_red,'000') AS id_redditor,
    s.id_red AS id_subreddit,
	u.name as redditor,
	s.name as subreddit,
	p.title,
	p.self_text as body,
	p.score,
	nsfw as over_18,
	ama,
	serio,
	tonto_index,
	date_posted as created_utc
FROM
    posts p
LEFT JOIN
    objects u ON u.id_dfr = p.id_user AND u.kind = 'U'
LEFT JOIN
    objects s ON s.id_dfr = p.id_sub AND s.kind = 'S';
"""
    old_conn = open_sqlite_database(old_db)
    new_conn = open_sqlite_database(new_db)
    for df in pd.read_sql(qry_import_submissions, old_conn, chunksize=chunk):
        df_copy = df.drop(['title','body'], axis=1)
        df_copy.to_sql('submissions', new_conn, if_exists='append', index=False)

        df_transforms1 = df[['id_submission', 'title']].copy()
        df_transforms1['kind'] = 'OT'
        df_transforms1.to_sql('txt_transforms', new_conn, if_exists='append', index=False)

        df_transforms2 = df[['id_submission', 'body']].copy()
        df_transforms2.dropna(inplace=True, subset=['body'])
        df_transforms2['kind'] = 'OT'
        df_transforms2.to_sql('txt_transforms', new_conn, if_exists='append', index=False)

def transfer_reds():
    global GLOBS
    CHUNK = GLOBS["MISC"].get("CHUNK") * 4

    old_db="/home/silvio/data/redsdb/stats.db"
    new_db=GLOBS["DB"].get("local")
    import_submissions(old_db, new_db, CHUNK)