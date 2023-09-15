import sqlite3
import contextlib

from rich import print as rprint
from settings import get_GLOBS


# rprint(GLOBS)
# GLOBS = get_GLOBS()

LOCAL_DB = GLOBS["DB"].get("local")
REMOTE_DB = GLOBS["DB"].get("remote")
ATTACH_DFR = f"ATTACH DATABASE '{REMOTE_DB}' AS dfr"


class DbsConnection:
    """returns a connection on stats.db wir dfr.db attached
    return: Connection object or None
    """

    def __init__(self):
        self._conn = self.create_conn()
        if self._conn is not None:
            self._conn.execute('pragma foreign_keys=ON')
            self._conn.row_factory = sqlite3.Row
            self._conn.execute(ATTACH_DFR)

    def __enter__(self):
        return self._conn

    def __exit__(self, type, value, traceback):
        self._conn.commit()
        self._conn.close()

    def create_conn(self):
        conn = None
        try:
            # conn = sqlite3.connect(GLOBS.localdb.get('name'))
            conn = sqlite3.connect(LOCAL_DB)
        except Error as e:
            print(e)
        return conn

class DbsCursor:
    """returns a cursor on the passed connection.
    """

    def __init__(self, _conn):
        self._conn = self.create_conn()
        if self._conn is not None:
            self._conn.execute('pragma foreign_keys=ON')
            self._conn.row_factory = sqlite3.Row
            self._conn.execute(ATTACH_DFR)

    def __enter__(self):
        return self.conn.

    def __exit__(self, type, value, traceback):
        self._conn.commit()
        self._conn.close()

    def create_conn(self):
        conn = None
        try:
            # conn = sqlite3.connect(GLOBS.localdb.get('name'))
            conn = sqlite3.connect(LOCAL_DB)
        except Error as e:
            print(e)
        return conn
