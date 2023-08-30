from typing import List, Tuple, Optional

from src.view.table_widget import TableMasterWidget


class TariffsTableWidget(TableMasterWidget):
    def __init__(self, master, **kwargs):
        column_tags = ("tariff_type", "tariff_value")
        column_names = ("0", "1")
        super().__init__(master, column_tags, column_names, **kwargs)

        self.tariff_types = ["0", "1", "2", "3"]  # will be named from outside
        self.update_tab()

    def _set_sort_key(self):
        self._sort_key = "str_or_float_swap_comma_dot"

    def update_tab(self):
        """
        vals:      [('elec', '4,0'), ('wat', '3,28')]
        new_vals:  [('Electricity', '4,0'), ('Water', '3,28')]
        """
        self.delete(*self.get_children())
        vals: List[Tuple[str, str]] = self._control_api.get_tab_tariffs()
        new_vals: List[Tuple[str, str]]
        new_vals = [(self._get_tariff_type(tup[0]), tup[1]) for tup in vals]
        self._fill_table_row_by_row(new_vals)

    def _get_tariff_type(self, tag):
        """'elec' -> 'Electricity'
             tag  -> self.tariff_types[i]"""
        tariff_tags = ["elec", "wat", "gas", "garb"]
        if tariff_tags[0] == tag:
            return self.tariff_types[0]
        elif tariff_tags[1] == tag:
            return self.tariff_types[1]
        elif tariff_tags[2] == tag:
            return self.tariff_types[2]
        elif tariff_tags[3] == tag:
            return self.tariff_types[3]
        else:
            raise ValueError(f"Wrong tag. Valid tags: {tariff_tags}")

    def rename_columns(self, value: Tuple[str, str]):
        """Columns are named from outside (used for localization)."""
        for i, tag in enumerate(self._column_tags):
            self.heading(tag, text=value[i])

    def get_selected_tariff(self) -> Optional[List[str]]:
        """
        If a table row is selected, the tariff type and value of that row
        are returned. If no table row is selected, None is returned."""
        row = self._get_selected_row()
        if row:
            return row
        else:
            return None
