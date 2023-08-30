import customtkinter as ctk
import os
from PIL import Image


class NavigationBaseFrame(ctk.CTkFrame):
    """Navigation menu for selecting language and frames (houses, tariffs)."""

    def __init__(self, master, kwargs_default=True, **kwargs):
        if kwargs_default: kwargs.update(corner_radius=0)
        super().__init__(master, **kwargs)

        # load imgs ===========================================================
        self._image_houses = None
        self._image_tariffs = None
        self._load_imgs()

        # houses button =======================================================
        self.text_houses_btn = ctk.StringVar()

        self.houses_btn = self._create_menu_btn(self.text_houses_btn,
                                                self._image_houses)
        self.houses_btn.grid(row=0, column=0, sticky="ew")

        # tariffs button ======================================================
        self.text_tariffs_btn = ctk.StringVar()

        self.tariffs_btn = self._create_menu_btn(self.text_tariffs_btn,
                                                 self._image_tariffs)
        self.tariffs_btn.grid(row=1, column=0, sticky="ew")

        # language selection ==================================================
        self.lang_menu = ctk.CTkOptionMenu(self,
                                           width=90,
                                           values=["RU", "ENG"])
        self.lang_menu.grid(row=6, column=0, sticky="s", padx=20, pady=20)

    def _load_imgs(self):
        image_path = os.path.join(os.path.dirname(
            os.path.realpath(__file__)), "imgs")

        self._image_houses = ctk.CTkImage(
            dark_image=Image.open(os.path.join(image_path, "houses.png")),
            size=(30, 30))  # 20 20
        self._image_tariffs = ctk.CTkImage(
            dark_image=Image.open(os.path.join(image_path, "tariffs.png")),
            size=(30, 30))  # 20 20

    def _create_menu_btn(self, textvar, image):
        btn = ctk.CTkButton(self,
                            corner_radius=0,
                            height=40,
                            width=130,
                            border_spacing=10,
                            textvariable=textvar,
                            fg_color="transparent",
                            text_color=("gray10", "gray90"),
                            hover_color=("gray70", "gray30"),
                            image=image,
                            anchor="w")
        return btn
