import customtkinter as ctk
from typing import Tuple

from .subframes import ElecWaterGasDataHeaderFrame
from .subframes import ElecWatGasTableWidget


class ElecWaterGasDataFrame(ctk.CTkFrame):
    """Left part of the elec_wat_gas frame (data table)."""

    def __init__(self, master, tab_columns: Tuple[str, str, str, str, str, str],
                 month_names: Tuple[str, ...], **kwargs):
        super().__init__(master, **kwargs)

        # table header ========================================================
        self.table_header = ElecWaterGasDataHeaderFrame(self,
                                                        month_names[-1],
                                                        width=100,
                                                        fg_color="#343638")
        self.table_header.grid(row=0, column=0, sticky="w",
                               padx=(10, 0), pady=(10, 0))

        # table main ==========================================================
        self.table_main = ElecWatGasTableWidget(self, tab_columns, month_names)
        self.table_main.grid(row=1, column=0, sticky="nsew",
                             padx=(10, 10), pady=(0, 10))
