import customtkinter as ctk
from typing import List, Tuple, Dict, Optional

from view.windows import MessageBox

from .subframes import DataFrame
from .subframes import MenuFrame


class TariffsBaseFrame(ctk.CTkFrame):
    def __init__(self, master, control_api, kwargs_default=True, **kwargs):
        if kwargs_default:
            kwargs.update(corner_radius=0, fg_color="transparent")
        super().__init__(master, **kwargs)

        self._control_api = control_api
        self.localiz_mes_box_tariffs: Dict = dict()

        # grid ================================================================
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # data ================================================================
        self.data = DataFrame(self, "TARIFFS")
        self.data.grid(row=0, column=0, sticky="nsew")

        # menu ================================================================
        self.menu = MenuFrame(self, "TARIFFS")
        self.menu.grid(row=0, column=1, sticky="nsew")

        # commands for btns from menu =========================================
        self.menu.btn_add.configure(command=self._add_tariff_btn_clicked)
        self.menu.btn_del.configure(command=self._del_tariff_btn_clicked)

        # tariff types ========================================================
        self.text_elec_type = ctk.StringVar()
        self.text_wat_type = ctk.StringVar()
        self.text_gas_type = ctk.StringVar()
        self.text_garb_type = ctk.StringVar()

    def set_tariff_types(self, values: List[str]):
        """For localization."""
        self.text_elec_type.set(values[0])
        self.text_wat_type.set(values[1])
        self.text_gas_type.set(values[2])
        self.text_garb_type.set(values[3])

    def _add_tariff_btn_clicked(self):
        tariff_input: Tuple[Optional[str], Optional[str]]
        tariff_input = self.menu.get_input()

        tariff_type: Optional[str]
        tariff_value: Optional[str]
        tariff_type, tariff_value = tariff_input

        if (tariff_type is None) or (tariff_value is None):
            MessageBox(self, self.localiz_mes_box_tariffs["error_creation"],
                       self.localiz_mes_box_tariffs["fill_fields"])
        else:
            self._execute_creation_tariff(tariff_type, tariff_value)

    def _del_tariff_btn_clicked(self):
        selected_tariff: Optional[List[str]]
        selected_tariff = self.data.table.get_selected_tariff()

        if selected_tariff is None:
            MessageBox(self, self.localiz_mes_box_tariffs["error_deletion"],
                       self.localiz_mes_box_tariffs["tariff_select"])
        else:
            tariff_type: str
            tariff_value: str
            tariff_type, tariff_value = selected_tariff
            tariff_tag: str = self._get_tariff_tag(tariff_type)

            self._control_api.delete_tariff(tariff_tag, tariff_value)
            self.data.table.update_tab()
            MessageBox(self, self.localiz_mes_box_tariffs["tariff_deleted"],
                       f"{tariff_type}: {tariff_value}")

    def _execute_creation_tariff(self, tariff_type, tariff_value):
        tariff_tag: str = self._get_tariff_tag(tariff_type)
        result: str = self._control_api.create_tariff(tariff_tag, tariff_value)

        if result == "ITEM_CREATED":
            self.data.table.update_tab()
            self.menu.clear_input()
            self.menu.btn_add.focus()
            MessageBox(self, self.localiz_mes_box_tariffs["tariff_created"],
                       f"{tariff_type}: {tariff_value}")

        elif result == "ITEM_ALREADY_EXISTS":
            MessageBox(self, self.localiz_mes_box_tariffs["error_creation"],
                       self.localiz_mes_box_tariffs["tariff_exists"])

    def _get_tariff_tag(self, tariff_type: str) -> str:
        if tariff_type == self.text_elec_type.get():
            return "elec"
        elif tariff_type == self.text_wat_type.get():
            return "wat"
        elif tariff_type == self.text_gas_type.get():
            return "gas"
        elif tariff_type == self.text_garb_type.get():
            return "garb"
