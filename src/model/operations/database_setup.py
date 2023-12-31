from typing import List, Tuple, Union

from model.database import DatabaseOperations
from model.sql_builders import SQLBuilderDBFirstConfigure


class DatabaseSetup:
    """The first connection to the DB while the program is running.
    Creates and configures a DB if it does not already exist.
    Prints the path and name of the DB."""

    def __init__(self):
        self._path = ""
        self._name = ""
        self._tabs: List[str] = []

    def execute(self):
        self._first_connect()
        self._check_db()

    def _first_connect(self):
        """
        If the program is launched from the src directory:
            path: 'root/src/model/database/'
            name: 'DEFAULT.db'

        If the program is launched from the root directory:
            path: 'root/'
            name: 'NON-DEFAULT.db'
        """
        self._path, self._name = DatabaseOperations.first_connect()
        print("==================================================")
        print(f"Connection to: {self._path + self._name}")

    def _check_db(self):
        """Checking if a new DB exists (it doesn't have a 'valid_db' table).
        If the DB is new, the initial setup is performed."""
        self._tabs = DatabaseOperations().get_db_tab_names()

        if "valid_db" not in self._tabs:
            print("New database")
            self._initial_setup()
        else:
            print("Existing database")
        print("==================================================")

    @staticmethod
    def _initial_setup():
        """The SQL transaction creates the base tables in the new DB."""
        queries: List[str]
        params: List[Union[None, Tuple]]
        queries, params = SQLBuilderDBFirstConfigure().get()
        DatabaseOperations.transaction(queries, params)
