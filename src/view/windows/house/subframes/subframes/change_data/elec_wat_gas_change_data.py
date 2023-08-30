import customtkinter as ctk
from typing import Tuple

from src.controller import ControllerAPI

from .subframes import MonthsLabelsFrame
from .subframes import ReadingsEntriesFrame
from .subframes import TariffsComboboxesFrame


class ElecWaterGasChangeDataFrame(ctk.CTkFrame):
    """Right part of the elec_wat_gas frame (menu for changing data)."""

    def __init__(self, master,
                 tab_columns: Tuple[str, str, str],
                 month_names: Tuple[str, ...],
                 tariffs_tag: str, **kwargs):
        super().__init__(master, **kwargs)

        self._month_names = month_names
        self._control_api = ControllerAPI()
        self._main_font = ctk.CTkFont("CTkDefaultFont", 13)

        # months ==============================================================
        self._months_labels_header = None
        self._months_labels_title = None
        self._months_labels_main = None
        self._create_months_labels(tab_columns[0])
        self._grid_months_labels()

        # readings ============================================================
        self.readings_entries_header = None
        self._readings_entries_title = None
        self.readings_entries_main = None
        self._create_readings_entries(tab_columns[1])
        self._grid_readings_entries()

        # tariffs =============================================================
        self._tariffs_comboboxes_title = None
        self.tariffs_comboboxes_main = None
        self._tariffs_tag = tariffs_tag
        self._create_tariffs_comboboxes(tab_columns[2])
        self._grid_tariffs_comboboxes()

    def _create_months_labels(self, text: str):
        self._months_labels_header = MonthsLabelsFrame(
            self,
            "HEADER",
            self._month_names
        )
        self._months_labels_title = ctk.CTkLabel(
            self,
            text=text,
            fg_color="#4A4A4A",
            width=80,  # 90
            height=18,
            font=self._main_font
        )
        self._months_labels_main = MonthsLabelsFrame(
            self,
            "MAIN_BODY",
            self._month_names)

    def _create_readings_entries(self, text: str):
        self.readings_entries_header = ReadingsEntriesFrame(
            self,
            frame_part="HEADER"
        )
        self._readings_entries_title = ctk.CTkLabel(
            self,
            text=text,
            fg_color="#4A4A4A",
            width=90,
            height=18,
            font=self._main_font
        )
        self.readings_entries_main = ReadingsEntriesFrame(
            self,
            frame_part="MAIN_BODY")

    def _create_tariffs_comboboxes(self, text: str):
        self._tariffs_comboboxes_title = ctk.CTkLabel(
            self,
            text=text,
            fg_color="#4A4A4A",
            width=100,
            height=18,
            font=self._main_font
        )
        self.tariffs_comboboxes_main = TariffsComboboxesFrame(
            self,
            self._control_api.get_tariffs_by_type(self._tariffs_tag))

    def _grid_months_labels(self):
        self._months_labels_header.grid(row=0, column=0,
                                        padx=(10, 0), pady=(10, 0))
        self._months_labels_title.grid(row=1, column=0,
                                       padx=(10, 0))
        self._months_labels_main.grid(row=2, column=0,
                                      padx=(10, 0), pady=(0, 10))

    def _grid_readings_entries(self):
        self.readings_entries_header.grid(row=0, column=1,
                                          padx=(2, 0), pady=(10, 0))
        self._readings_entries_title.grid(row=1, column=1,
                                          padx=(2, 0))
        self.readings_entries_main.grid(row=2, column=1,
                                        padx=(2, 0), pady=(0, 10))

    def _grid_tariffs_comboboxes(self):
        self._tariffs_comboboxes_title.grid(row=1, column=2,
                                            padx=(2, 10))
        self.tariffs_comboboxes_main.grid(row=2, column=2,
                                          padx=(2, 10), pady=(0, 10))
