import customtkinter as ctk
from typing import Tuple, Dict

from .subframes import ElecWaterGasFrame
from .subframes import GarbageFrame
from .subframes import OverallFrame


class MeterReadingsBaseFrame(ctk.CTkScrollableFrame):
    def __init__(self, master,
                 tabview_tabs: Tuple[str, str, str, str, str],
                 language: str,
                 house_id: int,
                 text_titles: Tuple[str, str],
                 tab_cols_elec_wat_gas: Tuple[
                     Tuple[str, str, str, str, str, str], Tuple[str, str, str]],
                 tab_cols_garb: Tuple[Tuple[str, str, str], Tuple[str, str]],
                 month_names: Tuple[str, ...],
                 localiz_mes_box_reads: Dict,
                 kwargs_default=True, **kwargs):
        if kwargs_default:
            kwargs.update(corner_radius=0,
                          fg_color="transparent",
                          orientation="horizontal")
        super().__init__(master, **kwargs)

        self.localiz_mes_box_reads = localiz_mes_box_reads
        self.grid_columnconfigure(0, weight=1)

        # tabview =============================================================
        self.tabview = ctk.CTkTabview(self, width=750, fg_color="#242424")

        self.text_elec_tab = tabview_tabs[0]
        self.text_wat_tab = tabview_tabs[1]
        self.text_gas_tab = tabview_tabs[2]
        self.text_garb_tab = tabview_tabs[3]
        self.text_all_tab = tabview_tabs[4]

        self.tabview.add(self.text_elec_tab)
        self.tabview.add(self.text_wat_tab)
        self.tabview.add(self.text_gas_tab)
        self.tabview.add(self.text_garb_tab)
        self.tabview.add(self.text_all_tab)
        self.tabview.grid(row=0, column=0, sticky="nsew")

        # electricity frame ===================================================
        self.elec = ElecWaterGasFrame(self.tabview.tab(self.text_elec_tab),
                                      master,
                                      language,
                                      house_id,
                                      "elec",
                                      text_titles,
                                      tab_cols_elec_wat_gas,
                                      month_names,
                                      self.localiz_mes_box_reads)
        self.elec.pack()

        # water frame =========================================================
        self.wat = ElecWaterGasFrame(self.tabview.tab(self.text_wat_tab),
                                     master,
                                     language,
                                     house_id,
                                     "wat",
                                     text_titles,
                                     tab_cols_elec_wat_gas,
                                     month_names,
                                     self.localiz_mes_box_reads)
        self.wat.pack()

        # gas frame ===========================================================
        self.gas = ElecWaterGasFrame(self.tabview.tab(self.text_gas_tab),
                                     master,
                                     language,
                                     house_id,
                                     "gas",
                                     text_titles,
                                     tab_cols_elec_wat_gas,
                                     month_names,
                                     self.localiz_mes_box_reads)
        self.gas.pack()

        # garbage frame =======================================================
        self.garb = GarbageFrame(self.tabview.tab(self.text_garb_tab),
                                 master,
                                 language,
                                 house_id,
                                 "garb",
                                 text_titles,
                                 tab_cols_garb,
                                 month_names,
                                 self.localiz_mes_box_reads)
        self.garb.pack()

        # all types frame =====================================================
        self.all_types = OverallFrame(self.tabview.tab(self.text_all_tab))
        self.all_types.pack()

    def clear_input(self):
        """Clears inputted readings (entries) and selected rates (comboboxes)"""
        self._clear_input_readings()
        self._clear_selected_tariffs()

    def _clear_input_readings(self):
        self.elec.change_data.readings_entries_header.clear()
        self.elec.change_data.readings_entries_main.clear()
        self.wat.change_data.readings_entries_header.clear()
        self.wat.change_data.readings_entries_main.clear()
        self.gas.change_data.readings_entries_header.clear()
        self.gas.change_data.readings_entries_main.clear()

    def _clear_selected_tariffs(self):
        self.elec.change_data.tariffs_comboboxes_main.clear()
        self.wat.change_data.tariffs_comboboxes_main.clear()
        self.gas.change_data.tariffs_comboboxes_main.clear()
        self.garb.change_data.tariffs_comboboxes_main.clear()
