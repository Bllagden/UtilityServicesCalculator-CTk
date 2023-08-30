from typing import List, Tuple, Union

from src.model.sql import SQL


class SQLBuilderDBFirstConfigure:
    """The class builds a SQL query for a transaction that creates base tables
    in a new DB."""

    def __init__(self):
        self._queries: List[str] = []
        self._params: List[Union[None, Tuple]] = []

    def get(self) -> Tuple[List[str], List[Union[None, Tuple]]]:
        self._create_basic_tabs()
        self._insert_language()
        return self._queries, self._params

    def _create_basic_tabs(self):
        self._queries = [
            SQL["CREATE_TAB_valid_db"],
            SQL["CREATE_TAB_language"],
            SQL["CREATE_TAB_houses"],
            SQL["CREATE_TAB_tariffs"],
            SQL["CREATE_TAB_years"],
            SQL["CREATE_TAB_meters"]
        ]
        self._params = [None, None, None, None, None, None]

    def _insert_language(self):
        query: str = SQL["INSERT_language"]
        params = ("ENG",)
        self._queries.append(query)
        self._params.append(params)
