import customtkinter as ctk
from typing import Tuple

from .table_meters import MetersTableWidget


class DataBaseFrame(ctk.CTkFrame):
    def __init__(self, master, column_names: Tuple[str], house_id: int,
                 year: int, meter_type: str, kwargs_default=True, **kwargs):
        if kwargs_default: kwargs.update(corner_radius=0,
                                         fg_color="transparent")
        super().__init__(master, **kwargs)

        self._house_id = house_id
        self._year = year
        self._meter_type = meter_type

        self.table = MetersTableWidget(self, column_names, house_id, year,
                                       meter_type)
        self.table.grid(row=0, column=0, sticky="nsew")
        self._create_scroll()

    def _create_scroll(self):
        self._scroll = ctk.CTkScrollbar(self, command=self.table.yview)
        self._scroll.grid(row=0, column=1, sticky="nsew")
        self.table.configure(yscrollcommand=self._scroll.set)
