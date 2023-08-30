from typing import List, Tuple

from src.model.database import DatabaseOperations
from src.model.sql import SQL


class GetSetLanguage:
    """The class for getting the current interface language from the DB and
    updating it in the DB.
    It is possible to save the last used language in the DB."""

    @staticmethod
    def get() -> str:
        """return options: 'RU' | 'ENG' """
        query: str = SQL["SELECT_language"]
        language: List[Tuple[str]] = DatabaseOperations.single_query(query)
        return language[0][0]

    @staticmethod
    def set(language: str):
        """input options: 'RU' | 'ENG' """
        query: str = SQL["UPDATE_language"]
        params: Tuple[str] = (language,)
        DatabaseOperations.single_query(query, params)
