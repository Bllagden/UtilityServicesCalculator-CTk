import customtkinter as ctk
from typing import Tuple, Dict, Optional

from src.view.windows import MessageBox
from src.view.windows import HouseWindow

from .subframes import DataFrame
from .subframes import MenuFrame


class HousesBaseFrame(ctk.CTkFrame):
    def __init__(self, master, control_api, kwargs_default=True, **kwargs):
        if kwargs_default:
            kwargs.update(corner_radius=0, fg_color="transparent")
        super().__init__(master, **kwargs)

        self._master = master
        self._control_api = control_api
        self.cur_lang = ""
        self.localiz_mes_box_houses: Dict = dict()

        # grid ================================================================
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # data ================================================================
        self.data = DataFrame(self, "HOUSES")
        self.data.grid(row=0, column=0, sticky="nsew")

        # menu ================================================================
        self.menu = MenuFrame(self, "HOUSES")
        self.menu.grid(row=0, column=1, sticky="nsew")

        # commands for btns from menu =========================================
        self.menu.btn_add.configure(command=self._add_house_btn_clicked)
        self.menu.btn_del.configure(command=self._del_house_btn_clicked)
        self._house_window = None
        self.data.btn_open.configure(command=self._open_house_btn_clicked)

    def _add_house_btn_clicked(self):
        house_input: Tuple[Optional[str], Optional[str]]
        house_input = self.menu.get_input()

        house_name: Optional[str]
        house_desc: Optional[str]
        house_name, house_desc = house_input

        if (house_name is None) or (house_desc is None):
            MessageBox(self, self.localiz_mes_box_houses["error_creation"],
                       self.localiz_mes_box_houses["fill_fields"])
        else:
            self._execute_creation_house(house_name, house_desc)

    def _execute_creation_house(self, house_name: str, house_desc: str):
        result = self._control_api.create_house(house_name, house_desc)

        if result == "ITEM_CREATED":
            self.data.table.update_tab()
            self.menu.clear_input()
            self.menu.btn_add.focus()
            MessageBox(self, self.localiz_mes_box_houses["house_created"],
                       house_name)

        elif result == "ITEM_ALREADY_EXISTS":
            MessageBox(self, self.localiz_mes_box_houses["error_creation"],
                       self.localiz_mes_box_houses["house_exists"])

    def _del_house_btn_clicked(self):
        house_name: Optional[str]
        house_name = self.data.table.get_name_selected_house()

        if house_name is None:
            MessageBox(self, self.localiz_mes_box_houses["error_deletion"],
                       self.localiz_mes_box_houses["house_select"])
        else:
            self._control_api.delete_house(house_name)
            self.data.table.update_tab()
            MessageBox(self, self.localiz_mes_box_houses["house_deleted"],
                       house_name)

    def _open_house_btn_clicked(self):
        house_name: Optional[str]
        house_name = self.data.table.get_name_selected_house()

        if house_name is None:
            MessageBox(self, self.localiz_mes_box_houses["error_opening"],
                       self.localiz_mes_box_houses["house_select"])
        else:
            house_id = self._control_api.get_house_id(house_name)
            self._open_window_selected_house(house_name, house_id)

    def _open_window_selected_house(self, house_name, house_id):
        """Hides the main window.
        Opens the window of the selected house with the protocol of its closing.
        """
        self._master.withdraw()
        self._house_window = HouseWindow(self._master,
                                         house_name,
                                         house_id,
                                         self.cur_lang)
        self._house_window.protocol("WM_DELETE_WINDOW",
                                    self._close_window_selected_house)

    def _close_window_selected_house(self):
        """Command for the protocol of closing the window of the selected house.
        Closes the window of the selected house and returns the visibility
        of the main window."""
        self._house_window.destroy()
        self._master.deiconify()
