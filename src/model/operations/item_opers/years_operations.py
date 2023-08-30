from typing import List, Tuple, Union, Optional

from src.model.database import DatabaseOperations
from src.model.sql_builders import SQLBuilderAddYear
from src.model.sql_builders import SQLBuilderDelYear
from src.model.sql import SQL

from .item_operations import ItemOperations


class YearsOperations(ItemOperations):
    """Class for working with years in the DB.
    Submitting non-DB years raises an exception."""

    def __init__(self,
                 house_id: int,
                 year: Optional[int] = None):
        self._house_id = house_id
        self._year = year

    def _is_item_in_db(self) -> bool:
        """Is there a year in the DB by house_id and year."""
        result: List[Tuple]
        result = DatabaseOperations.single_query(
            SQL["SELECT_is_year"], (self._house_id, self._year)
        )
        return bool(result)

    def _add_into_db(self):
        """Adding a year to the DB (house_id, year).
        When a year is created, a table is created in the DB for it,
        storing all its meter readings, tariffs, etc.
        """
        sql_build = SQLBuilderAddYear(self._house_id, self._year)

        queries: List[str]
        params: List[Union[None, Tuple, List[Tuple]]]
        queries, params = sql_build.get()
        DatabaseOperations.transaction(queries, params)

    def _del_from_db(self):
        """Deleting the year from the DB by house_id and year."""
        all_tabs: List[str] = DatabaseOperations().get_db_tab_names()
        sql_build = SQLBuilderDelYear(self._house_id, self._year, all_tabs)

        queries: List[str]
        params: List[Optional[Tuple]]
        queries, params = sql_build.get()
        DatabaseOperations.transaction(queries, params)

    def get_table(self) -> List[Tuple[int]]:
        """Getting a list of years of a selected house from the DB for a table.
        return options: [(2023,), (2024,), ...] or []
        """
        query: str = SQL["SELECT_years"]
        params = (self._house_id,)
        return DatabaseOperations.single_query(query, params)
