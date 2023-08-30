from typing import List, Tuple, Optional

from src.model.database import DatabaseOperations
from src.model.sql_builders import SQLBuilderGetReads


class GetMeterReadings:
    """
    Class for getting tables containing meter readings and related information
    for the selected house, year and meter_type.

    header - meter readings from the previous December."""

    def __init__(self,
                 house_id: int,
                 year: int,
                 meter_type: Optional[str] = None):
        self._house_id = house_id
        self._year = year
        self._meter_type = meter_type

    @staticmethod
    def base_tab_elec_wat_gas() -> Tuple[int, List[Tuple]]:
        """Returns the default table for (elec | wat | gas)."""
        header = 0
        main: List[Tuple]
        main = [(i, 0, "X", 0.0, "X") for i in range(1, 13)]
        return header, main

    @staticmethod
    def base_tab_garb() -> List[Tuple]:
        """Returns the default table for garb."""
        main: List[Tuple]
        main = [(i, "X") for i in range(1, 13)]
        return main

    def one_tab_elec_wat_gas(self) -> Tuple[int, List[Tuple]]:
        """Returns one table from the DB (elec | wat | gas)."""
        sql_build = SQLBuilderGetReads(self._house_id, self._year,
                                       self._meter_type)
        if self._meter_type in {"elec", "wat", "gas"}:
            query_elec_wat_gas: List[str]
            params: List[None]
            query_elec_wat_gas, params = sql_build.one_tab_elec_wat_gas()

            data: List[List[Tuple]]
            data = DatabaseOperations.transaction(query_elec_wat_gas, params)

            header: int = data[0][0][0]
            main: List[Tuple] = data[1]
            return header, main
        else:
            raise ValueError("Wrong 'meter_type'")

    def one_tab_garb(self):
        """Returns one table from the DB (garb)."""
        sql_build = SQLBuilderGetReads(self._house_id, self._year,
                                       self._meter_type)
        if self._meter_type == "garb":
            query_garb: str = sql_build.one_tab_garb()
            data = DatabaseOperations.single_query(query_garb)
            return data
        else:
            raise ValueError("Wrong 'meter_type'")

    def all_tabs_elec_wat_gas_garb(self) -> Tuple[Tuple, Tuple]:
        """Returns all tables from the database (elec & wat & gas & garb)."""
        sql_build = SQLBuilderGetReads(self._house_id, self._year)

        query: List[str]
        params: List[None]
        queries, params = sql_build.all_tabs()

        data: List[List[Tuple]]
        data = DatabaseOperations.transaction(queries, params)

        header: Tuple[int, int, int]
        header = data[0][0][0], data[1][0][0], data[2][0][0]

        main: Tuple[List[Tuple], List[Tuple], List[Tuple], List[Tuple]]
        main = data[3], data[4], data[5], data[6]

        return header, main
