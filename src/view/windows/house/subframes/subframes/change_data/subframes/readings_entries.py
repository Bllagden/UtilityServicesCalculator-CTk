import customtkinter as ctk
from typing import List

from view.win_settings import IsValid


class ReadingsEntriesFrame(ctk.CTkFrame):
    """Frame with entries for entering meter readings in a column for each month
    (HEADER - for December only).

    valid frame parts: 'HEADER', 'MAIN_BODY'."""

    def __init__(self, master, frame_part: str, kwargs_default=True, **kwargs):
        if kwargs_default: kwargs.update(fg_color="transparent")
        super().__init__(master, **kwargs)

        # is frame_part a valid ===============================================
        self._frame_part = frame_part
        IsValid(self._frame_part).validate_frame_part()

        # creating entries ====================================================
        if self._frame_part == "HEADER":
            self._readings_0 = self._create_entry()
            self._readings_0.grid(row=0, column=0)

        elif self._frame_part == "MAIN_BODY":
            self._readings_1 = self._create_entry()
            self._readings_2 = self._create_entry()
            self._readings_3 = self._create_entry()
            self._readings_4 = self._create_entry()
            self._readings_5 = self._create_entry()
            self._readings_6 = self._create_entry()
            self._readings_7 = self._create_entry()
            self._readings_8 = self._create_entry()
            self._readings_9 = self._create_entry()
            self._readings_10 = self._create_entry()
            self._readings_11 = self._create_entry()
            self._readings_12 = self._create_entry()

            self._readings_1.grid(row=0, column=0)
            self._readings_2.grid(row=1, column=0)
            self._readings_3.grid(row=2, column=0)
            self._readings_4.grid(row=3, column=0)
            self._readings_5.grid(row=4, column=0)
            self._readings_6.grid(row=5, column=0)
            self._readings_7.grid(row=6, column=0)
            self._readings_8.grid(row=7, column=0)
            self._readings_9.grid(row=8, column=0)
            self._readings_10.grid(row=9, column=0)
            self._readings_11.grid(row=10, column=0)
            self._readings_12.grid(row=11, column=0)

    def _create_entry(self):
        # validatecommand (input in entry)
        val_cmd = (self.register(self._valid_input_entries), "%P")

        entry = ctk.CTkEntry(self,
                             justify="center",
                             validate="key",
                             validatecommand=val_cmd,
                             # corner_radius=0,
                             width=90
                             )
        return entry

    @staticmethod
    def _valid_input_entries(new_value: str):
        allowed_chars = set("0123456789")
        if not all(c in allowed_chars for c in new_value):
            return False

        if new_value.startswith("0") and len(new_value) > 1:
            return False

        if len(new_value) > 10:
            return False
        return True

    def clear(self):
        if self._frame_part == "HEADER":
            self._readings_0.delete(0, "end")

        elif self._frame_part == "MAIN_BODY":
            self._readings_1.delete(0, "end")
            self._readings_2.delete(0, "end")
            self._readings_3.delete(0, "end")
            self._readings_4.delete(0, "end")
            self._readings_5.delete(0, "end")
            self._readings_6.delete(0, "end")
            self._readings_7.delete(0, "end")
            self._readings_8.delete(0, "end")
            self._readings_9.delete(0, "end")
            self._readings_10.delete(0, "end")
            self._readings_11.delete(0, "end")
            self._readings_12.delete(0, "end")

    def get(self) -> List[str]:
        input_readings = []
        if self._frame_part == "HEADER":
            input_readings = [self._readings_0.get()]

        elif self._frame_part == "MAIN_BODY":
            input_readings = [
                self._readings_1.get(),
                self._readings_2.get(),
                self._readings_3.get(),
                self._readings_4.get(),
                self._readings_5.get(),
                self._readings_6.get(),
                self._readings_7.get(),
                self._readings_8.get(),
                self._readings_9.get(),
                self._readings_10.get(),
                self._readings_11.get(),
                self._readings_12.get()
            ]

        return input_readings
