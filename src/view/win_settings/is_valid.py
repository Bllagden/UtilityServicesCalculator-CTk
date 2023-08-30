class IsValid:
    """Class for checking arguments-keys sent to frames."""
    valid_frame_types = {"HOUSES", "TARIFFS"}
    valid_frame_parts = {"HEADER", "MAIN_BODY"}

    def __init__(self, frame_item: str):
        self._frame_item = frame_item

    def validate_frame_type(self):
        f = f"frame_type '{self._frame_item}' not in " \
            f"{IsValid.valid_frame_types}."
        if self._frame_item not in IsValid.valid_frame_types:
            raise ValueError(f)

    def validate_frame_part(self):
        f = f"frame_part '{self._frame_item}' not in " \
            f"{IsValid.valid_frame_parts}."
        if self._frame_item not in IsValid.valid_frame_parts:
            raise ValueError(f)
