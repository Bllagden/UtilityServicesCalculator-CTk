from typing import Dict

# main window
from .text_main_win import LANG_MAIN_WIN
from .text_main_win import LANG_MAIN_WIN_MES_BOX_HOUSES
from .text_main_win import LANG_MAIN_WIN_MES_BOX_TARIFFS

# house window
from .text_house_win import LANG_HOUSE_WIN_PARAMS
from .text_house_win import LANG_HOUSE_WIN_TK_VARS
from .text_house_win import LANG_HOUSE_WIN_MES_BOX_YEARS
from .text_house_win import LANG_HOUSE_WIN_MES_BOX_READS

# meters window
from .text_meters_win import LANG_METERS_WIN_PARAMS
from .text_meters_win import LANG_METERS_WIN_TK_VARS
from .text_meters_win import LANG_METERS_WIN_MES_BOX


class Localization:
    """Class for interface localization."""
    valid_langs = {"RU", "ENG"}

    def __init__(self, language: str):
        self._language = language
        self._valid_language()

    def _valid_language(self):
        if self._language not in Localization.valid_langs:
            raise ValueError(
                f"wrong language: self.language = {self._language}")

    # main window =============================================================
    def get_main_win(self) -> Dict:
        return LANG_MAIN_WIN[self._language]

    def get_main_win_mes_box_houses(self) -> Dict:
        return LANG_MAIN_WIN_MES_BOX_HOUSES[self._language]

    def get_main_win_mes_box_tariffs(self) -> Dict:
        return LANG_MAIN_WIN_MES_BOX_TARIFFS[self._language]

    # house window ============================================================
    def get_house_win_params(self) -> Dict:
        return LANG_HOUSE_WIN_PARAMS[self._language]

    def get_house_win_tk_vars(self) -> Dict:
        return LANG_HOUSE_WIN_TK_VARS[self._language]

    def get_house_win_mes_box_years(self) -> Dict:
        return LANG_HOUSE_WIN_MES_BOX_YEARS[self._language]

    def get_house_win_mes_box_reads(self) -> Dict:
        return LANG_HOUSE_WIN_MES_BOX_READS[self._language]

    # meters window ===========================================================
    def get_meters_win_params(self) -> Dict:
        return LANG_METERS_WIN_PARAMS[self._language]

    def get_meters_win_tk_vars(self) -> Dict:
        return LANG_METERS_WIN_TK_VARS[self._language]

    def get_meters_win_mes_box(self) -> Dict:
        return LANG_METERS_WIN_MES_BOX[self._language]
