from typing import List, Tuple, Optional

from model.database import DatabaseOperations
from model.sql_builders import SQLBuilderDelHouse
from model.sql import SQL

from .item_operations import ItemOperations


class HousesOperations(ItemOperations):
    """Class for working with houses in the DB.
    Submitting non-DB houses raises an exception.
    Name and description must not be empty strings."""

    def __init__(self,
                 house_name: str,
                 house_desc: Optional[str] = None):
        self._house_name = house_name
        self._house_desc = house_desc

    def _is_item_in_db(self) -> bool:
        """Is there a house in the DB by name."""
        result: List[Tuple[int, str, str]]
        result = DatabaseOperations.single_query(
            SQL["SELECT_is_house"], (self._house_name,)
        )
        return bool(result)

    def _add_into_db(self):
        """Adding a house to the DB (name, description)."""
        DatabaseOperations.single_query(
            SQL["INSERT_house"], (self._house_name, self._house_desc)
        )

    def _del_from_db(self):
        """Deleting a house from the DB by name."""
        all_tabs: List[str] = DatabaseOperations().get_db_tab_names()
        sql_build = SQLBuilderDelHouse(self.get_house_id(), all_tabs)

        queries: List[str]
        params: List[Optional[Tuple]]
        queries, params = sql_build.get()
        DatabaseOperations.transaction(queries, params)

    def get_house_id(self) -> int:
        """Getting the house ID by its name from the DB."""
        if self._is_item_in_db():
            house_id: List[Tuple[int]]  # [(1,)]
            house_id = DatabaseOperations.single_query(
                SQL["SELECT_house_id"], (self._house_name,)
            )
            return house_id[0][0]
        else:
            raise ValueError("The house was not found in the DB.")

    @staticmethod
    def get_table() -> List[Tuple[str, str]]:
        """Getting a list of all houses from the DB for a table.
        return options: [('My house', '123'), ('Your house', '456'), ...] or []
        """
        query: str = SQL["SELECT_houses"]
        return DatabaseOperations.single_query(query)
