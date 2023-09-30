from typing import List, Tuple, Optional

from view.table_widget import TableMasterWidget
from view.table_widget import TableStyles


class ElecWatGasTableWidget(TableMasterWidget):
    def __init__(self, master,
                 column_names: Tuple[str, str, str, str, str, str],
                 month_names: Tuple[str, ...],
                 **kwargs):

        column_tags = (
            "num", "month", "meter_readings", "consumption", "tariff", "price")
        super().__init__(master, column_tags, column_names, **kwargs)

        self._month_names = month_names
        self.update_tab()

    def _apply_style(self):
        self.configure(style=TableStyles().calc_style(), height=12)

    def _layout_table(self):
        _width = int(self._column_width / 5)  # 30
        self.column(self._column_tags[0], width=30, anchor="center")

        width = 75  # int(self._column_width / 2)
        self.column(self._column_tags[1], width=width, anchor="w")
        self.column(self._column_tags[2], width=width, anchor="e")
        self.column(self._column_tags[3], width=80, anchor="e")
        self.column(self._column_tags[4], width=width, anchor="e")
        self.column(self._column_tags[5], width=width, anchor="e")

    def _init_table(self):
        """Without sorting columns."""
        for i, tag in enumerate(self._column_tags):
            self.heading(tag, text=self._column_names[i])

    def update_tab(self, values: Optional[List] = None):
        self.delete(*self.get_children())
        if not values: values = self._control_api.get_base_tab_elec_wat_gas()[1]
        self._fill_table_row_by_row(values)

    def _fill_table_row_by_row(self, values):
        """A month is added."""
        for i, row in enumerate(values):
            new_row = [row[0], self._month_names[i], row[1], row[2], row[3],
                       row[4]]
            self.insert(parent="", index="end", values=new_row)
