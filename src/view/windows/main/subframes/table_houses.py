from typing import Tuple, Optional

from view.table_widget import TableMasterWidget


class HousesTableWidget(TableMasterWidget):
    def __init__(self, master, **kwargs):
        column_tags = ("house_name", "house_description")
        column_names = ("0", "1")
        super().__init__(master, column_tags, column_names, **kwargs)

        self.update_tab()

    def update_tab(self):
        self.delete(*self.get_children())
        values = self._control_api.get_tab_houses()
        self._fill_table_row_by_row(values)

    def rename_columns(self, value: Tuple[str, str]):
        """Columns are named from outside (used for localization)."""
        for i, tag in enumerate(self._column_tags):
            self.heading(tag, text=value[i])

    def get_name_selected_house(self) -> Optional[str]:
        """
        If a table row is selected, the house name from that row is returned.
        If no table row is selected, None is returned.
        """
        row = self._get_selected_row()
        if row:
            return row[0]
        else:
            return None
