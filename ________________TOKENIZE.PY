Sure! Here's an example of how you can achieve this using a `LEFT JOIN` and `INSERT` statement in SQL:

```sql
INSERT INTO sort_base (rid_post, rid_comment, qa, code, content)
SELECT rd.rid_post, rd.rid_comment, rd.qa, rd.code, your_function(rd.content)
FROM raw_data rd
LEFT JOIN sort_base sb ON sb.rid_post = rd.rid_post AND sb.rid_comment = rd.rid_comment AND sb.qa = rd.qa AND sb.code = rd.code
WHERE sb.rid_post IS NULL;
```

This will select all rows from the `raw_data` table that are not present in the `sort_base` table based on the unique key columns (`rid_post`, `rid_comment`, `qa`, and `code`). The `your_function(rd.content)` applies your function to the `content` column of the selected rows. Finally, the selected rows are inserted into the `sort_base` table.

I hope this helps! Let me know if you have any questions or need further assistance.

##########################################################################################################3

Here is an example of how you can achieve this using Python and the SQLite3 library:

```python
import sqlite3
import signal

def modify_content(content):
    # Your function to modify the content column goes here
    return modified_content

def handle_interrupt(signum, frame):
    # Handle the interrupt signal here
    print("Interrupted by user. Saving data and exiting.")
    conn.commit()
    conn.close()
    exit(0)

# Register the interrupt signal handler
signal.signal(signal.SIGINT, handle_interrupt)

# Connect to the database
conn = sqlite3.connect('your_database.db')
c = conn.cursor()

# Set the chunk size
chunk_size = 1000

# Read and process data in chunks
while True:
    c.execute('SELECT * FROM row_data LIMIT ?', (chunk_size,))
    rows = c.fetchall()
    if not rows:
        break
    for row in rows:
        rid_post, rid_comment, qa, code, content = row
        modified_content = modify_content(content)
        c.execute('INSERT INTO sort_base VALUES (?, ?, ?, ?, ?)', (rid_post, rid_comment, qa, code, modified_content))
    conn.commit()

# Close the database connection
conn.close()
```

This code reads data from the `row_data` table in chunks of size `chunk_size`, modifies the `content` column using the `modify_content` function, and appends the modified rows to the `sort_base` table. The user can interrupt the process at any time using Ctrl-C, which will trigger the `handle_interrupt` function to save the data and exit gracefully.

Is there anything else you need help with?

###########################################

Yes, there are several ways to speed up the above procedure:

1. **Use transactions**: Instead of committing the changes to the database after every chunk, you can wrap the entire loop in a single transaction by calling `conn.execute('BEGIN')` before the loop and `conn.commit()` after the loop. This can significantly reduce the overhead of writing to the database.

2. **Increase the chunk size**: You can experiment with different chunk sizes to find the optimal value for your system. A larger chunk size means fewer database queries, but it also means more memory usage.

3. **Optimize the `modify_content` function**: Make sure that your `modify_content` function is as fast as possible. You can use profiling tools such as `cProfile` to identify bottlenecks in your code.

4. **Use multiple threads or processes**: You can use multiple threads or processes to read and process data in parallel. This can speed up the procedure on multi-core systems.

Is there anything else you need help with?


############################ FROM text_tokenize.py ############################

def qry_create_raw_data():
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
            body AS content
        FROM
            comments c1
        UNION ALL
        SELECT
            c2.rid_post,
            c2.rid_comment,
            'NS' AS code,
            'A' AS qa,
            body AS content
        FROM
            comments c2
        UNION ALL
        SELECT
            c3.rid_post,
            c3.rid_comment,
            'LD' AS code,
            'A' AS qa,
            body AS content
        FROM
            comments c3
        UNION ALL
        SELECT
            c4.rid_post,
            c4.rid_comment,
            'SD' AS code,
            'A' AS qa,
            body AS content
        FROM
            comments c4;
    """
    )

def qry_get_posts_to_tokenize(chunk: int = GLOBS["MISC"].get("CHUNK")) -> str:
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
        WHERE sb.rid_post IS NULL;
                """
    )


