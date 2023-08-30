import customtkinter as ctk

from src.view.win_settings import center_window


class MessageBox(ctk.CTkToplevel):
    def __init__(self, master, title_in: str, message_in: str):
        super().__init__(master)

        self.title(title_in)
        self._congigure_gui()
        self.protocol("WM_DELETE_WINDOW", self._close_message_box)

        # grid ================================================================
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # label ===============================================================
        self._label = ctk.CTkLabel(self, text=message_in)
        self._label.grid(row=0, column=0, sticky="nsew")

        # button ==============================================================
        self.button = ctk.CTkButton(self, text="OK",
                                    command=self._close_message_box)
        self.button.grid(row=1, column=0)

    def _congigure_gui(self):
        """When using the grab_set() and transient() methods together, there
        were problems when minimizing windows. If message_box is open in the
        current program, then when minimizing all windows in the OS at a time,
        not a single window of the current program will not expand
        (neither parent nor message_box). Therefore, instead of the transient()
        method, the attributes() method is used.

        1) The grab_set() method is used to implement a modal window and
        inability to use the parent window at this moment.
        2) The transient() method is used to set the parent window for
        child. The child window will always be displayed on top of the parent
        window windows and will be without collapse/expand buttons.
        3) The attributes() method with the '-toolwindow' attribute allows you
        to set the window is like a tool window, which will remove
        the collapse/expand buttons."""
        self.grab_set()
        self.attributes("-toolwindow", 1)

        center_window(self, 250, 130)
        self.resizable(False, False)

    def _close_message_box(self):
        self.grab_release()
        self.destroy()
