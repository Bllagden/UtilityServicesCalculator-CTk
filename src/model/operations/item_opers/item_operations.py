class ItemOperations:
    """The base class for working with items in a DB.
    Items: Houses, Tariffs, Years, Meters.
    The items are stored in the DB in the appropriate tables.
    Submitting non-DB items raises an exception."""

    def create(self) -> str:
        """Create an element.
        Returns a string indicating that the creation was successful or
        that the element already exists."""
        if not self._is_item_in_db():
            self._add_into_db()
            return "ITEM_CREATED"
        else:
            return "ITEM_ALREADY_EXISTS"

    def delete(self):
        """Deleting an element.
        Elements that are not in the DB cannot be submitted"""
        if self._is_item_in_db():
            self._del_from_db()
        else:
            raise ValueError("The item was not found in the DB.")

    def _is_item_in_db(self):
        """Checking if an element exists in the DB.
        Must be overridden in child classes."""
        pass

    def _add_into_db(self):
        """Adding an element to the DB.
        Must be overridden in child classes."""
        pass

    def _del_from_db(self):
        """Deleting an item from the DB.
        Must be overridden in child classes."""
        pass
