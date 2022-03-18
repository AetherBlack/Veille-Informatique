
from functools import wraps

import re


def database_invoke(fn):
    @wraps(fn)
    def wrapper(self, *args, **kwargs):
        # Get connection and cursor
        self.ConnectDatabase()
        # Execute function
        var = fn(self, *args, **kwargs)
        # Close the connection
        self.CloseDatabase()
        return var
    return wrapper

class Filter:

    @staticmethod
    def checkTitle(filter: dict, title: str) -> bool:
        """
        Check if filter match title
        @param: `dict`: `filter`: Filter to compare the `title` with.
        @param: `str`: `title`: Title of the news.
        """
        return Filter.checkStringWithFilter(filter, title, "title")

    @staticmethod
    def checkDescription(filter: dict, description: str) -> bool:
        """
        Check if filter match description
        @param: `dict`: `filter`: Filter to compare the `description` with.
        @param: `str`: `description`: Description of the news.
        """
        return Filter.checkStringWithFilter(filter, description, "description")

    @staticmethod
    def checkLink(filter: dict, link: str) -> bool:
        """
        Check if filter match link
        @param: `dict`: `filter`: Filter to compare the `link` with.
        @param: `str`: `link`: Link of the news.
        """
        return Filter.checkStringWithFilter(filter, link, "link")

    @staticmethod
    def checkStringWithFilter(filter: dict, string: str, field: str) -> bool:
        """
        Check if filter match string
        @param: `dict`: `filter`: Filter to compare the `string` with.
        @param: `str`: `string`: String in the news.
        @param: `str`: `field`: Field in the news like [Title, Description, Link]
        """
        # Check and get filter for the field
        if field in filter.keys():
            filter = filter[field]
        else: return True

        # List of boolean
        list_bool = list()
        
        # Check each field filter
        for keys in filter.keys():
            if keys == "in":
                list_bool.append(Filter.checkFilterInMethod(filter["in"], string))
            elif keys == "not in":
                list_bool.append(Filter.checkFilterNotInMethod(filter["not in"], string))
            elif keys == "match":
                list_bool.append(Filter.checkFilterMatchMethod(filter["match"], string))
            else:
                print(f"[!] '{keys}' is not implemented !")
        
        return all(list_bool)

    @staticmethod
    def checkFilterInMethod(list_string: list, field: str) -> bool:
        """
        Check if each string in List[string] are in provided field string.
        @param: `list`: `list_string`: List of string to check if they are in the `field`
        @param: `str`: `field`: Content of the Title, Description or Link
        """
        return all([True if string in field else False for string in list_string])

    @staticmethod
    def checkFilterNotInMethod(list_string: list, field: str) -> bool:
        """
        Check if each string in List[string] are not in provided field string.
        @param: `list`: `list_string`: List of string to check if they are not in the `field`
        @param: `str`: `field`: Content of the Title, Description or Link
        """
        return all([True if string not in field else False for string in list_string])

    @staticmethod
    def checkFilterMatchMethod(list_string: list, field: str) -> bool:
        """
        Check if each string in List[string] match (regex) the provided field string.
        @param: `list`: `list_string`: List of string to check if they match the `field`
        @param: `str`: `field`: Content of the Title, Description or Link
        """
        return all([True if re.match(string, field) is not None else False for string in list_string])
