import customtkinter as ctk
from typing import Tuple

from .subframes import GarbageTableWidget


class GarbageDataFrame(ctk.CTkFrame):
    """Left part of the garbage frame (data table)."""

    def __init__(self, master, tab_columns: Tuple[str, str, str],
                 month_names: Tuple[str, ...], **kwargs):
        super().__init__(master, **kwargs)

        self.table_main = GarbageTableWidget(self, tab_columns, month_names)
        self.table_main.grid(row=0, column=0, sticky="nsew",
                             padx=(10, 10), pady=(10, 10))
