import os
import sqlite3
import sys
from contextlib import contextmanager
from logging import warning
from pathlib import Path

## Users should have a nojazz_conf.py file in the
## root of their project. This ensure that.

sys.path.insert(0, str(Path().resolve()))

try:
    from nojazz_conf import DB_PATH

except ModuleNotFoundError:
    warning("`nojazz_conf.py` not found. Creating file.")

    with open("nojazz_conf.py", "w") as f:
        f.write('DB_PATH = "."')

    from nojazz_conf import DB_PATH


@contextmanager
def connect_to_db(database: str, db_dir: str = None):
    """
    Allows use of a context manager for connecting to a
    database, executing a query, and commiting the changes

    e.g.
        with connect_to_db('test.db') as cursor:
            cursor.execute('some sql')

    Arguments:
        database: name of the database file
        db_dir: (optional) the path to the directory holding
                the databse file
    """
    if db_dir:
        path = str(Path(db_dir).resolve())
    else:
        path = str(Path(DB_PATH).resolve())

    conn = sqlite3.connect(path + database)
    cur = conn.cursor()
    yield cur
    conn.commit()
    conn.close()
