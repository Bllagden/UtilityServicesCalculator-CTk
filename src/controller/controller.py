from typing import List, Tuple, Optional

from model import DatabaseSetup
from model import GetSetLanguage
# item operations
from model import HousesOperations
from model import TariffsOperations
from model import YearsOperations
from model import MetersOperations
# meter readings operations
from model import GetMeterReadings
from model import CalculationElecWatGas
from model import CalculationGarb

from .converter_readings import ConverterReadings
from .converter_tariffs import ConverterTariffs


class Controller:
    """A low-level 'Controller' class for 'Model' and 'View' interaction.

    Docstrings for these methods are in the 'ControllerAPI' class and
    in the 'Model' classes."""

    @staticmethod
    def db_connect():
        DatabaseSetup().execute()

    @staticmethod
    def get_language() -> str:
        return GetSetLanguage.get()

    @staticmethod
    def set_language(language: str):
        GetSetLanguage.set(language)

    # Houses ==================================================================
    @staticmethod
    def get_tab_houses() -> List[Tuple[str, str]]:
        data: List[Tuple[str, str]]
        data = HousesOperations.get_table()
        return data

    @staticmethod
    def create_house(house_name: str, house_desc: str) -> str:
        return HousesOperations(house_name, house_desc).create()

    @staticmethod
    def delete_house(house_name: str):
        HousesOperations(house_name).delete()

    @staticmethod
    def get_house_id(house_name: str) -> int:
        return HousesOperations(house_name).get_house_id()

    # Tariffs =================================================================
    @staticmethod
    def get_tab_tariffs() -> List[Tuple[str, str]]:
        data: List[Tuple[str, float]]
        data = TariffsOperations.get_table()

        new_data: List[Tuple[str, str]]
        new_data = ConverterTariffs.floats_to_strs_in_tuples(data)
        return new_data

    @staticmethod
    def create_tariff(tariff_type: str, tariff_value: str) -> str:
        tar_oper = TariffsOperations(tariff_type,
                                     ConverterTariffs.str_to_float(tariff_value)
                                     )
        return tar_oper.create()

    @staticmethod
    def delete_tariff(tariff_type: str, tariff_value: str):
        tar_oper = TariffsOperations(tariff_type,
                                     ConverterTariffs.str_to_float(tariff_value)
                                     )
        tar_oper.delete()

    @staticmethod
    def get_tariffs_by_type(tariff_tag: str) -> List[str]:
        data: List[float] = TariffsOperations(tariff_tag).get_values_by_type()
        return ConverterTariffs.floats_to_strs(data)

    # Years ===================================================================
    @staticmethod
    def get_tab_years(house_id) -> List[Tuple[int]]:
        data: List[Tuple[int]]
        data = YearsOperations(house_id).get_table()
        data.sort()
        return data

    @staticmethod
    def create_year(house_id: int, year: int) -> str:
        return YearsOperations(house_id, year).create()

    @staticmethod
    def delete_year(house_id: int, year: int):
        YearsOperations(house_id, year).delete()

    # Meters ==================================================================
    @staticmethod
    def get_meter_names(house_id: int, year: int) -> Tuple[List[str], ...]:
        return MetersOperations(house_id, year).get_names()

    @staticmethod
    def get_tab_meters(house_id: int, year: int, meter_type: str
                       ) -> List[Tuple[str]]:
        return MetersOperations(house_id, year, meter_type).get_table()

    @staticmethod
    def create_meter():
        pass

    @staticmethod
    def delete_meter():
        pass

    # Meter readings ==========================================================
    @staticmethod
    def get_base_tab_elec_wat_gas() -> Tuple[int, List[Tuple]]:
        data: Tuple[int, List[Tuple]]
        data = GetMeterReadings.base_tab_elec_wat_gas()

        header: int = data[0]
        main: List[Tuple] = data[1]
        new_main = ConverterReadings.elec_wat_gas(main)
        return header, new_main

    @staticmethod
    def get_base_tab_garb() -> List[Tuple]:
        data: List[Tuple] = GetMeterReadings.base_tab_garb()
        new_data = ConverterReadings.garb(data)
        return new_data

    @staticmethod
    def get_one_tab_elec_wat_gas(house_id: int, year: int, meter_type: str
                                 ) -> Tuple[int, List[Tuple]]:
        get_met_read = GetMeterReadings(house_id, year, meter_type)

        data: Tuple[int, List[Tuple]]
        data = get_met_read.one_tab_elec_wat_gas()

        header: int = data[0]
        main: List[Tuple] = data[1]
        new_main: List[Tuple] = ConverterReadings.elec_wat_gas(main)
        return header, new_main

    @staticmethod
    def get_one_tab_garb(house_id: int, year: int, meter_type: str
                         ) -> List[Tuple]:
        get_met_read = GetMeterReadings(house_id, year, meter_type)

        data: List[Tuple] = get_met_read.one_tab_garb()
        new_data: List[Tuple] = ConverterReadings.garb(data)
        return new_data

    @staticmethod
    def get_all_tabs_elec_wat_gas_garb(house_id: int, year: int
                                       ) -> Tuple[Tuple[int, int, int],
    Tuple[List[Tuple], List[Tuple], List[Tuple], List[Tuple]]]:
        get_met_read = GetMeterReadings(house_id, year)
        data: Tuple[
            Tuple[int, int, int],
            Tuple[List[Tuple], List[Tuple], List[Tuple], List[Tuple]]
        ]
        data = get_met_read.all_tabs_elec_wat_gas_garb()

        headers: Tuple[int, int, int] = data[0]
        mains: Tuple[List, List, List, List] = data[1]
        l1 = ConverterReadings.elec_wat_gas(mains[0])
        l2 = ConverterReadings.elec_wat_gas(mains[1])
        l3 = ConverterReadings.elec_wat_gas(mains[2])
        l4 = ConverterReadings.garb(mains[3])
        new_mains: Tuple[List, List, List, List] = (l1, l2, l3, l4)
        return headers, new_mains

    # Calculation =============================================================
    @staticmethod
    def calculate_elec_wat_gas(house_id: int, year: int, meter_type: str,
                               meter_name: str, input_readings: List[str],
                               input_tariffs: List[str]
                               ):
        readings: List[Optional[int]]
        readings = ConverterReadings.strs_to_ints_or_none(input_readings)

        tariffs: List[Optional[float]]
        tariffs = ConverterTariffs.strs_to_floats_or_none(input_tariffs)

        CalculationElecWatGas(house_id, year, meter_type, meter_name, readings,
                              tariffs).execute()

    @staticmethod
    def calculate_garb(house_id: int, year: int, meter_type: str,
                       meter_name: str, input_tariffs: List[str]
                       ):
        tariffs: List[Optional[float]]
        tariffs = ConverterTariffs.strs_to_floats_or_none(input_tariffs)

        CalculationGarb(house_id, year, meter_type, meter_name,
                        tariffs).execute()
