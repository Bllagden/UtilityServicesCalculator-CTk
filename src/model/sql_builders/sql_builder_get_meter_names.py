from typing import List, Tuple

from model.sql import SQL

from .sql_builder import SQLBuilder


class SQLBuilderGetMeterNames(SQLBuilder):
    """The class builds a SQL-query for a transaction that returns
    names of meters of all types of a selected house and year."""

    def __init__(self, house_id: int, year: int):
        self._house_id = house_id
        self._year = year

        self._queries: List[str] = []
        self._params: List[Tuple] = []

    def get(self) -> Tuple[List[str], List[Tuple]]:
        self._build()
        return self._queries, self._params

    def _build(self):
        queries: List[str]
        self._queries = [SQL["SELECT_meter_names"]] * 4

        self._params = [(self._house_id, self._year, "elec"),
                        (self._house_id, self._year, "wat"),
                        (self._house_id, self._year, "gas"),
                        (self._house_id, self._year, "garb")]
