from ..dal import Allergies
from .diners_service import get_diner_id

"""
Business Logic Layer (BLL) for Allergies.

This module provides higher-level wrappers around the DAL `Allergies` class.
It enforces business rules such as checking whether a diner exists before
returning allergy records and provides user-friendly return values for
the GUI layer.
"""


def get_all_allergies(server):
    """
    Retrieve all allergy records.

    Args:
        server (dict): Connection parameters for the database.

    Returns:
        list[tuple]: A list of allergy rows. The exact tuple structure is
        defined by the DAL and typically includes:
        (id, diner, allergy_type, allergy_level).
    """
    return Allergies.get_all_allergies(server)


def get_searched_allergy(server, name):
    """
    Search for all allergy records of a specific diner.

    First checks whether the diner exists, then retrieves the associated
    allergy records.

    Args:
        server (dict): Connection parameters for the database.
        name (str): Diner's name.

    Returns:
        list[list] | int | None:
            - A list of `[id, diner, allergy_type, allergy_level]` if
              allergy records exist.
            - 0 if the diner exists but has no allergy records.
            - None if the diner does not exist in the diners table.
    """
    res1 = get_diner_id(server, name)
    if res1 == -1:
        return None  # diner not found

    res2 = Allergies.get_searched_allergy(server, name)
    return 0 if len(res2) == 0 else res2


def add_allergy(server, diner, allergy_type, allergy_level):
    """
    Add a new allergy record for a diner.

    Args:
        server (dict): Connection parameters for the database.
        diner (str): Diner's name.
        allergy_type (str): The type of allergy (e.g., 'Nuts', 'Dairy').
        allergy_level (str): The severity level (e.g., 'Mild', 'Severe').

    Returns:
        bool | int:
            - True  -> allergy added successfully.
            - -1    -> invalid allergy type or level.
            - -2    -> diner not found.
            - -3    -> allergy already exists for this diner.
            - False -> database error occurred.
    """
    return Allergies.add_Allergy(server, diner, allergy_type, allergy_level)


def delete_allergy(server, diner, allergy_type):
    """
    Delete an allergy record for a diner by type.

    Args:
        server (dict): Connection parameters for the database.
        diner (str): Diner's name.
        allergy_type (str): The allergy type to delete.

    Returns:
        bool | int:
            - True  -> allergy deleted successfully.
            - -1    -> allergy not found for the diner.
            - False -> database error occurred.
    """
    return Allergies.delete_allergy(server, diner, allergy_type)
