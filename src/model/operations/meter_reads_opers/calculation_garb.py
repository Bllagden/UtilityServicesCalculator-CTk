from typing import List, Tuple, Union, Optional

from src.model.database import DatabaseOperations
from src.model.sql_builders import SQLBuilder
from src.model.sql_builders import SQLBuilderSetReadsGarb
from src.model.sql_builders import SQLBuilderTabNames
from src.model.sql import SQL


class CalculationGarb:
    """The class calculates new values for DB table (garb) and updates
    the corresponding table in the DB."""

    def __init__(self,
                 house_id: int,
                 year: int,
                 meter_type: str,
                 meter_name: str,
                 input_tariffs: List[Optional[float]]
                 ):
        self._house_id = house_id
        self._year = year
        self._meter_type = meter_type
        self._meter_name = meter_name
        self._input_tariffs = input_tariffs

        self._tab_name = ""
        self._meter_num: int

        self._old_tariffs: List[Union[float, str]] = []
        self._merged_tariffs: List[Union[float, str]] = []

    def execute(self):
        self._get_meter_num()
        self._build_tab_name()
        self._old_tariffs = self._get_from_db()
        self._merged_tariffs = self._merge_data(self._input_tariffs,
                                                self._old_tariffs)
        self._update_db_table()

    def _get_meter_num(self):
        """Gets the current meter number."""
        query = SQL["SELECT_meter_num"]
        params = (
            self._house_id, self._year, self._meter_type, self._meter_name)
        data: List[Tuple[int]] = DatabaseOperations.single_query(query, params)
        self._meter_num = data[0][0]

    def _build_tab_name(self):
        """Builds the name of the table being worked on."""
        sql_build = SQLBuilderTabNames()
        self._tab_name = sql_build.build_tab_name(self._house_id, self._year,
                                                  self._meter_type,
                                                  self._meter_num)

    def _get_from_db(self) -> List[Union[float, str]]:
        """Gets the old data from the DB table (tariffs)."""
        query = SQL["SELECT_tariff_price"]
        form_query = SQLBuilder().merge(query, self._tab_name)

        data: List[Tuple[Union[float, str]]]  # 12 tuples
        data = DatabaseOperations.single_query(form_query)

        tariffs: List[Union[float, str]] = [_tuple[0] for _tuple in data]
        return tariffs

    @staticmethod
    def _merge_data(input_data: List[Optional[float]],
                    old_data: List[Union[float, str]]
                    ) -> List[Union[float, str]]:
        """
        Merges old data from the DB and new data from the interface (tariffs)"""
        merged_data = []
        for i, val in enumerate(input_data):
            if val is not None:
                merged_data.append(val)
            else:
                merged_data.append(old_data[i])
        return merged_data

    def _update_db_table(self):
        """Update a DB table with new data."""
        sql_build = SQLBuilderSetReadsGarb(self._tab_name, self._merged_tariffs)

        query: str
        params: List[Tuple]
        query, params = sql_build.get()
        DatabaseOperations.single_query(query, params)
