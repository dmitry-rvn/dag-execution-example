import sqlite3
import math
import os
from typing import Optional, Any

from dotenv import load_dotenv
import pandas as pd


load_dotenv()

DATABASE = os.getenv('DATABASE_FILEPATH')
DB_DATE_FORMAT = '%Y-%m-%d'


def _add_functions_to_sqlite(con: sqlite3.Connection):
    con.create_function('POWER', 2, lambda base, exponent: base ** exponent)
    con.create_function('LN', 1, lambda x: math.log(x))
    con.create_function('EXP', 1, lambda x: math.exp(x))


def execute_query(sql: str, as_script: bool = False) -> Optional[list[tuple[Any]]]:
    with sqlite3.connect(DATABASE) as con:
        _add_functions_to_sqlite(con)
        cur = con.cursor()
        if as_script:
            cur.executescript(sql)
        else:
            cur.execute(sql)
        con.commit()
        return cur.fetchall()


def fetch_data() -> pd.DataFrame:
    with sqlite3.connect(DATABASE) as con:
        return pd.read_sql_query('SELECT * FROM rates', con)
