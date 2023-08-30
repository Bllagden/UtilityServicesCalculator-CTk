from typing import List, Tuple, Union, Optional

from src.model.sql import SQL

from .database import Database


class DatabaseOperations:
    """A high-level class for working with SQLite DB.
    Uses the functionality of the low-level class 'Database'.

    example of query and params:
    query = 'SELECT year FROM years WHERE house_id=?
    params = (5,)'
    """

    @staticmethod
    def first_connect():
        """The first connection to the DB while the program is running.
        Creates a DB if it does not already exist.
        Returns the path and name of the DB."""
        path, name = "", ""
        with Database() as db:
            path, name = db.path, db.name
        return path, name

    def get_db_tab_names(self) -> List[str]:
        """Gets the names of all tables from the DB."""
        query: str = SQL["SELECT_all_TABS"]
        tables: List[Tuple[str]] = self.single_query(query)

        result: List[str]
        result = [tuple_i[0] for tuple_i in tables]
        return result

    @staticmethod
    def single_query(query: str,
                     params: Union[None, Tuple, List[Tuple]] = None
                     ) -> Optional[List[Tuple]]:
        """params options:
        * None - query without parameters (execute method);
        * Tuple - query with parameters (execute method);
        * List[Tuple] - execute the query several times with different params,
        where each Tuple is a new parameter for the next query execution
        (executemany method).

        return options:
        * List[Tuple] - if SELECT query;
        * None - if not SELECT query;
        * [] - if the result of the SELECT query is empty."""
        with Database() as db:
            select_result = db.single_query(query, params)
        return select_result

    @staticmethod
    def transaction(queries: List[str],
                    params: List[Union[None, Tuple, List[Tuple]]]
                    ) -> Optional[List[List[Tuple]]]:
        """params options:
        the same as in single_query, only their >1, and they are in the list.

        return options:
        * List[List[Tuple] - if there are SELECT queries;
        * None - if there are no SELECT queries.

        len(queries) and len(params) must be equal."""
        with Database() as db:
            select_result = db.transaction(queries, params)
        return select_result
