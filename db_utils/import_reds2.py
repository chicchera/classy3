import inspect
import os
import sqlite3
import time
from collections import namedtuple
from contextlib import closing
from typing import List

import db_utils.dbutils as dbu
import pandas as pd
import sqlparse
import utils.txt_utils as tu
from db_utils.dbutils import open_sqlite_database, query_will_return
from db_utils.queries import clean_sql
# from db_utils.queries import que
from rich import print
from settings import get_GLOBS
from tqdm import tqdm
from utils.spelling import spell_text


def import_submissions(new_db, *, old_db, old_alias, chunk):
    qry_import_submissions = f"""
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
    {old_alias}.posts p
LEFT JOIN
    {old_alias}.objects u ON u.id_dfr = p.id_user AND u.kind = 'U'
LEFT JOIN
    {old_alias}.objects s ON s.id_dfr = p.id_sub AND s.kind = 'S';
"""
    conn = open_sqlite_database(new_db)
    dbu.attach_db(conn, file=old_db, alias=old_alias)

    for df in pd.read_sql(qry_import_submissions, conn, chunksize=chunk):
        df_copy = df.drop(['title','body'], axis=1)
        df_copy.to_sql('submissions', conn, if_exists='append', index=False)

        df_transforms1 = df[['id_submission', 'title']].copy()
        df_transforms1['kind'] = 'OT'
        df_transforms1.to_sql('txt_transforms', conn, if_exists='append', index=False)

        df_transforms2 = df[['id_submission', 'body']].copy()
        df_transforms2.dropna(inplace=True, subset=['body'])
        df_transforms2['kind'] = 'OT'
        df_transforms2.to_sql('txt_transforms', conn, if_exists='append', index=False)
    conn.close()
    return


def transfer_reds():
    global GLOBS
    CHUNK = GLOBS["MISC"].get("CHUNK") * 4

    old_db="/home/silvio/data/redsdb/stats.db"
    new_db=GLOBS["DB"].get("local")
    import_submissions(new_db , old_db=old_db, old_alias="reds", chunk=CHUNK)