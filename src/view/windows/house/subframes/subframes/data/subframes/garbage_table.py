from typing import List, Tuple, Optional

from view.table_widget import TableMasterWidget
from view.table_widget import TableStyles


class GarbageTableWidget(TableMasterWidget):
    def __init__(self, master,
                 column_names: Tuple[str, str, str],
                 month_names: Tuple[str, ...],
                 **kwargs):

        column_tags = ("num", "month", "tariff")
        super().__init__(master, column_tags, column_names, **kwargs)

        self._month_names = month_names
        self.update_tab()

    def _apply_style(self):
        self.configure(style=TableStyles().calc_style(), height=12)

    def _layout_table(self):
        self.column(self._column_tags[0], width=int(self._column_width / 5),
                    anchor="center")  # 30
        self.column(self._column_tags[1], width=int(self._column_width / 2),
                    anchor="w")
        self.column(self._column_tags[2], width=int(self._column_width / 1.5),
                    anchor="center")

    def _init_table(self):
        """Without sorting columns."""
        for i, tag in enumerate(self._column_tags):
            self.heading(tag, text=self._column_names[i])

    def update_tab(self, values: Optional[List] = None):
        self.delete(*self.get_children())
        if not values: values = self._control_api.get_base_tab_garb()
        self._fill_table_row_by_row(values)

    def _fill_table_row_by_row(self, values):
        """A month is added."""
        for i, row in enumerate(values):
            new_row = [row[0], self._month_names[i], row[1]]
            self.insert(parent="", index="end", values=new_row)
