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
    u.id_red AS id_redditor,
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
    objects s ON s.id_dfr = p.id_sub AND s.kind = 'S'
LIMIT 100000;
"""

IMPORT_COMMENTS_QRY = """
SELECT
    c.reddit_id AS id_comment,
    post.id_red AS id_submission,
    parent.id_red AS id_parent,
    author.id_red AS id_redditor,
    c.body,
    c.is_op AS is_submitter,
    c.score,
    c.date_posted AS created_utc
FROM comments c
LEFT JOIN ids post ON post.id_dfr = c.post_id AND post.tbl = 'P'
LEFT JOIN ids parent ON c.parent_id = parent.id_dfr AND parent.tbl = 'C'
LEFT JOIN objects author ON author.id_dfr = c.author_id AND author.kind = 'U'
"""

IMPORT_SUBREDDITS_QRY = """
SELECT
    id_red AS id_subreddit,
    name,
    created AS created_utc
FROM objects
WHERE kind = 'S';
"""

IMPORT_USERS_QRY = """
SELECT
    id_red AS id_redditor,
    name AS redditor,
    created AS created_utc,
    has_mail AS has_verified_email,
    bad_rec AS bad_record
FROM objects
WHERE kind = 'U';
"""



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