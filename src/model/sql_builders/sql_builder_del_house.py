from typing import List, Tuple, Optional

from src.model.sql import SQL

from .sql_builder import SQLBuilder
from .sql_builder_tab_names import SQLBuilderTabNames


class SQLBuilderDelHouse(SQLBuilder):
    """The class builds an SQL-query for a transaction that deletes a house."""

    def __init__(self, house_id: int, all_tabs: List[str]):
        self._house_id = house_id
        self._all_tabs = all_tabs

        self._queries: List[str] = []
        self._params: List[Optional[Tuple]] = []

    def get(self) -> Tuple[List[str], List[Optional[Tuple]]]:
        self._delete_row_house()
        self._delete_rows_years()
        self._delete_rows_meters()
        self._drop_tabs_meters()
        return self._queries, self._params

    def _delete_row_house(self):
        """Delete house from the 'house' table."""
        query: str = SQL["DELETE_house"]
        self._queries.append(query)

        params: Tuple[int] = (self._house_id,)
        self._params.append(params)

    def _delete_rows_years(self):
        """Delete all years of this house from the 'year' table."""
        query: str = SQL["DELETE_years"]
        self._queries.append(query)

        params: Tuple[int] = (self._house_id,)
        self._params.append(params)

    def _delete_rows_meters(self):
        """Delete all meters of this house from the 'meters' table."""
        query: str = SQL["DELETE_meters_by_house"]
        self._queries.append(query)

        params: Tuple[int] = (self._house_id,)
        self._params.append(params)

    def _drop_tabs_meters(self):
        """Delete the meter tables of this house to store readings."""
        sql = SQLBuilderTabNames()
        prefix: str = sql.build_tab_name_prefix(self._house_id)
        tab_names: List[str] = sql.find_tabs_by_prefix(self._all_tabs, prefix)

        queries: List[str] = [SQL["DROP_TAB"], ] * len(tab_names)
        form_queries: List[str] = self.merge(queries, tab_names)
        self._queries.extend(form_queries)

        params = (None,) * len(tab_names)
        self._params.extend(params)
