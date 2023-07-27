from collections import namedtuple
from rich import print
from tqdm import tqdm
import db_utils.dbutils as dbu
from settings import get_GLOBS

GLOBS = get_GLOBS()

Subreddit = namedtuple(
    "Subreddit",
        [
            "id_subreddit",
            "name" ,
            "created_utc",
            "display_name",
            "description",
            "over_18",
            "last_submission_id",
            "last_submission_utc",
            "last_scraped_utc"
        ]
)
Submission = namedtuple(
    "Submission",
        ['id_submission',
        'id_redditor',
        'id_subreddit',
        'title',
        'selftext',
        'score',
        'over_18',
        'ama',
        'serio',
        'tonto_index',
        'created_utc',
        'num_comments'
    ]
)
Comment = namedtuple(
    "Comment",
    [
        "id",
        "author_id",
        "body_html",
        "score",
        "is_submitter",
        "parent_id",
        "submission_id",
        "date_posted"
    ]
)
Redditor = namedtuple(
    "Redditor",
    [
        'id_redditor',
        'name',
        'has_verified_mail',
        'created_utc',
        'bad_record'
    ]
)


def init_tables() -> list:
    """
    Inserts initial data into the tables 'redditors' and 'subreddits' if they do not already exist.
    This function uses a database connection to execute SQL queries and perform the necessary insertions.
    It first inserts a single row into the 'redditors' table with some predefined values.
    Then, it iterates over a list of subreddit names stored in the 'GLOBS' dictionary.
    For each subreddit name, it checks if it already exists in the 'subreddits' table.
    If the subreddit does not exist, it retrieves information about the subreddit from the Reddit API using the 'praw' library.
    Finally, it inserts a new row into the 'subreddits' table with the retrieved information.
    The function commits the changes to the database at the end.
    """
    with dbu.DbsConnection() as conn:
        c = conn.cursor()
        c.execute(
            "INSERT OR IGNORE INTO redditors (id_redditor, name, has_verified_mail, created_utc, bad_record) VALUES('000','nn',False,1689850792,True);"
        )

        for subreddit_name in GLOBS["SUBREDS"]:
            c.execute(
                f"SELECT name FROM subreddits WHERE name = '{subreddit_name}';"
            )
            result = c.fetchone()
            if result is None:
                subreddit = reddit.subreddit(subreddit_name)
                c.execute(
                    """
                    INSERT INTO subreddits(
                        id_subreddit,
                        name,
                        created_utc,
                        last_submission_id,
                        last_submission_utc,
                        last_scraped_utc,
                        description,
                        display_name)
                    VALUES
                        ( ?, ?, ?, '000', ?, ?, ?, ?);
                        """,
                    (
                        subreddit.id,
                        subreddit_name,
                        subreddit.created_utc,
                        subreddit.created_utc,
                        subreddit.created_utc,
                        subreddit.description,
                        subreddit.display_name,
                    ),
                )
        conn.commit()

        c = conn.cursor()
        c.execute("""SELECT * FROM subreddits;""")
        data = c.fetchall()
        return_table = []
        for row in data:
            record = {}
            for i, col in enumerate(c.description):
                record[col[0]] = row[i]
            return_table.append(record)

        # pbar = tqdm((range(len(return_table))), colour="magenta",leave=False, desc="Subreddits")
        # i = 0
        # for i in pbar:
        #     pbar.set_description(return_table[i]['display_name'])
        #     id_value = return_table[i]['id_subreddit']
        #     print(id_value)
        #     i = i + 1
        #     pbar.update(1)

        return return_table