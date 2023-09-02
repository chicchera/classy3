"""
    A centrilized place to write all the needed queries,
    where possible.
"""
import sqlite3
from collections import namedtuple
import sqlparse
from main import GLOBS

from settings import get_GLOBS
GLOBS = get_GLOBS()

CHUNK = GLOBS["MISC"].get("CHUNK")

named_query = namedtuple("named_qry", "des, qry")


def query_will_return__(qry: str, conn: sqlite3.Connection) -> int:
    """Returns the number of records that will return aquery so tha progress bars make sense

    Args:
        qry (str): the string that containes the query
        conn (conn): the connection to the database


    Returns:
        int: the number of records that will be returned.
        it discards the LIMI clause if it exists.
    """

    qry_count = qry.lower().partition("limit")[0]
    qry_count = "SELECT COUNT (*) FROM " + qry_count.partition("from")[2]
    num_recs = conn.execute(qry_count).fetchone()[0]
    return num_recs


def clean_sql(qry: str) -> str:
    """returns a sql statement properly formatted
       by sqlparse to make sure the statements are valid, at least formally.
    Args:
        sql (str): the sql statement to format
    Returns:
        str: the original statement cleaned
    """
    return sqlparse.format(
        qry,
        keyword_case="upper",
        identifier_case="lower",
        strip_coments=True,
        reindent=True,
        indent_tabs=False,
        indent_width=2,
        use_space_around_operators=False,
        comma_first=False,
    )


def qry_get_schema() -> str:
    return """SELECT sql FROM sqlite_schema WHERE sql IS NOT NULL ORDER BY rootpage;"""


def qry_import_chunk_from_dfr_post(chunk: int = GLOBS["MISC"].get("CHUNK")) -> str:
    """
        returns a SQL statement to import records from
        DFR->post
        It checks that the new records aren't already imported
    Args:
        chunk (int): the max number of records to return
                     default is value stored in config.json
                     ["MISC"]["CHUNK"] = 50_000
    Returns:
        string : a clean SQL statement with the value of LIMIT
    """

    return clean_sql(
        f"""
        SELECT
            "id" AS "dfrid_post",
            "reddit_id" AS "rid_post",
            "author_id" AS "dfrid_author",
            "subreddit_id" AS "dfrid_sub",
            "title",
            "text_html" as "body",
            "strftime"('%s', "date_posted") as "date_posted",
            "score",
            "nsfw",
            FALSE AS "ama",
            FALSE AS "serio",
            0 AS "tonto_index"
        FROM
            dfr.post remote
            WHERE remote.id NOT IN
                (SELECT "dfrid_post" FROM posts)
        LIMIT {CHUNK};
    """
    )


def qry_import_chunk_from_dfr_comment(chunk: int = GLOBS["MISC"].get("CHUNK")) -> str:
    """
        returns a SQL statement to import records from
        DFR->comment
        It checks that the new records aren't already imported
    Args:
        chunk (int): the max number of records to return
                     default is value stored in config.json
                     ["MISC"]["CHUNK"] = 50_000
    Returns:
        string : a clean SQL statement with the value of LIMIT
    """
    return clean_sql(
        f"""
        SELECT
            "id" AS "dfrid_comment",
            "reddit_id" AS "rid_comment",
            "post_id" AS "dfrid_post",
            "parent_id" AS "dfrid_parent",
            "body_html" AS "body",
            "score",
            "strftime"('%s', "date_posted") AS "date_posted",
            "author_id" AS "dfrid_author",
            "" AS "rid_author",
            NULL AS "is_op"
        FROM
            dfr.comment remote
            WHERE remote.id NOT IN
                (SELECT "dfrid_comment" FROM comments)
        LIMIT {CHUNK}
        ;
    """
    )


def after_import_queries() -> list:
    """
    Returns a list of queries to be launched after
    importing submissions and comments.
    The purpose is to run them inside a loop using
    one single connection to save some time.

    Returns:
        list: a list of named queries

    """
    queries_list = []
    qry = """
        INSERT OR IGNORE INTO ids (tbl, id_dfr, id_red)
        SELECT
            "P" AS tbl,
            dfrid_post AS id_dfr,
            rid_post AS id_red
        FROM posts;"""
    queries_list.append(
        named_query(
            "Extract [cyan bold]ids[default] from [cyan bold]posts", clean_sql(qry)
        )
    )

    qry = """
    INSERT OR IGNORE INTO ids (tbl, id_dfr, id_red)
    SELECT
        "C" AS tbl,
        dfrid_comment AS id_dfr,
        rid_comment AS id_red
    FROM comments;"""
    queries_list.append(
        named_query(
            "Extract [cyan bold]ids[default] from [cyan bold]comments", clean_sql(qry)
        )
    )

    qry = """
    INSERT INTO objects (dfrid_object, name, tbl)
    SELECT
        "id" AS dfrid_object,
        "name",
        substr(object_type,1,1) AS tbl
    FROM dfr.reddit_object remote
    WHERE remote.id NOT IN
        (SELECT "dfrid_object" FROM objects);"""
    queries_list.append(
        named_query(
            "[cyan bold]Import users[default] from [cyan bold]remote.reddit_object",
            clean_sql(qry),
        )
    )

    qry = """
    UPDATE comments
        SET is_op = TRUE
        WHERE EXISTS
        (SELECT *
        FROM posts p
        WHERE comments.dfrid_post == p.dfrid_post
        AND   comments.dfrid_author == p.dfrid_author);"""
    queries_list.append(
        named_query(
            "Update [cyan bold]original posters (OP) [default]in [cyan bold][cyan bold]comments[default]",
            clean_sql(qry),
        )
    )

    qry = """
    UPDATE comments
    SET rid_post = (SELECT
        ids.id_red
        FROM ids
		WHERE ids.tbl = "C" AND
		ids.id_dfr = comments.dfrid_post);
        """
    queries_list.append(
        named_query(
            "Update [cyan bold]reddit post id [default]in [cyan bold]comments",
            clean_sql(qry),
        )
    )
    qry = """
    UPDATE comments
    SET rid_parent = (SELECT
        ids.id_red
        FROM ids
        WHERE comments.dfrid_parent IS NOT NULL
        AND ids.id_dfr = comments.dfrid_parent
        AND ids.tbl = "C"
        AND comments.dfrid_parent IS NOT NULL
        AND ids.id_dfr IS NOT NULL);
        """
    queries_list.append(
        named_query(
            "Update [cyan bold]reddit parent id [default]in [cyan bold]comments",
            clean_sql(qry),
        )
    )

    return queries_list


# #####################################################
#
# queries used for tokenization and classification
#
# #####################################################


def qry_create_raw_data():
    return clean_sql(
        """
        CREATE TEMPORARY TABLE raw_data AS
        SELECT
            p.rid_post,
            NULL AS rid_comment,
            '' AS code,
            'Q' AS qa,
            rtrim(coalesce(p.title || ' ', '') || coalesce(p.body, '')) AS content
        FROM
            posts p
        UNION ALL
        SELECT
            c.rid_post,
            c.rid_comment,
            '' AS code,
            'A' AS qa,
            c.body AS content
        FROM
            comments c;
        """
    )


def qry_create_raw_data__():
    return clean_sql(
        """
        CREATE TEMPORARY TABLE raw_data AS
        SELECT
            p1.rid_post,
            NULL AS rid_comment,
            'NS' AS code,
            'Q' AS qa,
            rtrim(coalesce(p1.title || ' ', '') || coalesce(p1.body, '')) AS content
        FROM
            posts p1
        UNION ALL
        SELECT
            p2.rid_post,
            NULL AS rid_comment,
            'ND' AS code,
            'Q' AS qa,
            rtrim(coalesce(p2.title || ' ', '') || coalesce(p2.body, '')) AS content
        FROM
            posts p2
        UNION ALL
        SELECT
            p3.rid_post,
            NULL AS rid_comment,
            'LD' AS code,
            'Q' AS qa,
            rtrim(coalesce(p3.title || ' ', '') || coalesce(p3.body, '')) AS content
        FROM
            posts p3
        UNION ALL
        SELECT
            p4.rid_post,
            NULL AS rid_comment,
            'SD' AS code,
            'Q' AS qa,
            rtrim(coalesce(p4.title || ' ', '') || coalesce(p4.body, '')) AS content
        FROM
            posts p4
        UNION ALL
        SELECT
            c1.rid_post,
            c1.rid_comment,
            'NS' AS code,
            'A' AS qa,
            c1.body AS content
        FROM
            comments c1
        UNION ALL
        SELECT
            c2.rid_post,
            c2.rid_comment,
            'ND' AS code,
            'A' AS qa,
            c2.body AS content
        FROM
            comments c2
        UNION ALL
        SELECT
            c3.rid_post,
            c3.rid_comment,
            'LD' AS code,
            'A' AS qa,
            c3.body AS content
        FROM
            comments c3
        UNION ALL
        SELECT
            c4.rid_post,
            c4.rid_comment,
            'SD' AS code,
            'A' AS qa,
            c4.body AS content
        FROM
            comments c4;
    """
    )


def qry_get_posts_to_tokenize(chunk: int = GLOBS["MISC"].get("CHUNK"), offset=0) -> str:
    return clean_sql(
        f"""
        SELECT
            rd.rid_post,
            rd.rid_comment,
            rd.qa,
            rd.code,
            rd.content
        FROM
            raw_data AS rd
        LEFT JOIN sort_base AS sb
            ON
                sb.rid_post = rd.rid_post
                AND
                sb.rid_comment = rd.rid_comment
                AND
                sb.qa = rd.qa
                AND
                sb.code = rd.code
        WHERE sb.rid_post IS NULL
        LIMIT {chunk} OFFSET {offset};
                """
    )


def qry_sel_users_to_update(
    chunk: int = GLOBS["MISC"].get("CHUNK") / 100, offset=0
) -> str:
    """
    Returns a SQL query to select the names of users to update.
    Chunkis is divided by 100 due to the time limit imposed by PRAW.
    """
    chunk_size = chunk / 100

    query = f"""
        SELECT
            name
        FROM
            users
        WHERE
            kind = 'U'
        AND bad_rec IS FALSE
        LIMIT {chunk_size}
        OFFSET {offset};
    """
    return clean_sql(query)


def qry_get_posts_to_tokenize__(
    chunk: int = GLOBS["MISC"].get("CHUNK"), offset=0
) -> str:
    return clean_sql(
        f"""
        SELECT
            rd.rid_post,
            rd.rid_comment,
            rd.qa,
            rd.code,
            rd.content
        FROM
            raw_data AS rd
        LEFT JOIN sort_base AS sb
            ON
                sb.rid_post = rd.rid_post
                AND
                sb.rid_comment = rd.rid_comment
                AND
                sb.qa = rd.qa
                AND
                sb.code = rd.code
        WHERE sb.rid_post IS NULL
        LIMIT {chunk} OFFSET {offset};
                """
    )


"""
Use the above query as:
    INSERT INTO sort_base (rid_post, rid_comment, qa, code, content)
    SELECT rd.rid_post, rd.rid_comment, rd.qa, rd.code, your_function(rd.content)
    FROM row_data rd
    LEFT JOIN sort_base sb ON sb.rid_post = rd.rid_post AND sb.rid_comment = rd.rid_comment AND sb.qa = rd.qa AND sb.code = rd.code
    WHERE sb.rid_post IS NULL;

    This will select all rows from the row_data table that are not present in the sort_base table based on the unique key columns (rid_post, rid_comment, qa, and code). The your_function(rd.content) applies your function to the content column of the selected rows. Finally, the selected rows are inserted into the sort_base table.
"""
