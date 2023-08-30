import customtkinter as ctk
from typing import List


class TariffsComboboxesFrame(ctk.CTkFrame):
    """Frame with comboboxes for selecting tariffs in a column for each month"""

    def __init__(self, master, tariff_values: List[str],
                 kwargs_default=True, **kwargs):
        if kwargs_default: kwargs.update(fg_color="transparent")
        super().__init__(master, **kwargs)

        self._tariff_1 = self._create_combobox(tariff_values)
        self._tariff_2 = self._create_combobox(tariff_values)
        self._tariff_3 = self._create_combobox(tariff_values)
        self._tariff_4 = self._create_combobox(tariff_values)
        self._tariff_5 = self._create_combobox(tariff_values)
        self._tariff_6 = self._create_combobox(tariff_values)
        self._tariff_7 = self._create_combobox(tariff_values)
        self._tariff_8 = self._create_combobox(tariff_values)
        self._tariff_9 = self._create_combobox(tariff_values)
        self._tariff_10 = self._create_combobox(tariff_values)
        self._tariff_11 = self._create_combobox(tariff_values)
        self._tariff_12 = self._create_combobox(tariff_values)

        self._tariff_1.grid(row=0, column=0)
        self._tariff_2.grid(row=1, column=0)
        self._tariff_3.grid(row=2, column=0)
        self._tariff_4.grid(row=3, column=0)
        self._tariff_5.grid(row=4, column=0)
        self._tariff_6.grid(row=5, column=0)
        self._tariff_7.grid(row=6, column=0)
        self._tariff_8.grid(row=7, column=0)
        self._tariff_9.grid(row=8, column=0)
        self._tariff_10.grid(row=9, column=0)
        self._tariff_11.grid(row=10, column=0)
        self._tariff_12.grid(row=11, column=0)

    def _create_combobox(self, values: List[str]):
        combobox = ctk.CTkComboBox(self,
                                   values=values,
                                   state="readonly",
                                   width=100)
        return combobox

    def clear(self):
        self._tariff_1.set("")
        self._tariff_2.set("")
        self._tariff_3.set("")
        self._tariff_4.set("")
        self._tariff_5.set("")
        self._tariff_6.set("")
        self._tariff_7.set("")
        self._tariff_8.set("")
        self._tariff_9.set("")
        self._tariff_10.set("")
        self._tariff_11.set("")
        self._tariff_12.set("")

    def get(self) -> List[str]:
        selected_tariffs = [
            self._tariff_1.get(),
            self._tariff_2.get(),
            self._tariff_3.get(),
            self._tariff_4.get(),
            self._tariff_5.get(),
            self._tariff_6.get(),
            self._tariff_7.get(),
            self._tariff_8.get(),
            self._tariff_9.get(),
            self._tariff_10.get(),
            self._tariff_11.get(),
            self._tariff_12.get()
        ]
        return selected_tariffs
