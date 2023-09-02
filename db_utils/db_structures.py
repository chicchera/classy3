import sqlite3
from rich import print as print
# import dbutils as dbu
from settings import get_GLOBS

from settings import get_GLOBS
GLOBS = get_GLOBS()


def create_table_dictionary(cursor, table_name):
    cursor.execute(f"PRAGMA table_info({table_name})")
    columns = [column[1] for column in cursor.fetchall()]
    table_dict = {column: None for column in columns}
    return table_dict

database_path = GLOBS["DB"].get("local")


def dump_tables_dict(output_file_path):
    if output_file_path is None:
        output_file_path = GLOBS['PRG']['PATHS'].get('LOGS_PATH') + '/structures_dump.txt'
    try:
        connection = sqlite3.connect(database_path)
        cursor = connection.cursor()

        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        table_names = [table[0] for table in cursor.fetchall()]

        table_dictionaries = {}

        for table_name in table_names:
            table_dict = create_table_dictionary(cursor, table_name)
            table_dictionaries[table_name] = table_dict
        # TODO: change the writes to print to file
        with open(output_file_path, 'w') as output_file:
            for table_name, table_dict in table_dictionaries.items():
                output_file.write(f"Structure for table '{table_name}':\n")
                output_file.write(str(table_dict) + '\n\n')
                print(f"Structure for table '{table_name}':")
                print(table_dict)
                print()

    except sqlite3.Error as e:
        print("SQLite error:", e)
    finally:
        if connection:
            connection.close()



