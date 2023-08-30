import customtkinter as ctk


class OverallFrame(ctk.CTkFrame):
    def __init__(self, master, kwargs_default=True, **kwargs):
        if kwargs_default:
            kwargs.update(corner_radius=0, fg_color="transparent")
        super().__init__(master, **kwargs)

        self.textbox = ctk.CTkTextbox(master=self, width=400, corner_radius=0,
                                      fg_color="transparent")
        self.textbox.grid(row=0, column=0, sticky="nsew", pady=(150, 0))
