import customtkinter as ctk

from src.view.win_settings import center_window
from src.view.localization import Localization

from .base_frame_navigation import NavigationBaseFrame
from .base_frame_houses import HousesBaseFrame
from .base_frame_tariffs import TariffsBaseFrame


class MainWindow(ctk.CTk):
    def __init__(self, controller_api):
        super().__init__()
        self._control_api = controller_api
        self._control_api.db_connect()

        # window settings =====================================================
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        self._win_width = 640  # 600
        self._win_height = 395  # 350
        center_window(self, self._win_width, self._win_height)
        self._init_gui()

        # grid layout 1x2 =====================================================
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # base frames =========================================================
        self._navigate = NavigationBaseFrame(self)
        self._houses = HousesBaseFrame(self, self._control_api)
        self._tariffs = TariffsBaseFrame(self, self._control_api)

        self._navigate.grid(row=0, column=0, sticky="nsew")
        self._navigate.grid_rowconfigure(6, weight=1)

        # commands ============================================================
        self._navigate.houses_btn.configure(command=self._select_houses_frame)
        self._navigate.tariffs_btn.configure(command=self._select_tariffs_frame)
        self._navigate.lang_menu.configure(command=self._event_set_localization)

        # default preferences =================================================
        self._select_houses_frame()
        self._event_set_localization(self._control_api.get_language())

    @staticmethod
    def _init_gui():
        ctk.deactivate_automatic_dpi_awareness()
        # self.tk.call('tk', 'scaling', 2.0)
        # ctypes.windll.shcore.SetProcessDpiAwareness(2)

    def _select_houses_frame(self):
        self._select_frame_by_navigation("HOUSES")

    def _select_tariffs_frame(self):
        self._select_frame_by_navigation("TARIFFS")

    def _select_frame_by_navigation(self, frame_name: str):
        # setting the button color for the selected button
        self._navigate.houses_btn.configure(fg_color=(
            "gray75", "gray25") if frame_name == "HOUSES" else "transparent")
        self._navigate.tariffs_btn.configure(fg_color=(
            "gray75", "gray25") if frame_name == "TARIFFS" else "transparent")

        # show selected frame
        if frame_name == "HOUSES":
            self._houses.grid(row=0, column=1, sticky="nsew")
        else:
            self._houses.grid_forget()
        if frame_name == "TARIFFS":
            self._tariffs.grid(row=0, column=1, sticky="nsew")
        else:
            self._tariffs.grid_forget()

    def _event_set_localization(self, language: str):
        localiz = Localization(language).get_main_win()

        # window title ========================================================
        self.title(localiz["title_main"])

        # navigate ============================================================
        self._navigate.text_houses_btn.set(localiz["btn_houses"])
        self._navigate.text_tariffs_btn.set(localiz["btn_tariffs"])

        # houses data =========================================================
        text_houses_tab_cols = (localiz["label_house_name"],
                                localiz["label_house_desc"])
        self._houses.data.table.rename_columns(text_houses_tab_cols)

        self._houses.data.text_open_btn.set(localiz["btn_open"])

        # houses menu =========================================================
        self._houses.menu.text_label_menu.set(localiz["label_create_delete"])

        text_houses_fields = (localiz["label_house_name"],
                              localiz["label_house_desc"])
        self._houses.menu.rename_fields(text_houses_fields)

        self._houses.menu.text_add_btn.set(localiz["btn_add"])
        self._houses.menu.text_del_btn.set(localiz["btn_del"])

        # tariff data =========================================================
        text_tariffs_tab_cols = (localiz["label_tariff_type"],
                                 localiz["label_tariff_value"])
        self._tariffs.data.table.rename_columns(text_tariffs_tab_cols)

        self._tariffs.data.table.tariff_types = localiz["meter_types"]
        self._tariffs.data.table.update_tab()

        self._tariffs.data.text_note_label.set(localiz["label_tariff_note"])

        # tariff menu =========================================================
        self._tariffs.menu.text_label_menu.set(localiz["label_create_delete"])

        self._tariffs.menu.text_tariff_type.set(localiz["label_tariff_type"])
        text_tariffs_fields = (localiz["label_tariff_type"],
                               localiz["meter_types"],
                               localiz["label_tariff_value"])
        self._tariffs.menu.rename_fields(text_tariffs_fields)
        self._tariffs.set_tariff_types(localiz["meter_types"])

        self._tariffs.menu.text_add_btn.set(localiz["btn_add"])
        self._tariffs.menu.text_del_btn.set(localiz["btn_del"])

        # message_boxes for houses and tariffs ================================
        text_mb_houses = Localization(language).get_main_win_mes_box_houses()
        text_mb_tariffs = Localization(language).get_main_win_mes_box_tariffs()
        self._houses.localiz_mes_box_houses = text_mb_houses
        self._tariffs.localiz_mes_box_tariffs = text_mb_tariffs

        # final settings ======================================================
        self._navigate.lang_menu.focus()
        self._navigate.lang_menu.set(language)
        self._houses.cur_lang = language
        self._control_api.set_language(language)
