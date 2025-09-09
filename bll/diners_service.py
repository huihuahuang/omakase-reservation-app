from ..dal import Diners
"""
Business Logic Layer (BLL) for Diners.

This module provides higher-level wrappers around the DAL `Diners` class.
It is responsible for applying business rules, handling empty results,
and exposing clean methods to be consumed by the GUI layers.
"""
def get_diner_id(server, name):
    """
    Retrieve a diner's ID by name.

    Args:
        server (dict): Connection parameters for the database.
        name (str): The diner's name.

    Returns:
        int: The diner ID if found; -1 if not found.
    """
    return Diners.get_diner_id(server, name)

def get_all_diners(server):
    """
    Retrieve all diners.

    Args:
        server (dict): Connection parameters for the database.

    Returns:
        list[tuple]: A list of tuples representing all diners,
        typically in the form `(id, diner, phone)`.
    """
    return Diners.get_all_diners(server)

def get_searched_diner(server, name):
    """
    Search for a diner by exact name.

    Args:
        server (dict): Connection parameters for the database.
        name (str): The diner's name to search for.

    Returns:
        list[list] | None:
            - A list of `[id, diner, phone]` if matches are found.
            - None if no diner matches the given name.
    """
    res = Diners.get_searched_diner(server, name)
    return None if len(res) == 0 else res

def add_diner(server, name, phone):
    """
    Add a new diner.

    Args:
        server (dict): Connection parameters for the database.
        name (str): Diner's name.
        phone (str): Diner's phone number.

    Returns:
        bool | int:
            - True  -> diner added successfully.
            - -1    -> diner already exists.
            - False -> database error occurred.
    """
    return Diners.add_diner(server, name, phone)

def delete_diner(server, name):
    """
    Delete a diner by name.

    Args:
        server (dict): Connection parameters for the database.
        name (str): Diner's name.

    Returns:
        bool | int:
            - True  -> diner deleted successfully.
            - -1    -> diner not found.
            - False -> database error occurred.
    """
    return Diners.delete_diner(server, name)