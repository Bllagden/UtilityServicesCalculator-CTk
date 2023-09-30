import customtkinter as ctk
from typing import Optional

from view.localization import Localization
from view.windows import MessageBox


class MenuBaseFrame(ctk.CTkFrame):
    def __init__(self, master, language: str, kwargs_default=True, **kwargs):
        if kwargs_default: kwargs.update(corner_radius=0)
        super().__init__(master, **kwargs)

        self.localiz_mes_box = Localization(language).get_meters_win_mes_box()

        # grid ================================================================
        self.grid_rowconfigure((0, 1, 2, 4), weight=0)
        self.grid_rowconfigure(3, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # label menu ==========================================================
        self.text_label_menu = ctk.StringVar()
        self._label_menu = ctk.CTkLabel(self, textvariable=self.text_label_menu)
        self._label_menu.grid(row=0, column=0, pady=(10, 0))

        # entry name ==========================================================
        self._entry_name = ctk.CTkEntry(self)
        self._entry_name.grid(row=1, column=0, pady=(10, 10))

        # button create =======================================================
        self.text_add_btn = ctk.StringVar()
        self.btn_add = ctk.CTkButton(self, textvariable=self.text_add_btn,
                                     command=self._tmp_btn_clicked)
        self.btn_add.grid(row=2, column=0)

        # button rename =======================================================
        self.text_rename_btn = ctk.StringVar()
        self.btn_change = ctk.CTkButton(self, textvariable=self.text_rename_btn,
                                        command=self._tmp_btn_clicked)
        self.btn_change.grid(row=3, column=0)

        # button delete =======================================================
        self.text_del_btn = ctk.StringVar()
        self.btn_del = ctk.CTkButton(self, textvariable=self.text_del_btn,
                                     command=self._tmp_btn_clicked)
        self.btn_del.grid(row=4, column=0, pady=(0, 20))

    def get_input(self) -> Optional[str]:
        data = self._entry_name.get()
        if data:
            return data
        else:
            return None

    def _tmp_btn_clicked(self):
        MessageBox(self, "X", self.localiz_mes_box["xxx"])
