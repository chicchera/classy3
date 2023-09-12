import pandas as pd
import inspect
import traceback
from db_utils.dbutils import open_sqlite_database, attach_db
from db_utils.queries import clean_sql
from rich import print
from settings import get_GLOBS

def import_submissions(new_db, old_db, old_alias, chunk):

    chunk = 200_000

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
        {old_alias}.objects s ON s.id_dfr = p.id_sub AND s.kind = 'S'
    WHERE p.id_red NOT IN
        (SELECT id_submission FROM submissions);
    """

    conn = open_sqlite_database(new_db)
    attach_db(conn, file=old_db, alias=old_alias)
    try:
        for df in pd.read_sql(qry_import_submissions, conn, chunksize=chunk):
            # Remove duplicates from the DataFrame based on the primary key or unique constraint columns
            df_no_duplicates = df.drop_duplicates(subset=['id_submission'])

            df_ot = df_no_duplicates.drop(['body','title'], axis=1)
            print("OT")
            print(df_ot)
            df_ot.to_sql('submissions', conn, if_exists='append', index=False)

            df_transforms1 = df_no_duplicates[['id_submission', 'title']].copy()
            df_transforms1.rename(columns={'title': 'content'}, inplace=True)
            df_transforms1['kind'] = 'OT'
            df_transforms1.to_sql('txt_transforms', conn, if_exists='append', index=False)

            df_transforms2 = df_no_duplicates[['id_submission', 'body']].copy()
            df_transforms2.rename(columns={'body': 'content'}, inplace=True)
            df_transforms2.dropna(inplace=True, subset=['content'])
            df_transforms2['kind'] = 'OB'
            df_transforms2.to_sql('txt_transforms', conn, if_exists='append', index=False)
    except Exception as e:
        print("An error occurred:")
        print(str(e))
        traceback.print_exc()  # Print the traceback
        frame = inspect.currentframe()
        if frame is not None:
            caller_frame = frame.f_back
            if caller_frame is not None:
                print("Caller function:", caller_frame.f_code.co_name)
                print("Caller line number:", caller_frame.f_lineno)
    conn.close()

def transfer_reds():
    global GLOBS
    GLOBS = get_GLOBS()
    CHUNK = GLOBS["MISC"].get("CHUNK") * 4

    old_db = "/home/silvio/data/redsdb/stats.db"
    new_db = GLOBS["DB"].get("local")
    import_submissions(new_db , old_db=old_db, old_alias="reds", chunk=CHUNK)
