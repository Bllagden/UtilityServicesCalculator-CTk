import customtkinter as ctk
from typing import List, Dict, Optional

from src.view.windows import MessageBox
from src.view.windows import MetersWindow


class MetersMenuFrame(ctk.CTkFrame):
    """A frame with the selection and settings of counters."""

    def __init__(self, master, master_window, language: str, house_id: int,
                 tariffs_tag: str, localiz_mes_box_reads: Dict,
                 kwargs_default=True, **kwargs):
        if kwargs_default: kwargs.update(fg_color="transparent")
        super().__init__(master, **kwargs)

        self._master = master_window
        self._language = language
        self._house_id = house_id
        self._tariffs_tag = tariffs_tag
        self.localiz_mes_box_reads = localiz_mes_box_reads
        self.selected_year: Optional[int] = None

        # option menu =========================================================
        self.text_inactive_menu = ctk.StringVar()
        self.text_cur_menu = ctk.StringVar()

        self.menu_meters_choice = ctk.CTkOptionMenu(self, width=130,
                                                    variable=self.text_cur_menu,
                                                    state="disabled")
        self.menu_meters_choice.grid(row=0, column=1, padx=(0, 5))

        # button ==============================================================
        self.text_params_btn = ctk.StringVar()
        self.btn_params = ctk.CTkButton(self, width=90,
                                        textvariable=self.text_params_btn,
                                        command=self.open_meters_btn_clicked)
        self.btn_params.grid(row=0, column=2, padx=(5, 0))

    def open_meters_btn_clicked(self):
        if self.selected_year is None:
            MessageBox(self, self.localiz_mes_box_reads["error_opening"],
                       self.localiz_mes_box_reads["year_select"])
        else:
            self._open_window_meters()

    def _open_window_meters(self):
        """
        A window for setting meters for the selected house, year and type opens.

        house_window is disabled because for some reason grab_set() only works
        on the first click (so '-disabled' instead of grub_set())."""
        self._master.attributes("-disabled", 1)
        self._meters_window = MetersWindow(self._master,
                                           self._language,
                                           self._house_id,
                                           self.selected_year,
                                           self._tariffs_tag)
        self._meters_window.protocol("WM_DELETE_WINDOW",
                                     self._close_window_meters)

    def _close_window_meters(self):
        self._meters_window.destroy()
        self._master.attributes("-disabled", 0)
        self._master.deiconify()

    def activate(self, values: List[str]):
        """Аctivate meters menu (it can be opened).
        Call from outside if the year is selected."""
        self.text_cur_menu.set(values[0])
        self.menu_meters_choice.configure(state="normal", values=values)

    def deactivate(self):
        """Deactivate meters menu (it can't be opened).
        Call from outside if the year selection is reset."""
        self.text_cur_menu.set(self.text_inactive_menu.get())
        self.menu_meters_choice.configure(state="disabled")

    def get_meter_name(self) -> str:
        return self.menu_meters_choice.get()
