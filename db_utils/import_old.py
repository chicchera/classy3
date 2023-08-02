import os
import sqlite3
import time
from contextlib import closing

import utils.txt_utils as tu
from utils.spelling import spell_text

import db_utils.dbutils as dbu
from settings import get_GLOBS

from rich import print

OLD_DB="/home/silvio/dataredsdb/stats.db"
IMPORT_SUBMISSIONS_QRY = """
SELECT
    p.id_red AS id_submission,
    r.id_red AS id_redditor,
    s.id_red AS id_subreddit,
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
    objects r ON r.id_red = p.id_user AND r.kind = 'U'
LEFT JOIN
    objects s ON s.id_red = p.id_sub AND s.kind = 'S'
LIMIT 1000;"""

GLOBS = get_GLOBS()

column_mapping = {

}

def import_old():
    # use:
    # cursor = db.execute("SELECT customer FROM table")
    # for row in cursor:
    #           print row[0]
    # Connect to the source (old) and target databases
    source_conn = sqlite3.connect(OLD_DB)
    with dbu.DbsConnection() as conn:
        pass