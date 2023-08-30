import customtkinter as ctk

from src.controller import ControllerAPI
from src.view.win_settings import center_window
from src.view.localization import Localization

from .base_frame_data import DataBaseFrame
from .base_frame_menu import MenuBaseFrame


class MetersWindow(ctk.CTkToplevel):
    """A window for setting meters for the selected house, year and type."""

    def __init__(self, master, language: str, house_id: int, year: int,
                 meter_tag: str):
        super().__init__(master)

        # fields ==============================================================
        self._language = language
        self._house_id = house_id
        self._year = year
        self._meter_tag = meter_tag
        self._control_api = ControllerAPI()

        # window settings =====================================================
        self.grab_set()
        self._win_width = 420
        self._win_height = 300
        self.resizable(False, False)
        center_window(self, self._win_width, self._win_height)

        localiz_pars = Localization(language).get_meters_win_params()
        title_start = localiz_pars["title_meters"]
        self.title(f"{title_start}: {meter_tag}")

        # grid ================================================================
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # base frames =========================================================
        self.data = DataBaseFrame(self, localiz_pars["tab_col_meter_name"],
                                  house_id, year, meter_tag)
        self.data.grid(row=0, column=0, sticky="nsew")

        self.menu = MenuBaseFrame(self, language)
        self.menu.grid(row=0, column=1, sticky="nsew")

        # localization ========================================================
        self._set_localization()

    def _set_localization(self):
        localiz_tk_vars = Localization(self._language).get_meters_win_tk_vars()
        self.menu.text_label_menu.set(localiz_tk_vars["label_control"])
        self.menu.text_add_btn.set(localiz_tk_vars["btn_add"])
        self.menu.text_rename_btn.set(localiz_tk_vars["btn_rename"])
        self.menu.text_del_btn.set(localiz_tk_vars["btn_del"])
