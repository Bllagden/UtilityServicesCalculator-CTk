from typing import List, Tuple, Union

from model.sql import SQL

from .sql_builder import SQLBuilder


class SQLBuilderSetReadsGarb(SQLBuilder):
    """
    The class builds a SQL-query for a transaction that updates one table of
    readings in the DB (garb) for a specific house and year.
    """

    def __init__(self, tab_name: str, tariffs: List[Union[float, str]]):
        self._tab_name = tab_name
        self._tariffs = tariffs

        self._query: str = ""
        self._params: List[Tuple] = []

    def get(self) -> Tuple[str, List[Tuple]]:
        self._set_main()
        return self._query, self._params

    def _set_main(self):
        query: str = SQL["UPDATE_tariff_price"]
        self._query = self.merge(query, self._tab_name)
        self._params = [(self._tariffs[i - 1], i) for i in range(1, 13)]
