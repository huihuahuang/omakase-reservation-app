from dal import Prices

"""
Business Logic Layer (BLL) for Prices.

This module provides higher-level wrappers around the DAL `Prices` class.
It enforces business rules such as positive pricing and ensures the GUI
or other application layers get clean, user-friendly return values.
"""

def get_all_prices(server):
    """
    Retrieve all pricing classes.

    Args:
        server (dict): Connection parameters for the database.

    Returns:
        list[list]: A list of `[classId, name, formatted_price]` for all
        classes, where `formatted_price` is a string like "$100.00".
    """
    return Prices.get_all_prices(server)

def get_searched_class(server, name):
    """
    Search for a pricing class by exact name.

    Args:
        server (dict): Connection parameters for the database.
        name (str): The class name to search for.

    Returns:
        list[list] | None:
            - A list of `[id, name, costPerPerson]` if matches are found.
            - None if no class matches the given name.
    """
    res = Prices.get_searched_class(server, name)
    return None if len(res) == 0 else res

def add_class(server, name, price):
    """
    Add a new pricing class if it does not already exist.

    Business rules:
        - Price must be greater than zero.

    Args:
        server (dict): Connection parameters for the database.
        name (str): The new class name.
        price (float): The price for the class.

    Returns:
        bool | int:
            - True  -> class added successfully.
            - -1    -> class already exists.
            - -2    -> invalid price (<= 0).
            - False -> database error occurred.
    """
    if price <= 0:
        # Price must be over zero
        return -2
    return Prices.add_class(server, name, price)

def update_class(server, old_name, new_name, new_price):
    """
    Update an existing class's name and/or price.

    Args:
        server (dict): Connection parameters for the database.
        old_name (str): The current class name.
        new_name (str | None): The new name for the class (optional).
        new_price (float | None): The new price for the class (optional).

    Returns:
        bool | int:
            - True  -> update succeeded.
            - -1    -> old class not found.
            - -2    -> new class name already exists.
            - -3    -> other failure cases.
            - False -> database error occurred.
    """
    return Prices.update_class(server, old_name, new_name, new_price)