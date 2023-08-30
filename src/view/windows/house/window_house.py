import customtkinter as ctk
from typing import List, Tuple, Optional

from src.controller import ControllerAPI
from src.view.win_settings import center_window
from src.view.localization import Localization
from src.view.windows import MessageBox

from .base_frame_years_menu import YearsMenuBaseFrame
from .base_frame_meter_readings import MeterReadingsBaseFrame


class HouseWindow(ctk.CTkToplevel):
    """Window for viewing and changing the meter readings of the selected house.
    """

    def __init__(self, master, house_name: str, house_id: int, language: str):
        super().__init__(master)

        self._lang = language
        self._control_api = ControllerAPI()

        # window settings =====================================================
        self._win_width = 865  # 865
        self._win_height = 560  # 560
        self.minsize(480, self._win_height)
        self.maxsize(self._win_width, self._win_height)
        center_window(self, self._win_width, self._win_height)

        localiz_pars = Localization(language).get_house_win_params()
        title_start = localiz_pars["title_main"]
        self.title(f"{title_start}: {house_name}")

        # grid ================================================================
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # years menu base frame ===============================================
        self._house_id = house_id
        self._years = YearsMenuBaseFrame(self, localiz_pars["tab_col_year"],
                                         self._house_id)
        self._years.grid(row=0, column=0, sticky="nsew")

        # meter readings base frame ===========================================
        text_mb_reads = Localization(self._lang).get_house_win_mes_box_reads()
        self._meter_readings = MeterReadingsBaseFrame(
            self,
            localiz_pars["tabview"],
            language,
            self._house_id,
            localiz_pars["labels_data_change_data"],
            localiz_pars["tab_cols_elec_wat_gas"],
            localiz_pars["tab_cols_garb"],
            localiz_pars["months"],
            text_mb_reads
        )
        self._meter_readings.grid(row=0, column=1, sticky="nsew",
                                  padx=(5, 0))

        # commands ============================================================
        self._new_year: Optional[int] = None
        self._selected_year: Optional[int] = None

        self._years.add_btn.configure(
            command=self._add_year_btn_clicked)
        self._years.del_btn.configure(
            command=self._del_year_btn_clicked)

        self._years.table.bind("<<TreeviewSelect>>",
                               self._select_year_table_row_clicked)

        # localization mes_boxes ==============================================
        self._set_localization_tk_vars()
        localiz = Localization(language)
        self.localiz_mes_box_years = localiz.get_house_win_mes_box_years()

    def _add_year_btn_clicked(self):
        self._new_year = self._years.get_input()

        if self._new_year is None:
            MessageBox(self, self.localiz_mes_box_years["error_creation"],
                       self.localiz_mes_box_years["fill_field"])
        else:
            self._execute_creation_year()

    def _execute_creation_year(self):
        result = self._control_api.create_year(self._house_id, self._new_year)

        if result == "ITEM_CREATED":
            self._years.table.update_tab()
            self._years.clear_input()
            self._reset_meters()
            self._reset_table_data()
            self._meter_readings.clear_input()
            MessageBox(self, self.localiz_mes_box_years["year_created"],
                       f"{self._new_year}")

        elif result == "ITEM_ALREADY_EXISTS":
            MessageBox(self, self.localiz_mes_box_years["error_creation"],
                       self.localiz_mes_box_years["year_exists"])

    def _del_year_btn_clicked(self):
        self._selected_year = self._years.table.get_selected_year()

        if self._selected_year is None:
            MessageBox(self, self.localiz_mes_box_years["error_deletion"],
                       self.localiz_mes_box_years["year_select"])
        else:
            self._control_api.delete_year(self._house_id, self._selected_year)
            self._reset_meters()
            self._reset_table_data()
            self._meter_readings.clear_input()
            MessageBox(self, self.localiz_mes_box_years["year_deleted"],
                       f"{self._selected_year}")
            self._years.table.update_tab()

    def _reset_meters(self):
        """Deactivate the menu of all meters."""
        self._meter_readings.elec.meters.deactivate()
        self._meter_readings.wat.meters.deactivate()
        self._meter_readings.gas.meters.deactivate()
        self._meter_readings.garb.meters.deactivate()

    def _reset_table_data(self):
        """Resets the values of all tables to the default values."""
        # elec, wat, gas ======================================================
        data_elec_wat_gas = self._control_api.get_base_tab_elec_wat_gas()
        header, main = data_elec_wat_gas

        # garb ================================================================
        data_garb = self._control_api.get_base_tab_garb()

        # table headers =======================================================
        self._meter_readings.elec.data.table_header.update_tab(
            header)
        self._meter_readings.wat.data.table_header.update_tab(header)
        self._meter_readings.gas.data.table_header.update_tab(header)

        # table mains =========================================================
        self._meter_readings.elec.data.table_main.update_tab(main)
        self._meter_readings.wat.data.table_main.update_tab(main)
        self._meter_readings.gas.data.table_main.update_tab(main)
        self._meter_readings.garb.data.table_main.update_tab(data_garb)

    def _select_year_table_row_clicked(self, event):
        """Callback by clicking on the year in the table."""
        self._selected_year = self._years.table.get_selected_year()

        if self._selected_year is not None:
            self._update_meters()
            self._update_tables()
            self._meter_readings.clear_input()
        self._set_selected_year(self._selected_year)

    def _set_selected_year(self, value):
        """
        Set the value of the selected year in subframes for further calculations
        """
        self._meter_readings.elec.set_selected_year(value)
        self._meter_readings.wat.set_selected_year(value)
        self._meter_readings.gas.set_selected_year(value)
        self._meter_readings.garb.set_selected_year(value)

    def _update_meters(self):
        """Activate the menu of all meters and fill them with the values
        obtained from the DB."""
        elec: List[str]
        wat: List[str]
        gas: List[str]
        garb: List[str]
        elec, wat, gas, garb = self._control_api.get_meter_names(self._house_id,
                                                                 self._selected_year)
        self._meter_readings.elec.meters.activate(elec)
        self._meter_readings.wat.meters.activate(wat)
        self._meter_readings.gas.meters.activate(gas)
        self._meter_readings.garb.meters.activate(garb)

    def _update_tables(self):
        """Update all tables with the values received from the DB."""
        header: Tuple[int, int, int]
        main: Tuple[List[Tuple], List[Tuple], List[Tuple], List[Tuple]]
        header, main = self._control_api.get_all_tabs_elec_wat_gas_garb(
            self._house_id,
            self._selected_year)

        # header tables =======================================================
        self._meter_readings.elec.data.table_header.update_tab(
            header[0])
        self._meter_readings.wat.data.table_header.update_tab(
            header[1])
        self._meter_readings.gas.data.table_header.update_tab(
            header[2])

        # main tables =========================================================
        self._meter_readings.elec.data.table_main.update_tab(main[0])
        self._meter_readings.wat.data.table_main.update_tab(main[1])
        self._meter_readings.gas.data.table_main.update_tab(main[2])
        self._meter_readings.garb.data.table_main.update_tab(main[3])

    def _set_localization_tk_vars(self):
        localiz_tk_vars = Localization(self._lang).get_house_win_tk_vars()

        # years table =========================================================
        self._years.text_add_btn.set(localiz_tk_vars["btn_add"])
        self._years.text_del_btn.set(localiz_tk_vars["btn_del"])

        # tabview subframes ===================================================
        # elec
        self._meter_readings.elec.meters.text_inactive_menu.set(
            localiz_tk_vars["menu_meters_default"])
        self._meter_readings.elec.meters.text_cur_menu.set(
            localiz_tk_vars["menu_meters_default"])
        self._meter_readings.elec.meters.text_params_btn.set(
            localiz_tk_vars["btn_meters_settings"])

        # wat
        self._meter_readings.wat.meters.text_inactive_menu.set(
            localiz_tk_vars["menu_meters_default"])
        self._meter_readings.wat.meters.text_cur_menu.set(
            localiz_tk_vars["menu_meters_default"])
        self._meter_readings.wat.meters.text_params_btn.set(
            localiz_tk_vars["btn_meters_settings"])

        # gas
        self._meter_readings.gas.meters.text_inactive_menu.set(
            localiz_tk_vars["menu_meters_default"])
        self._meter_readings.gas.meters.text_cur_menu.set(
            localiz_tk_vars["menu_meters_default"])
        self._meter_readings.gas.meters.text_params_btn.set(
            localiz_tk_vars["btn_meters_settings"])

        # garb
        self._meter_readings.garb.meters.text_inactive_menu.set(
            localiz_tk_vars["menu_meters_default"])
        self._meter_readings.garb.meters.text_cur_menu.set(
            localiz_tk_vars["menu_meters_default"])
        self._meter_readings.garb.meters.text_params_btn.set(
            localiz_tk_vars["btn_meters_settings"])

        # all types
        self._meter_readings.all_types.textbox.insert(
            "0.0",
            localiz_tk_vars["label_all_types"])

        # buttons =============================================================
        # elec
        self._meter_readings.elec.text_export_btn.set(
            localiz_tk_vars["btn_exp"])
        self._meter_readings.elec.text_calc_btn.set(
            localiz_tk_vars["btn_calc"])

        # wat
        self._meter_readings.wat.text_export_btn.set(
            localiz_tk_vars["btn_exp"])
        self._meter_readings.wat.text_calc_btn.set(
            localiz_tk_vars["btn_calc"])

        # gas
        self._meter_readings.gas.text_export_btn.set(
            localiz_tk_vars["btn_exp"])
        self._meter_readings.gas.text_calc_btn.set(
            localiz_tk_vars["btn_calc"])

        # garb
        self._meter_readings.garb.text_export_btn.set(
            localiz_tk_vars["btn_exp"])
        self._meter_readings.garb.text_calc_btn.set(
            localiz_tk_vars["btn_calc"])
