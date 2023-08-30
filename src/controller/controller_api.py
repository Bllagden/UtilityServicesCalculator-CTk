from typing import List, Tuple

from .controller import Controller


class ControllerAPI:
    """A high-level 'Controller' class for 'Model' and 'View' interaction.
    Uses the functionality of the low-level 'Controller' class.

    Imported into the 'View' and its methods are called from there."""

    def __init__(self, controller=Controller()):
        self.controller = controller

    def db_connect(self):
        """The first connection to the DB while the program is running.
        Creates and configures a DB if it does not already exist.
        Prints the path and name of the DB."""
        self.controller.db_connect()

    def get_language(self) -> str:
        """Get the current interface language from the DB.
        return options: 'RU' | 'ENG' """
        return self.controller.get_language()

    def set_language(self, language: str):
        """Update the current interface language in the DB.
        input options: 'RU' | 'ENG' """
        self.controller.set_language(language)

    # Houses ==================================================================
    #   * name and description must not be empty strings
    #   * submitting non-DB houses raises an exception

    def get_tab_houses(self) -> List[Tuple[str, str]]:
        """Getting a list of all houses from the DB for a table.
        return options: [('My house', '123'), ('Your house', '456'), ...] or []
        """
        return self.controller.get_tab_houses()

    def create_house(self, house_name: str, house_desc: str) -> str:
        """
        The method tries to create a house in the DB and returns a str result:
            'ITEM_CREATED';
            'ITEM_ALREADY_EXISTS' ('house_name' is already in the DB)."""
        return self.controller.create_house(house_name, house_desc)

    def delete_house(self, house_name: str):
        """The method removes the house by name from the DB."""
        self.controller.delete_house(house_name)

    def get_house_id(self, house_name: str) -> int:
        """The method gets house id from the DB by name."""
        return self.controller.get_house_id(house_name)

    # Tariffs =================================================================
    #   * type and value must not be empty strings
    #   * submitting non-DB tariffs raises an exception
    #   * type options: 'elec' | 'wat' | 'gas' | 'garb'
    #   * value options: '2' | '2.0' | '2,0' | '2.6' | '2,67'

    def get_tab_tariffs(self) -> List[Tuple[str, str]]:
        """Getting a list of all tariffs from the DB for a table.
        return options: [('elec', '4,5'), ('wat', '2,0'), ...] or []
        """
        return self.controller.get_tab_tariffs()

    def create_tariff(self, tariff_type: str, tariff_value: str) -> str:
        """
        The method tries to create a tariff in the DB and returns a str result:
            'ITEM_CREATED';
            'ITEM_ALREADY_EXISTS' ('t_type' and 't_value' is already in the DB).
        """
        return self.controller.create_tariff(tariff_type, tariff_value)

    def delete_tariff(self, tariff_type: str, tariff_value: str):
        """The method removes the tariff by type and value from the DB."""
        self.controller.delete_tariff(tariff_type, tariff_value)

    def get_tariffs_by_type(self, tariff_tag: str) -> List[str]:
        """Getting a list of tariff values by type from the DB.
        return options:  ['10,8', '2,0', '0,0']  |  ['0,0']"""
        return self.controller.get_tariffs_by_type(tariff_tag)

    # Years ===================================================================
    #   * submitting non-DB years raises an exception

    def get_tab_years(self, house_id: int) -> List[Tuple[int]]:
        """Getting a list of years of a selected house from the DB for a table.
        return options: [(2023,), (2024,), ...] or []
        """
        return self.controller.get_tab_years(house_id)

    def create_year(self, house_id: int, year: int) -> str:
        """
        The method tries to create a year in the DB and returns a str result:
            'ITEM_CREATED';
            'ITEM_ALREADY_EXISTS' ('year' is already in the DB)."""
        return self.controller.create_year(house_id, year)

    def delete_year(self, house_id: int, year: int):
        """The method removes the year by 'house_id' and 'year' from the DB."""
        self.controller.delete_year(house_id, year)

    # Meters ==================================================================
    #   * submitting non-DB meters raises an exception

    def get_meter_names(self, house_id: int, year: int
                        ) -> Tuple[List[str], ...]:
        """Getting the names of meters of all types of a particular house and
        year from the DB.
        return options:(['Met1', 'Met2'], ['Met1'], ['Met1'], ... )"""
        return self.controller.get_meter_names(house_id, year)

    def get_tab_meters(self, house_id: int, year: int, meter_type: str
                       ) -> List[Tuple[str]]:
        """Getting a list of meter names for the selected house, year and type
        from the DB for the table.
        return options: [('Elec_Met_1',), ('Elec_Met_2',), ...] or []
        """
        return self.controller.get_tab_meters(house_id, year, meter_type)

    def create_meter(self):
        """Not implemented yet"""
        pass

    def delete_meter(self):
        """Not implemented yet"""
        pass

    # Meter readings ==========================================================
    def get_base_tab_elec_wat_gas(self) -> Tuple[int, List[Tuple]]:
        """Returns the default table (elec | wat | gas) containing
        meter readings and related information.

        return options:
            (0, [(1, 0, 'X', '0,0', 'X'), ... , (12, 0, 'X', '0,0', 'X')])"""
        return self.controller.get_base_tab_elec_wat_gas()

    def get_base_tab_garb(self) -> List[Tuple]:
        """Returns the default table (garb) containing
        tariffs and related information for .

        return options: [(1, 'X'), ... , (12, 'X')]"""
        return self.controller.get_base_tab_garb()

    def get_one_tab_elec_wat_gas(self, house_id: int, year: int, meter_type: str
                                 ) -> Tuple[int, List[Tuple]]:
        """Returns the selected DB table (elec | wat | gas) containing
        meter readings and related information.

        return options:
            (19, [(1, 36, 17, '5,0', '85,00'), ... , (12, 0, 'X', '0,0', 'X')])
        """
        return self.controller.get_one_tab_elec_wat_gas(house_id, year,
                                                        meter_type)

    def get_one_tab_garb(self, house_id: int, year: int, meter_type: str
                         ) -> List[Tuple]:
        """Returns the selected DB table (garb) containing
        tariffs and related information.

        return options: [(1, '448,65'), ... , (12, 'X')]"""
        return self.controller.get_one_tab_garb(house_id, year, meter_type)

    def get_all_tabs_elec_wat_gas_garb(self, house_id: int, year: int
                                       ) -> Tuple[Tuple, Tuple]:
        """Returns the selected 4 DB tables (elec & wat & gas & garb) containing
        meter readings and related information.

        type -> Tuple[
                    Tuple[int, int, int],
                    Tuple[List[Tuple], List[Tuple], List[Tuple], List[Tuple]]
                ]

        return options:
            (
              (19, 4, 17),
              (
                [(1, 36, 17, '5,0', '85,00'), ... , (12, 0, 'X', '0,0', 'X')],
                [(1, 25, 21, '6,0', '126,00'), ... , (12, 0, 'X', '0,0', 'X')],
                [(1, 98, 81, '0,0', '0,00'), ... , (12, 0, 'X', '0,0', 'X')],
                [(1, '448,65'), ... , (12, 'X')]
              )
            )
        """
        return self.controller.get_all_tabs_elec_wat_gas_garb(house_id, year)

    # Calculation =============================================================
    def calculate_elec_wat_gas(self, house_id: int, year: int,
                               meter_type: str, meter_name: str,
                               input_readings: List[str],
                               input_tariffs: List[str]):
        """Calculates new values for DB table (elec | wat | gas) and updates
        the corresponding table in the DB."""
        self.controller.calculate_elec_wat_gas(
            house_id, year, meter_type, meter_name, input_readings,
            input_tariffs)

    def calculate_garb(self, house_id: int, year: int,
                       meter_type: str, meter_name: str,
                       input_tariffs: List[str]):
        """Calculates new values for DB table (garb) and updates
        the corresponding table in the DB."""
        self.controller.calculate_garb(
            house_id, year, meter_type, meter_name, input_tariffs)
