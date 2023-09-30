from typing import List, Tuple, Union

from model.sql import SQL

from .sql_builder import SQLBuilder
from .sql_builder_tab_names import SQLBuilderTabNames


class SQLBuilderAddYear(SQLBuilder):
    """The class builds an SQL-query for a transaction that creates a year
    for the selected house."""

    def __init__(self, house_id: int, year: int):
        self._house_id = house_id
        self._year = year

        self._queries: List[str] = []
        self._params: List[Union[None, Tuple, List[Tuple]]] = []

    def get(self) -> Tuple[List[str], List[Union[None, Tuple, List[Tuple]]]]:
        self._insert_row_year()
        self._insert_rows_meters()
        self._create_insert_meter_tabs()
        return self._queries, self._params

    def _insert_row_year(self):
        """Insert new year of selected house into 'years' table."""
        query: str = SQL["INSERT_year"]
        self._queries.append(query)

        params: Tuple[int, int, int, int, int, int]
        params = (self._house_id, self._year, 1, 1, 1, 1)
        self._params.append(params)

    def _insert_rows_meters(self):
        """Insert new first meters of selected house into the 'meters' table."""
        queries: List[str] = [SQL["INSERT_meter"]] * 4
        self._queries.extend(queries)

        params: List[Tuple[int, int, str, int, str]]
        p1 = (self._house_id, self._year, "elec", 1, "1")
        p2 = (self._house_id, self._year, "wat", 1, "1")
        p3 = (self._house_id, self._year, "gas", 1, "1")
        p4 = (self._house_id, self._year, "garb", 1, "1")
        params = [p1, p2, p3, p4]
        self._params.extend(params)

    def _create_insert_meter_tabs(self):
        """Creation and initial filling of meter tables for storing readings."""
        sql = SQLBuilderTabNames()
        tab_names: List[str]
        tab_names = sql.build_names_first_tabs(self._house_id, self._year)

        self._create_meter_tabs(tab_names)
        self._insert_into_meter_tabs(tab_names)

    def _create_meter_tabs(self, tab_names):
        queries: List[str] = [SQL["CREATE_TAB_elec_wat_gas"], ] * 3
        queries.append(SQL["CREATE_TAB_garb"])
        form_queries: List[str] = self.merge(queries, tab_names)
        self._queries.extend(form_queries)

        params = (None, None, None, None)
        self._params.extend(params)

    def _insert_into_meter_tabs(self, tab_names):
        queries: List[str] = [SQL["INSERT_in_elec_wat_gas"], ] * 3
        queries.append(SQL["INSERT_in_garb"])
        form_queries: List[str] = self.merge(queries, tab_names)
        self._queries.extend(form_queries)

        data_elec_wat_gas: List[Tuple]
        data_elec_wat_gas = [(i, 0, "X", 0.0, "X") for i in range(0, 13)]

        data_garb: List[Tuple]
        data_garb = [(i, "X") for i in range(1, 13)]

        params: List[List[Tuple]]
        params = [data_elec_wat_gas] * 3
        params.append(data_garb)

        self._params.extend(params)
