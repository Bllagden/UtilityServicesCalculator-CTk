from typing import List, Union, Optional


class SQLBuilder:
    """The base class collects an SQL query for a transaction
    that has common methods."""

    @staticmethod
    def merge(query: Union[str, List[str]],
              tab_name: Union[str, List[Optional[str]]]
              ) -> Union[str, List[str]]:
        """Merges an SQL query to a table name:
            query - 'SELECT * FROM {}'
            name - 'house_2_2023_garb_1'
        A list of queries and a list of names are supported."""

        # single merge - str
        if isinstance(query, str) and isinstance(tab_name, str):
            return query.format(tab_name)

        # multiple merge - list[str]
        elif isinstance(query, list) and isinstance(tab_name, list):
            if len(query) != len(tab_name):
                raise ValueError("len(query) != len(tab_name)")

            result = []
            for i, name in enumerate(tab_name):
                if name is not None:
                    result.append(query[i].format(name))
                else:
                    result.append(query[i])
            return result

        else:
            raise TypeError("wrong types of query or tab_name")
