import customtkinter as ctk
from typing import Tuple, Optional

from src.view.win_settings import IsValid


class MenuFrame(ctk.CTkFrame):
    """Right part of base frames (houses and tariffs).
    valid frame types: 'HOUSES', 'TARIFFS'."""

    def __init__(self,
                 master,
                 frame_type: str,
                 kwargs_default=True,
                 **kwargs
                 ):
        if kwargs_default: kwargs.update(corner_radius=0)
        super().__init__(master, **kwargs)

        # is frame_type a valid ===============================================
        self._frame_type = frame_type
        IsValid(self._frame_type).validate_frame_type()

        # grid ================================================================
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)
        self.grid_rowconfigure((0, 1, 2, 3), weight=0)
        self.grid_rowconfigure(4, weight=1)

        # label ===============================================================
        self.text_label_menu = ctk.StringVar()
        self._label_menu = None
        self._create_label()

        # create fields: ======================================================
        # 1) house name entry OR tariff type combobox
        # 2) house description entry OR tariff value entry
        self.text_field_1 = ctk.StringVar()
        self.text_field_2 = ctk.StringVar()

        if self._frame_type == "HOUSES":
            self._entry_house_name = None
            self._entry_house_desc = None
        elif self._frame_type == "TARIFFS":
            self._combobox_tariff_type = None
            self._entry_tariff_value = None
            self.text_tariff_type = ctk.StringVar()
        self._create_fields()

        # valid input entry ===================================================
        self._pressed_keys = set()
        self._bind_handlers()

        # buttons =============================================================
        self.text_add_btn = ctk.StringVar()
        self.text_del_btn = ctk.StringVar()
        self.btn_add = None
        self.btn_del = None
        self._create_buttons()

    def _create_label(self):
        self._label_menu = ctk.CTkLabel(self, textvariable=self.text_label_menu)
        self._label_menu.grid(row=0, column=0, sticky="ew", pady=20)

    def _create_fields(self):
        if self._frame_type == "HOUSES":
            self._entry_house_name = ctk.CTkEntry(self, justify="center")
            self._entry_house_desc = ctk.CTkEntry(self, justify="center")

            self._entry_house_name.grid(row=1, column=0, sticky="ew",
                                        padx=20)
            self._entry_house_desc.grid(row=2, column=0, sticky="ew",
                                        padx=20, pady=10)

        elif self._frame_type == "TARIFFS":
            values = ["1", "2", "3", "4"]
            self._combobox_tariff_type = ctk.CTkComboBox(self,
                                                         values=values,
                                                         state="readonly")
            self._entry_tariff_value = ctk.CTkEntry(self, justify="center")

            self._combobox_tariff_type.grid(row=1, column=0, sticky="ew",
                                            padx=20)
            self._entry_tariff_value.grid(row=2, column=0, sticky="ew",
                                          padx=20, pady=10)

    def rename_fields(self, values):
        """For localization."""
        if self._frame_type == "HOUSES":
            self._entry_house_name.configure(placeholder_text=values[0])
            self._entry_house_desc.configure(placeholder_text=values[1])

        elif self._frame_type == "TARIFFS":
            self._combobox_tariff_type.set(values[0])
            self._combobox_tariff_type.configure(values=values[1])
            self._entry_tariff_value.configure(placeholder_text=values[2])

    def _create_buttons(self):
        self.btn_add = ctk.CTkButton(self, textvariable=self.text_add_btn)
        self.btn_del = ctk.CTkButton(self, textvariable=self.text_del_btn)

        self.btn_add.grid(row=3, column=0)
        self.btn_del.grid(row=4, column=0, sticky="s", pady=20)

    def clear_input(self):
        if self._frame_type == "HOUSES":
            self._entry_house_name.delete(0, "end")
            self._entry_house_desc.delete(0, "end")

        elif self._frame_type == "TARIFFS":
            # self._combobox_tariff_type.set(self.text_label.get())
            self._entry_tariff_value.delete(0, "end")

    def get_input(self) -> Tuple[Optional[str], Optional[str]]:
        if self._frame_type == "HOUSES":
            house_name: str = self._entry_house_name.get()
            house_desc: str = self._entry_house_desc.get()

            valid_house_name: Optional[str] = \
                self._check_houses_input(house_name)
            valid_house_desc: Optional[str] = \
                self._check_houses_input(house_desc)
            return valid_house_name, valid_house_desc

        elif self._frame_type == "TARIFFS":
            tariff_type: str = self._combobox_tariff_type.get()
            tariff_value: str = self._entry_tariff_value.get()

            valid_tariff_type: Optional[str] = \
                self._check_tariffs_input(tariff_type)
            valid_tariff_value: Optional[str] = \
                self._check_tariffs_input(tariff_value)
            return valid_tariff_type, valid_tariff_value

    @staticmethod
    def _check_houses_input(item: str) -> Optional[str]:
        if not item:
            return None
        else:
            return item

    def _check_tariffs_input(self, item: str) -> Optional[str]:
        if not item or item == self.text_tariff_type.get():
            return None
        else:
            return item

    # handlers for entries ====================================================
    #
    #   * handlers are used instead of the validatecommand param because
    #   it fails to save placeholder_text after activating entry
    #

    def _bind_handlers(self):
        if self._frame_type == "HOUSES":
            self._bind_for_houses()
        elif self._frame_type == "TARIFFS":
            self._bind_for_tariffs()

    def _bind_for_houses(self):
        self._entry_house_name.bind("<KeyPress>",
                                    self._handler_on_key_press_all)
        self._entry_house_desc.bind("<KeyPress>",
                                    self._handler_on_key_press_all)
        self._entry_house_name.bind("<KeyRelease>",
                                    self._handler_on_key_release_hs)
        self._entry_house_desc.bind("<KeyRelease>",
                                    self._handler_on_key_release_hs)
        self._entry_house_name.bind("<<Paste>>", self._handler_on_paste_hs)
        self._entry_house_desc.bind("<<Paste>>", self._handler_on_paste_hs)

    def _bind_for_tariffs(self):
        self._entry_tariff_value.bind("<Key>", self._handler_on_key_trf)
        self._entry_tariff_value.bind("<KeyPress>",
                                      self._handler_on_key_press_all)
        self._entry_tariff_value.bind("<KeyRelease>",
                                      self._handler_on_key_release_trf)
        self._entry_tariff_value.bind("<<Paste>>", self._handler_on_paste_trf)

    @staticmethod
    def _handler_on_key_trf(event):
        """key press"""
        control_keys = {"BackSpace", "Left", "Right", "Home", "End", "Delete"}
        if event.keysym in control_keys:
            return

        allowed_chars = set("0123456789,.")
        if event.char not in allowed_chars:
            return "break"

    def _handler_on_key_press_all(self, event):
        """key holding"""
        control_keys = {"BackSpace", "Left", "Right", "Delete"}

        if event.keysym in control_keys:
            return

        if event.keysym not in self._pressed_keys:
            self._pressed_keys.add(event.keysym)
        else:
            return "break"

    def _handler_on_key_release_hs(self, event):
        """key release"""
        self._pressed_keys.discard(event.keysym)
        current_text = event.widget.get()

        if current_text.startswith("0"):
            new_text = current_text[1:]
        else:
            new_text = current_text

        if len(new_text) > 40:
            new_text = new_text[:40]

        if new_text != current_text:
            event.widget.delete(0, "end")
            event.widget.insert(0, new_text)

    def _handler_on_key_release_trf(self, event):
        """key release.

        Events:
        * '0', 'dot' and 'comma' are del if entered at the beginning of the line
        * duplicate 'dots' and 'commas' are removed
        * the length of the str is 15 characters (the extra ones are removed)

        By deleting characters, we mean creating a new line without them,
        and placing this line in entry instead of the original one."""
        self._pressed_keys.discard(event.keysym)
        current_text = event.widget.get()

        if current_text.startswith(("0", ",", ".")):
            new_text = current_text[1:]
        else:
            new_text = current_text

        # remove extra commas and dots
        if ("," in new_text and "." in new_text) or \
                new_text.count(",") > 1 or new_text.count(".") > 1:
            i = min(new_text.find(","), new_text.find("."))
            left_new_text = new_text[:i + 1]
            right_new_text = "".join(
                c for c in new_text[i + 1:] if c not in (",", "."))

            new_text = "".join((left_new_text, right_new_text))

        # correct output of insignificant zeros at the end
        sep = None
        if "," in new_text:
            sep = ","
        elif "." in new_text:
            sep = "."

        if sep is not None:
            integer_part, fractional_part = new_text.split(sep)
            if len(fractional_part) > 1:
                fractional_part = fractional_part.rstrip("0")
            new_text = sep.join((integer_part, fractional_part))

        # if only zero
        if new_text == "0":
            new_text = ""

        if len(new_text) > 15:
            new_text = new_text[:15]

        # overwriting
        if new_text != current_text:
            event.widget.delete(0, "end")
            event.widget.insert(0, new_text)

    @staticmethod
    def _handler_on_paste_hs(event):
        """paste text"""
        widget = event.widget
        current_text = widget.get()
        clipboard_text = widget.clipboard_get()
        new_text = "".join((current_text, clipboard_text))
        if new_text.startswith("0"):
            new_text = new_text.lstrip("0")
        widget.delete(0, "end")
        widget.insert(0, new_text)
        return "break"

    @staticmethod
    def _handler_on_paste_trf(event):
        """paste text.
        You cannot insert text containing at the beginning: '0', 'comma', 'dot'.
        """
        widget = event.widget
        current_text = widget.get()
        clipboard_text = widget.clipboard_get()
        new_text = "".join((current_text, clipboard_text))

        if new_text.startswith(("0", ",", ".")):
            new_text = ""

        allowed_chars = set("0123456789")
        for i in new_text:
            if i not in allowed_chars:
                new_text = ""
                break

        widget.delete(0, "end")
        widget.insert(0, new_text)
        return "break"
