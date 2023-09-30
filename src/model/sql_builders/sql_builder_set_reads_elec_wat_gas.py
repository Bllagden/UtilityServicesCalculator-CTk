from typing import List, Tuple, Union

from model.sql import SQL

from .sql_builder import SQLBuilder


class SQLBuilderSetReadsElecWatGas(SQLBuilder):
    """
    The class builds a SQL-query for a transaction that updates one table of
    meter readings in a DB (elec, wat, gas) of a specific house, year, and type.
    """

    def __init__(self, tab_name: str, readings: List[int],
                 consumption: List[Union[int, str]], tariffs: List[float],
                 price: List[Union[float, str]]):
        self._tab_name = tab_name
        self._readings = readings
        self._consumption = consumption
        self._tariffs = tariffs
        self._price = price

        self._queries: List[str] = []
        self._params: List[Union[Tuple, List[Tuple]]] = []

    def get(self) -> Tuple[List[str], List[Union[Tuple, List[Tuple]]]]:
        self._set_header()
        self._set_main()
        return self._queries, self._params

    def _set_header(self):
        """SQL-query for updating the readings of the previous December."""
        query: str = SQL["UPDATE_0_reads"]
        form_query: str = self.merge(query, self._tab_name)
        self._queries.append(form_query)

        params: Tuple[int] = (self._readings[0],)
        self._params.append(params)

    def _set_main(self):
        """SQL-query for updating the main data."""
        query: str = SQL["UPDATE_main_reads"]
        form_query: str = self.merge(query, self._tab_name)
        self._queries.append(form_query)

        papams: List[Tuple]
        params = [
            (self._readings[i + 1],
             self._consumption[i],
             self._tariffs[i],
             self._price[i],
             i + 1) for i in range(0, 12)
        ]
        self._params.append(params)
