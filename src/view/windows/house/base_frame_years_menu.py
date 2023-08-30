import customtkinter as ctk
from typing import Tuple, Optional

from .subframes import YearsTableWidget


class YearsMenuBaseFrame(ctk.CTkFrame):
    def __init__(self, master, column_names: Tuple[str], house_id: int,
                 kwargs_default=True, **kwargs):
        if kwargs_default: kwargs.update(corner_radius=0)
        super().__init__(master, **kwargs)

        # grid ================================================================
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure((1, 2, 3), weight=0)
        self.grid_columnconfigure(0, weight=1)

        # table ===============================================================
        self.table = YearsTableWidget(self, column_names, house_id)
        self.table.grid(row=0, column=0, sticky="nsew")

        # scroll for table ====================================================
        self.scroll = ctk.CTkScrollbar(self, command=self.table.yview)
        self.scroll.grid(row=0, column=1, sticky="ns")
        self.table.configure(yscrollcommand=self.scroll.set)

        # entry year ==========================================================
        self.entry_year = ctk.CTkEntry(self, justify="center", width=80)
        self.entry_year.grid(row=1, column=0, columnspan=2, pady=(12, 10))
        # valid input in entry
        val_cmd = (self.register(self._valid_input_year), "%P")
        self.entry_year.configure(validate="key", validatecommand=val_cmd)

        # button add year =====================================================
        self.text_add_btn = ctk.StringVar()
        self.add_btn = ctk.CTkButton(self, textvariable=self.text_add_btn,
                                     width=80)
        self.add_btn.grid(row=2, column=0, columnspan=2, pady=(0, 10))

        # button del year =====================================================
        self.text_del_btn = ctk.StringVar()
        self.del_btn = ctk.CTkButton(self, textvariable=self.text_del_btn,
                                     width=80)
        self.del_btn.grid(row=3, column=0, columnspan=2, pady=(0, 15))

    def _valid_input_year(self, new_value):
        # isdigit()
        allowed_chars = set("0123456789")
        if not all(c in allowed_chars for c in new_value):
            return False

        if new_value.startswith("0"):
            return False

        # Truncate input if it exceeds 20 characters
        if len(new_value) > 4:
            self.entry_year.delete(4, "end")
            return False

        return True

    def clear_input(self):
        self.entry_year.delete(0, "end")

    def get_input(self) -> Optional[int]:
        new_year = self.entry_year.get()
        if new_year:
            return int(new_year)
        else:
            return None
