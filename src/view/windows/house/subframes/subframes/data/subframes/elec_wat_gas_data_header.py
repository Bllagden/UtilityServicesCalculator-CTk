import customtkinter as ctk

from controller import ControllerAPI


class ElecWaterGasDataHeaderFrame(ctk.CTkFrame):
    """Meter readings from the previous December."""

    def __init__(self, master, month_dec: str, **kwargs):
        super().__init__(master, **kwargs)

        main_font = ctk.CTkFont("CTkDefaultFont", 13)
        self.control_api = ControllerAPI()

        self._label_num = ctk.CTkLabel(self,
                                       text="0",
                                       fg_color="#343638",
                                       width=30,
                                       font=main_font)
        self._label_month = ctk.CTkLabel(self,
                                         text=f" {month_dec}",
                                         fg_color="#343638",
                                         width=71,  # 75
                                         font=main_font,
                                         anchor="w")
        self._readings = ctk.CTkLabel(self,
                                      text=f"{self._get_base_readings()}",
                                      fg_color="#343638",
                                      width=75,
                                      font=main_font,
                                      anchor="e")
        self._label_end_header = ctk.CTkLabel(self,
                                              text="",
                                              fg_color="#343638",
                                              width=4)

        self._label_num.grid(row=0, column=0)
        self._label_month.grid(row=0, column=1)
        self._readings.grid(row=0, column=2)
        self._label_end_header.grid(row=0, column=3)

    def _get_base_readings(self):
        return self.control_api.get_base_tab_elec_wat_gas()[0]

    def update_tab(self, value):
        self._readings.configure(text=value)
