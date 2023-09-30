from typing import List, Tuple, Optional

from model.database import DatabaseOperations
from model.sql import SQL

from .item_operations import ItemOperations


class TariffsOperations(ItemOperations):
    """Class for working with tariffs in the DB.
    Submitting non-DB tariffs raises an exception.

    Type and value must not be empty strings.
    type options: 'elec' | 'wat' | 'gas' | 'garb'
    value options: '2' | '2.0' | '2,0' | '2.6' | '2,67'
    """

    def __init__(self,
                 tariff_type: str,
                 tariff_value: Optional[float] = None):
        self._tariff_type = tariff_type
        self._tariff_value = tariff_value

        self._tariff_values_by_type: List[Tuple[float]] = []

    def _is_item_in_db(self) -> bool:
        """Is there a tariff in the DB by type and value."""
        result: List[Tuple[str, float]]
        result = DatabaseOperations.single_query(
            SQL["SELECT_is_tariff"], (self._tariff_type, self._tariff_value)
        )
        return bool(result)

    def _add_into_db(self):
        """Adding a tariff to the DB (type, value)."""
        DatabaseOperations.single_query(
            SQL["INSERT_tariff"], (self._tariff_type, self._tariff_value)
        )

    def _del_from_db(self):
        """Deleting a tariff from the DB by type and value."""
        DatabaseOperations.single_query(
            SQL["DELETE_tariff"], (self._tariff_type, self._tariff_value)
        )

    @staticmethod
    def get_table() -> List[Tuple[str, float]]:
        """Getting a list of all tariffs from the DB for a table.
        return options: [('elec', '4.5'), ('wat', '2.0'), ...] or []
        """
        query: str = SQL["SELECT_tariffs"]
        return DatabaseOperations.single_query(query)

    def get_values_by_type(self) -> List[float]:
        """Getting a list of tariff values by type from the DB.
        return options:  [10.8, 2.0, 0.0]  |  [0.0]"""
        self._select_values()
        return self._convert_values()

    def _select_values(self):
        """result: [(2.0,), (10.8,), ...] or []"""
        result: List[Tuple[float]]
        result = DatabaseOperations.single_query(
            SQL["SELECT_tariffs_by_type"], (self._tariff_type,)
        )
        self._tariff_values_by_type = result

    def _convert_values(self) -> List[float]:
        """Conversion of tariff values of a specific type and their sorting.
        values from db : [(2.0,), (10.8,)]    |   []
        return options:  [10.8, 2.0, 0.0]     |  [0.0]
        """
        conv_tars = []
        if self._tariff_values_by_type:
            conv_tars = list(
                tuple_i[0] for tuple_i in self._tariff_values_by_type)
            conv_tars.sort(reverse=True)
        conv_tars.append(0.0)
        return conv_tars
