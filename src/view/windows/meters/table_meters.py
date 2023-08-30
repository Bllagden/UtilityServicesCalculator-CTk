from typing import Tuple, Optional

from src.view.table_widget import TableMasterWidget


class MetersTableWidget(TableMasterWidget):
    def __init__(self, master,
                 column_names: Tuple[str],
                 house_id: int, year: int, meter_type: str,
                 **kwargs):

        column_tags = ("meter_name",)
        super().__init__(master, column_tags, column_names, **kwargs)

        self._house_id = house_id
        self._year = year
        self._meter_type = meter_type
        self.update_tab()

    def _layout_table(self):
        self.column(self._column_tags[0], width=200, anchor="center")

    def update_tab(self):
        self.delete(*self.get_children())
        values = self._control_api.get_tab_meters(self._house_id,
                                                  self._year,
                                                  self._meter_type)
        self._fill_table_row_by_row(values)

    def get_name_selected_meter(self) -> Optional[str]:
        """
        If a table row is selected, the meter name from that row is returned.
        If no table row is selected, None is returned.
        """
        row = self._get_selected_row()
        if row:
            return row[0]
        else:
            return None
