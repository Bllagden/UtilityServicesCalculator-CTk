from typing import List, Tuple, Union, Optional
from decimal import Decimal

from src.model.database import DatabaseOperations
from src.model.sql_builders import SQLBuilder
from src.model.sql_builders import SQLBuilderSetReadsElecWatGas
from src.model.sql_builders import SQLBuilderTabNames
from src.model.sql import SQL


class CalculationElecWatGas:
    """
    The class calculates new values for DB table (elec | wat | gas) and updates
    the corresponding table in the DB."""

    def __init__(self,
                 house_id: int,
                 year: int,
                 meter_type: str,
                 meter_name: str,
                 input_readings: List[Optional[int]],
                 input_tariffs: List[Optional[float]]
                 ):
        self._house_id = house_id
        self._year = year
        self._meter_type = meter_type
        self._meter_name = meter_name
        self._input_readings = input_readings
        self._input_tariffs = input_tariffs

        self._tab_name = ""
        self._meter_num: int

        self._old_readings: List[int] = []
        self._old_tariffs: List[float] = []

        self._merged_readings: List[int] = []
        self._merged_tariffs: List[float] = []

        self._consumption: List[Union[int, str]] = []
        self._price: List[Union[float, str]] = []

    def execute(self):
        self._get_meter_num()
        self._build_tab_name()
        self._old_readings, self._old_tariffs = self._get_from_db()
        self._merged_readings = self._merge_data(self._input_readings,
                                                 self._old_readings)
        self._merged_tariffs = self._merge_data(self._input_tariffs,
                                                self._old_tariffs)
        self._consumption = self._calculate_consumption()
        self._price = self._calculate_price()
        self._update_db_table()

    def _get_meter_num(self):
        """Gets the current meter number."""
        query: str = SQL["SELECT_meter_num"]
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

    def _get_from_db(self) -> Tuple[List[int], List[float]]:
        """Gets the old data from the DB table (meter readings and tariffs)."""
        query = SQL["SELECT_reads__tariff"]
        form_query = SQLBuilder().merge(query, self._tab_name)

        data: List[Tuple[int, float]]  # 13 tuples
        data = DatabaseOperations.single_query(form_query)

        readings: List[int] = [_tuple[0] for _tuple in data]
        tariffs: List[float] = [_tuple[1] for _tuple in data]
        del tariffs[0]  # December last year
        return readings, tariffs

    @staticmethod
    def _merge_data(
            input_data: Union[List[Optional[int]], List[Optional[float]]],
            old_data: Union[List[int], List[float]]
    ) -> Union[List[int], List[float]]:
        """Merges old data from the DB and new data from the interface
        (meter readings and tariffs)."""
        merged_data = []
        for i, val in enumerate(input_data):
            if val is not None:
                merged_data.append(val)
            else:
                merged_data.append(old_data[i])
        return merged_data

    def _calculate_consumption(self) -> List[Union[int, str]]:
        """Getting the consumption for each month from the new meter readings"""
        consump = []
        for i, read in enumerate(self._merged_readings):
            if i == 12: break
            consump.append(self._merged_readings[i + 1] - read)
        result = self._convert_consumption(consump)
        return result

    def _convert_consumption(self, consump) -> List[Union[int, str]]:
        """Replacement of negative and unused consumption values for each month.
        """
        for i, val in enumerate(consump):
            if val < 0:
                consump[i] = "X"
            if (val == 0) and (self._merged_readings[i + 1] == 0):
                consump[i] = "X"
        return consump

    def _calculate_price(self) -> List[Union[float, str]]:
        """Calculation of prices for each month."""
        price = []
        for i, consump in enumerate(self._consumption):
            if consump == "X":
                price.append("X")
            else:
                price_i = Decimal(consump) * Decimal(self._merged_tariffs[i])
                price_i = round(price_i, 2)
                price.append(float(price_i))
        return price

    def _update_db_table(self):
        """Update a DB table with new data."""
        sql_build = SQLBuilderSetReadsElecWatGas(self._tab_name,
                                                 self._merged_readings,
                                                 self._consumption,
                                                 self._merged_tariffs,
                                                 self._price)
        queries: List[str]
        params: List[Union[Tuple, List[Tuple]]]
        queries, params = sql_build.get()
        DatabaseOperations.transaction(queries, params)
