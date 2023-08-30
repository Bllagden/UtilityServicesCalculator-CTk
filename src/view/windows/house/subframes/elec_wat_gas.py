import customtkinter as ctk
from typing import List, Tuple, Dict, Optional

from src.controller import ControllerAPI
from src.view.windows import MessageBox

from .subframes import MetersMenuFrame
from .subframes import TitleFrame
from .subframes import ElecWaterGasDataFrame
from .subframes import ElecWaterGasChangeDataFrame


class ElecWaterGasFrame(ctk.CTkFrame):
    """Tabview tab - electricity | water | gas."""

    def __init__(self, master, master_window,
                 language: str,
                 house_id: int,
                 tariffs_tag: str,
                 text_titles: Tuple[str, str],
                 tab_columns: Tuple[
                     Tuple[str, str, str, str, str, str], Tuple[str, str, str]],
                 month_names: Tuple[str, ...],
                 localiz_mes_box_reads: Dict,
                 kwargs_default=True, **kwargs):
        if kwargs_default:
            kwargs.update(corner_radius=0, fg_color="transparent")
        super().__init__(master, **kwargs)

        self._house_id = house_id
        self._tariffs_tag = tariffs_tag
        self.localiz_mes_box_reads = localiz_mes_box_reads

        # meters menu =========================================================
        self.meters = MetersMenuFrame(self, master_window,
                                      language,
                                      self._house_id,
                                      self._tariffs_tag,
                                      self.localiz_mes_box_reads)
        self.meters.grid(row=0, column=0, columnspan=2, sticky="ns")

        # data frame and related ==============================================
        self._data_title = TitleFrame(self, text_titles[0])
        self._data_title.grid(row=1, column=0, sticky="nsew", padx=(0, 0))

        self.data = ElecWaterGasDataFrame(self, tab_columns[0], month_names)
        self.data.grid(row=2, column=0, sticky="nsew", padx=(0, 0))

        self.text_export_btn = ctk.StringVar()
        self._btn_export = ctk.CTkButton(self,
                                         textvariable=self.text_export_btn,
                                         command=self._export_btn_clicked)
        self._btn_export.grid(row=3, column=0, pady=(10, 5))

        # change data frame and related =======================================
        self._change_data_title = TitleFrame(self, text_titles[1])
        self._change_data_title.grid(row=1, column=1, sticky="nsew",
                                     padx=(10, 0))

        self.change_data = ElecWaterGasChangeDataFrame(self, tab_columns[1],
                                                       month_names,
                                                       self._tariffs_tag)
        self.change_data.grid(row=2, column=1, sticky="nsew", padx=(10, 0))

        self.text_calc_btn = ctk.StringVar()
        self._btn_calculate = ctk.CTkButton(self,
                                            textvariable=self.text_calc_btn,
                                            command=self._calculate_btn_clicked)
        self._btn_calculate.grid(row=3, column=1, pady=(10, 5))

        # fields ==============================================================
        self.selected_year = None
        self._input_readings = []
        self._input_tariffs = []
        self._meter_name = ""
        self._control_api = ControllerAPI()

    def set_selected_year(self, value: Optional[int]):
        self.selected_year = value
        self.meters.selected_year = value

    def _export_btn_clicked(self):
        MessageBox(self, "X", self.localiz_mes_box_reads["xxx"])

    def _calculate_btn_clicked(self):
        if self.selected_year is not None:
            self._meter_name = self.meters.get_meter_name()
            self._get_input_readings()
            self._get_selected_tariffs()

            self._control_api.calculate_elec_wat_gas(self._house_id,
                                                     self.selected_year,
                                                     self._tariffs_tag,
                                                     self._meter_name,
                                                     self._input_readings,
                                                     self._input_tariffs)
            header: int
            main: List[Tuple]
            header, main = self._control_api.get_one_tab_elec_wat_gas(
                self._house_id,
                self.selected_year,
                self._tariffs_tag)
            self.data.table_header.update_tab(header)
            self.data.table_main.update_tab(main)

        else:
            MessageBox(self, self.localiz_mes_box_reads["error_calculation"],
                       self.localiz_mes_box_reads["year_select"])

    def _get_input_readings(self):
        header: List[str] = self.change_data.readings_entries_header.get()
        main: List[str] = self.change_data.readings_entries_main.get()
        self._input_readings: List[str] = header + main

    def _get_selected_tariffs(self):
        self._input_tariffs: List[str] = \
            self.change_data.tariffs_comboboxes_main.get()
