from typing import List, Tuple, Optional

from model.database import DatabaseOperations
from model.sql_builders import SQLBuilderGetMeterNames
from model.sql import SQL

from .item_operations import ItemOperations


class MetersOperations(ItemOperations):
    """Class for working with meters in the DB.
    Submitting non-DB meters raises an exception.

    meter_type options: 'elec' | 'wat' | 'gas' | 'garb' """

    def __init__(self,
                 house_id: int,
                 year: int,
                 meter_type: Optional[str] = None):
        self._house_id = house_id
        self._year = year
        self._meter_type = meter_type

    def _is_item_in_db(self):
        """Is there a meter in the DB.
        Not implemented yet."""
        pass

    def _add_into_db(self):
        """Adding a meter to the DB.
        Not implemented yet."""
        pass

    def _del_from_db(self):
        """Deleting a meter from the DB.
        Not implemented yet."""
        pass

    def get_names(self) -> Tuple[List[str], ...]:
        """Getting the names of meters of all types of a selected house and
        year from the DB."""
        sql_build = SQLBuilderGetMeterNames(self._house_id, self._year)
        queries, params = sql_build.get()

        data: List[List[Tuple[str]]]
        # [ [('Met1',), ('Met2',)], [('Met1',)], [('Met1',)], ... ]
        data = DatabaseOperations.transaction(queries, params)

        result: Tuple[List[str], ...]
        # ( ['Met1', 'Met2'], ['Met1'], ['Met1'], ... )
        result = tuple([x[0] for x in sublist] for sublist in data)

        return result

    def get_table(self) -> List[Tuple[str]]:
        """Getting a list of meter names for the selected house, year and type
        from the DB for the table.
        return options: [('Elec_Met_1',), ('Elec_Met_2',), ...] or []
        """

        query: str = SQL["SELECT_meter_names"]
        params = (self._house_id, self._year, self._meter_type)

        data: List[Tuple[str]] = DatabaseOperations.single_query(query,
                                                                   params)
        return data
