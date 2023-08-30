from typing import List, Tuple, Union


class TableSorts:
    """The class gets the values to sort and the sort key.
    Depending on the sort key, the values are converted (for example,
    string numbers in int or float to sort non-lexicographically)
    and are sorted. Then they are returned in sorted form.
    """
    valid_sort_keys = {
        "str_default",
        "int",
        "str_or_float_swap_comma_dot"
    }

    def __init__(self, caller_class: str, sort_key: str,
                 sortable_column: List[Tuple[str, str]], reverse: bool):

        self._caller_class = caller_class
        self._sort_key = sort_key
        self._validate_sort_key()

        self._sortable_column = sortable_column
        self._reverse = reverse

    def _validate_sort_key(self):
        f = f"sort_key '{self._sort_key}' not in {TableSorts.valid_sort_keys}." \
            f"\nclass with wrong sort_key: {self._caller_class}."
        if self._sort_key not in TableSorts.valid_sort_keys:
            raise ValueError(f)

    def execute_sort(self):
        result = self._convert_values()
        result.sort(reverse=self._reverse)
        return result

    def _convert_values(self):
        """Converting sorted values before sorting."""
        result = []
        if self._sort_key == "str_default":
            result = self._str_default()
        elif self._sort_key == "int":
            result = self._int_convert()
        elif self._sort_key == "str_or_float_swap_comma_dot":
            result = self._str_or_float_swap_comma_dot_convert()
        return result

    def _str_default(self) -> List[Tuple[str, str]]:
        """Already str"""
        return self._sortable_column

    def _int_convert(self) -> List[Tuple[int, str]]:
        """str -> int"""
        tmp_lst = self._sortable_column
        result = [(int(tuple_i[0]), tuple_i[1]) for tuple_i in tmp_lst]
        return result

    def _str_or_float_swap_comma_dot_convert(self
                                             ) -> Union[
        List[Tuple[str, str]], List[Tuple[float, str]]
    ]:
        """Or strings (nothing happens to them).
        Or decimal fractions(str) -> decimal fractions(float),
        their comma changes to a dot."""
        result = []
        for tuple_i in self._sortable_column:
            try:
                new_tuple = (float(tuple_i[0].replace(",", ".")), tuple_i[1])
            except ValueError:
                new_tuple = tuple_i
            result.append(new_tuple)
        return result
