from tkinter import ttk
from typing import List, Tuple, Dict

from controller import ControllerAPI
from .styles import TableStyles
from .sorts import TableSorts


class TableMasterWidget(ttk.Treeview):
    """Table widget based on ttk.Treeview.
    To create a table class, you need to inherit from this class.

    Table styles and column sorting are implemented in separate classes."""

    def __init__(self, master,
                 column_tags: Tuple[str, ...],
                 column_names: Tuple[str, ...],
                 **kwargs):

        kwargs.update(columns=column_tags, show="headings", selectmode="browse")
        super().__init__(master, **kwargs)

        self._control_api = ControllerAPI()

        # style table =========================================================
        self._apply_style()

        # layout table ========================================================
        self._column_tags = column_tags
        self._column_width = 150
        self._layout_table()

        # init table ==========================================================
        self._column_names = column_names
        self._sort_key: str = ""
        self._init_table()

    def _apply_style(self):
        """A style with the desired name is created in the 'TableStyles' class
        (the style now exists) and then its name is passed here."""
        self.configure(style=TableStyles().main_style())

    def _layout_table(self):
        for tag in self._column_tags:
            self.column(tag, width=self._column_width)

    def _init_table(self):
        """Initializing the displayed column names and
        sorting the table by columns."""
        for i, tag in enumerate(self._column_tags):
            self.heading(tag,
                         text=self._column_names[i],
                         command=lambda _i=i: self._sort(_i, False)
                         )

    def _sort(self, col_id: int, reverse: bool):
        """Sort the table by clicking on the column.
        col_id: numeric index of the column: 0 | 1 | ... (by which to sort).
        reverse: sorting order.
        """

        # getting the id of all table rows ====================================
        row_ids: Tuple[str, ...]
        row_ids = self.get_children("")
        # row_ids = ('I001', 'I002') | ()

        # getting the values of the sorted column =============================
        sortable_column: List[Tuple[str, str]]
        sortable_column = [
            (self.set(row_id, col_id), row_id) for row_id in row_ids
        ]
        # sortable_column = [('1,5', 'I001'), ('33,0', 'I002')] | []
        #   in each tuple: column value and row id of this value

        # Sorting by key in TableSorts ========================================
        self._set_sort_key()
        table_sort = TableSorts(
            self.__class__.__name__,  # name of the class that created the table
            self._sort_key,
            sortable_column,
            reverse
        )
        # sorted sortable_column by column values
        sorted_column: List[Tuple] = table_sort.execute_sort()

        # sorted_column = [(33.0, 'I002'), (1.5, 'I001')]
        #   in this case, before sorting, the values were converted
        #   to float and it was sorted by float

        # =====================================================================
        # reordering the values in the table by row_ids after sorting
        for index, (_, row_id) in enumerate(sorted_column):
            self.move(row_id, "", index)

        # =====================================================================
        # the next sorting by this column will be in reverse order
        self.heading(col_id,
                     command=lambda: self._sort(col_id, not reverse))

    def _set_sort_key(self):
        """The choice of a key for sorting, sorting occurs in 'TableSorts'.
        'value' from TableSorts.valid_sort_keys.
        """
        self._sort_key = "str_default"

    def _fill_table_row_by_row(self, values):
        """Complete filling of the table row by row.
        Accepts a list of tuples, where each tuple is a string."""
        for row in values:
            self.insert(parent="", index=0, values=row)

    def _get_selected_row(self) -> List[str]:
        """Returns a list of values of the selected row.
        If the row is not selected, an empty list will be returned."""
        selected_row_id: Tuple[str, ...] = self.selection()  # ('I002',) | ()

        row_values: List[str] = []
        if selected_row_id:
            row_info: Dict = self.item(selected_row_id[0])
            row_values = row_info["values"]

            # Implicit type conversion occurs (int instead of str, if the
            # element can be int). Maybe tkinter does it, maybe sqlite.
            # Just in case, the type of table elem is specified explicitly (str)
            row_values = list(map(str, row_values))
        return row_values
