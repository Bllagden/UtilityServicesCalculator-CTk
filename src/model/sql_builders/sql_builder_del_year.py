from typing import List, Tuple, Optional

from model.sql import SQL

from .sql_builder import SQLBuilder
from .sql_builder_tab_names import SQLBuilderTabNames


class SQLBuilderDelYear(SQLBuilder):
    """The class builds an SQL-query for a transaction that deletes the year
    of the selected house."""

    def __init__(self, house_id: int, year: int, all_tabs: List[str]):
        self._house_id = house_id
        self._year = year
        self._all_tabs = all_tabs

        self._queries: List[str] = []
        self._params: List[Optional[Tuple]] = []

    def get(self) -> Tuple[List[str], List[Optional[Tuple]]]:
        self._delete_row_year()
        self._delete_rows_meters()
        self._drop_tabs_meters()
        return self._queries, self._params

    def _delete_row_year(self):
        """Delete year of selected house from the 'year' table."""
        query: str = SQL["DELETE_year"]
        self._queries.append(query)

        params: Tuple[int, int] = (self._house_id, self._year)
        self._params.append(params)

    def _delete_rows_meters(self):
        """Delete all meters of this year from the 'meters' table."""
        query: str = SQL["DELETE_meters_by_house_year"]
        self._queries.append(query)

        params: Tuple[int, int] = (self._house_id, self._year)
        self._params.append(params)

    def _drop_tabs_meters(self):
        """Delete the meter tables of this year to store readings."""
        sql = SQLBuilderTabNames()
        prefix: str = sql.build_tab_name_prefix(self._house_id, self._year)
        tab_names: List[str] = sql.find_tabs_by_prefix(self._all_tabs, prefix)

        queries: List[str] = [SQL["DROP_TAB"], ] * len(tab_names)
        form_queries: List[str] = self.merge(queries, tab_names)
        self._queries.extend(form_queries)

        params = (None,) * len(tab_names)
        self._params.extend(params)
