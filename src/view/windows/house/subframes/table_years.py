from typing import Tuple, Optional

from view.table_widget import TableMasterWidget
from view.table_widget import TableStyles


class YearsTableWidget(TableMasterWidget):
    def __init__(self, master, column_names: Tuple[str], house_id: int,
                 **kwargs):
        column_tags = ("year",)
        super().__init__(master, column_tags, column_names, **kwargs)

        self._house_id = house_id
        self.update_tab()

    def _apply_style(self):
        self.configure(style=TableStyles().years_style())

    def _layout_table(self):
        self.column(self._column_tags[0], width=90, anchor="center")

    def _set_sort_key(self):
        self._sort_key = "int"

    def update_tab(self):
        self.delete(*self.get_children())
        values = self._control_api.get_tab_years(self._house_id)
        self._fill_table_row_by_row(values)

    def get_selected_year(self) -> Optional[int]:
        """
        If a table row is selected, the year from that row is returned.
        If no table row is selected, None is returned.
        """
        row = self._get_selected_row()
        if row:
            return int(row[0])
        else:
            return None
