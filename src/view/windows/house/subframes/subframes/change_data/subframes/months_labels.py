import customtkinter as ctk
from typing import Tuple

from src.view.win_settings import IsValid


class MonthsLabelsFrame(ctk.CTkFrame):
    """Frame with the names of the months in a column (HEADER - December only).

    valid frame parts: 'HEADER', 'MAIN_BODY'."""

    def __init__(self, master, frame_part: str, month_names: Tuple[str, ...],
                 kwargs_default=True, **kwargs):
        if kwargs_default: kwargs.update(fg_color="transparent")
        super().__init__(master, **kwargs)

        # is frame_part a valid ===============================================
        self._frame_part = frame_part
        IsValid(self._frame_part).validate_frame_part()

        # creating labels =====================================================
        self._month_names = month_names

        if self._frame_part == "HEADER":
            self._month_label_0 = self._create_label(self._month_names[11])
            self._month_label_0.grid(row=0, column=0, sticky="ew")

        elif self._frame_part == "MAIN_BODY":
            self._month_label_1 = self._create_label(self._month_names[0])
            self._month_label_2 = self._create_label(self._month_names[1])
            self._month_label_3 = self._create_label(self._month_names[2])
            self._month_label_4 = self._create_label(self._month_names[3])
            self._month_label_5 = self._create_label(self._month_names[4])
            self._month_label_6 = self._create_label(self._month_names[5])
            self._month_label_7 = self._create_label(self._month_names[6])
            self._month_label_8 = self._create_label(self._month_names[7])
            self._month_label_9 = self._create_label(self._month_names[8])
            self._month_label_10 = self._create_label(self._month_names[9])
            self._month_label_11 = self._create_label(self._month_names[10])
            self._month_label_12 = self._create_label(self._month_names[11])

            self._month_label_1.grid(row=0, column=0, sticky="ew")
            self._month_label_2.grid(row=1, column=0, sticky="ew")
            self._month_label_3.grid(row=2, column=0, sticky="ew")
            self._month_label_4.grid(row=3, column=0, sticky="ew")
            self._month_label_5.grid(row=4, column=0, sticky="ew")
            self._month_label_6.grid(row=5, column=0, sticky="ew")
            self._month_label_7.grid(row=6, column=0, sticky="ew")
            self._month_label_8.grid(row=7, column=0, sticky="ew")
            self._month_label_9.grid(row=8, column=0, sticky="ew")
            self._month_label_10.grid(row=9, column=0, sticky="ew")
            self._month_label_11.grid(row=10, column=0, sticky="ew")
            self._month_label_12.grid(row=11, column=0, sticky="ew")

    def _create_label(self, text):
        label = ctk.CTkLabel(self,
                             text=f"  {text}",
                             anchor="w",
                             width=80,  # 90
                             fg_color="#343638")
        return label
