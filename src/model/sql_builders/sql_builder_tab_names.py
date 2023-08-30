from typing import List, Optional


class SQLBuilderTabNames:
    """A class for assembling DB table names of particular meters.
    Each of the tables stores the readings of a particular meter, year, house.

            'house_1_2023_elec_1'
    'house_houseID_year_meterTAG_meterNUM'
    """

    @staticmethod
    def build_tab_name(house_id: int, year: int, meter_type: str, num: int = 1
                       ) -> str:
        """ 'house_1_2023_elec_1' """
        name = f"house_{house_id}_{year}_{meter_type}_{num}"
        return name

    def build_names_first_tabs(self, house_id: int, year: int) -> List[str]:
        n1 = self.build_tab_name(house_id, year, "elec")
        n2 = self.build_tab_name(house_id, year, "wat")
        n3 = self.build_tab_name(house_id, year, "gas")
        n4 = self.build_tab_name(house_id, year, "garb")
        return [n1, n2, n3, n4]

    @staticmethod
    def build_tab_name_prefix(house_id: int, year: Optional[int] = None) -> str:
        """ 'house_1_', 'house_1_2023_' """
        if year is None:
            table_name_prefix = f"house_{house_id}_"
        else:
            table_name_prefix = f"house_{house_id}_{year}_"
        return table_name_prefix

    @staticmethod
    def find_tabs_by_prefix(tabs: List[str], prefix: str) -> List[str]:
        """tabs - list with table names"""
        tabs_with_prefix = []
        for tab in tabs:
            if tab.startswith(prefix):
                tabs_with_prefix.append(tab)
        return tabs_with_prefix
