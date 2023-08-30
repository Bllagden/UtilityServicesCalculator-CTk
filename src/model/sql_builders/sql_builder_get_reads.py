from typing import List, Tuple, Optional

from src.model.sql import SQL

from .sql_builder import SQLBuilder
from .sql_builder_tab_names import SQLBuilderTabNames


class SQLBuilderGetReads(SQLBuilder):
    """The class builds a SQL-query for a transaction that returns one or all
    tables of meter readings from the DB (elec, wat, gas, garb)
    for a particular house and year."""

    def __init__(self, house_id: int, year: int,
                 meter_type: Optional[str] = None):
        self._house_id = house_id
        self._year = year
        self._meter_type = meter_type

        self._tab_name: str = ""
        self._tab_names: List[str] = []
        self._queries: List[str] = []
        self._params: List[None] = []

    def one_tab_elec_wat_gas(self) -> Tuple[List[str], List[None]]:
        """SQL-query for one table (elec | wat | gas)."""
        self._build_tab_name()

        query_1: str = SQL["SELECT_0_reads"]
        query_2: str = SQL["SELECT_main_reads"]
        queries = [query_1, query_2]
        self._tab_names = [self._tab_name, self._tab_name]
        form_queries: List[str] = self.merge(queries, self._tab_names)
        self._queries.extend(form_queries)

        params = (None, None)
        self._params.extend(params)
        return self._queries, self._params

    def one_tab_garb(self) -> str:
        """SQL-query for one table (garb)."""
        self._build_tab_name()
        query: str = SQL["SELECT_all"]
        form_query: str = self.merge(query, self._tab_name)
        return form_query

    def all_tabs(self) -> Tuple[List[str], List[None]]:
        """SQL-query for all tables (elec, wat, gas, garb)."""
        self._build_tab_names()
        self._get_all_headers()
        self._get_all_mains()
        return self._queries, self._params

    def _build_tab_name(self):
        """
        Builds a table name for the SQL-query from which readings will be taken
        (elec | wat | gas | garb)."""
        self._tab_name = SQLBuilderTabNames().build_tab_name(self._house_id,
                                                             self._year,
                                                             self._meter_type)

    def _build_tab_names(self):
        """
        Builds table names for the SQL query, from which readings will be taken
        (elec & wat & gas & garb)."""
        sql = SQLBuilderTabNames()
        tab_1 = sql.build_tab_name(self._house_id, self._year, "elec")
        tab_2 = sql.build_tab_name(self._house_id, self._year, "wat")
        tab_3 = sql.build_tab_name(self._house_id, self._year, "gas")
        tab_4 = sql.build_tab_name(self._house_id, self._year, "garb")
        self._tab_names = [tab_1, tab_2, tab_3, tab_4]

    def _get_all_headers(self):
        """All readings from previous December (elec & wat & gas)."""
        queries: List[str] = [SQL["SELECT_0_reads"], ] * 3
        form_queries: List[str] = self.merge(queries, self._tab_names[:3])
        self._queries.extend(form_queries)

        params = (None,) * 3
        self._params.extend(params)

    def _get_all_mains(self):
        """All main readings and related info (elec & wat & gas & garb)."""
        queries: List[str] = [SQL["SELECT_main_reads"], ] * 3
        queries.append(SQL["SELECT_all"])
        form_queries: List[str] = self.merge(queries, self._tab_names)
        self._queries.extend(form_queries)

        params = (None,) * 4
        self._params.extend(params)
