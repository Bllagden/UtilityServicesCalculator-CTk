import customtkinter as ctk


class TitleFrame(ctk.CTkFrame):
    def __init__(self, master, text: str, kwargs_default=True, **kwargs):
        if kwargs_default: kwargs.update(fg_color="transparent")
        super().__init__(master, **kwargs)

        self._text = text

        self._f_title = ctk.CTkLabel(self, text=self._text)
        self._f_title.pack()
