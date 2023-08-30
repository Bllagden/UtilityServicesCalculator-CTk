import sqlite3 as sl
from typing import List, Tuple, Union, Optional

from .db_settings import DB_DEFAULT_PATH, DB_DEFAULT_NAME


class Database:
    """A low-level class for working with SQLite DB.
    Manages the connection to the DB using the context manager and
    executes SQL queries.

    Docstrings for queries methods are in the 'DatabaseOperations' class."""

    def __init__(self):
        self.path = DB_DEFAULT_PATH
        self.name = DB_DEFAULT_NAME

    def __enter__(self):
        try:
            self.conn = sl.connect(self.path + self.name)
        except sl.OperationalError:
            self.conn = sl.connect(self.name)
        self.curs = self.conn.cursor()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            self.conn.commit()
        else:
            self.conn.rollback()
            print(exc_type, exc_val, exc_tb, sep="\n")
        self.curs.close()
        self.conn.close()

    def single_query(self,
                     query: str,
                     params: Union[None, Tuple, List[Tuple]] = None
                     ) -> Optional[List[Tuple]]:

        if params is None:
            self.curs.execute(query)
        else:
            self._execute_with_params(query, params)

        if query.startswith("SELECT"): return self.curs.fetchall()

    def _execute_with_params(self,
                             query: str,
                             params: Union[Tuple, List[Tuple]]
                             ):
        """tuple - execute; list[tuple] - executemany"""

        if isinstance(params, tuple):
            self.curs.execute(query, params)

        elif isinstance(params, list):
            self.curs.executemany(query, params)

    def transaction(self,
                    queries: List[str],
                    params: List[Union[None, Tuple, List[Tuple]]]
                    ) -> Optional[List[List[Tuple]]]:

        if not (len(queries) == len(params)):
            raise ValueError("wrong len (queries != params)")

        self.curs.execute("BEGIN")
        select_result = []
        for i, v in enumerate(params):
            oper = self.single_query(queries[i], params[i])
            if queries[i].startswith("SELECT"): select_result.append(oper)

        if select_result: return select_result
