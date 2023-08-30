import customtkinter as ctk

from src.view.win_settings import IsValid

from .table_houses import HousesTableWidget
from .table_tariffs import TariffsTableWidget


class DataFrame(ctk.CTkFrame):
    """Left part of base frames (houses and tariffs).
    valid frame types: 'HOUSES', 'TARIFFS'."""

    def __init__(self, master, frame_type: str, kwargs_default=True, **kwargs):
        if kwargs_default:
            kwargs.update(corner_radius=0, fg_color="transparent")
        super().__init__(master, **kwargs)

        # is frame_type a valid ===============================================
        self._frame_type = frame_type
        IsValid(self._frame_type).validate_frame_type()

        # grid ================================================================
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # table ===============================================================
        self.table = None
        self._create_table()

        # scroll for table ====================================================
        self._scroll = None
        self._create_scroll()

        # button ==============================================================
        if self._frame_type == "HOUSES":
            self._btn_frame = None
            self.btn_open = None
            self.text_open_btn = ctk.StringVar()
            self._create_btn()

    def _create_table(self):
        if self._frame_type == "HOUSES":
            self.table = HousesTableWidget(self)
        elif self._frame_type == "TARIFFS":
            self.table = TariffsTableWidget(self)

        self.table.grid(row=0, column=0, sticky="nsew",
                        padx=(8, 5), pady=(8, 8))

    def _create_scroll(self):
        self._scroll = ctk.CTkScrollbar(self, command=self.table.yview)
        self._scroll.grid(row=0, column=1, sticky="nsew")
        self.table.configure(yscrollcommand=self._scroll.set)

    def _create_btn(self):
        self._btn_frame = ctk.CTkFrame(self,
                                       corner_radius=0,
                                       border_width=0,
                                       height=80)
        self._btn_frame.grid(row=1, column=0, columnspan=2, sticky="nsew")
        self.btn_open = ctk.CTkButton(self._btn_frame,
                                      textvariable=self.text_open_btn)
        self.btn_open.pack(pady=(9, 9))
