from ..dal import Rooms

"""
Business Logic Layer (BLL) for Rooms.

This module provides higher-level wrappers around the DAL `Rooms` class.
It is responsible for exposing clean methods for interacting with the
rooms table, ensuring user-friendly return values for the GUI and
other application layers.
"""


def room_existing(server, name):
    """
    Check if a room exists by name.

    Args:
        server (dict): Connection parameters for the database.
        name (str): The room name to check.

    Returns:
        int: A non-`-1` value if the room exists; `-1` if not found.
    """
    return Rooms.get_room_existence(server, name)


def get_all_rooms(server):
    """
    Retrieve all rooms.

    Args:
        server (dict): Connection parameters for the database.

    Returns:
        list[tuple]: A list of tuples containing room details, typically
        in the form `(room, staff, class_name, tv)`.
    """
    return Rooms.get_all_rooms(server)


def get_searched_room(server, name):
    """
    Search for a room by exact name.

    Args:
        server (dict): Connection parameters for the database.
        name (str): The room name to search for.

    Returns:
        list[list] | None:
            - A list of `[room, staff, class_name, tv]` if found.
            - None if no room matches the given name.
    """
    res = Rooms.get_searched_room(server, name)
    return None if len(res) == 0 else res


def add_room(server, room, tv, class_name):
    """
    Add a new room.

    Args:
        server (dict): Connection parameters for the database.
        room (str): Room name (unique).
        tv (str | int): TV availability flag (DB-specific format).
        class_name (str): Associated pricing class.

    Returns:
        bool | int:
            - True  -> room added successfully.
            - -2    -> class does not exist.
            - -3    -> duplicate room name.
            - -4    -> class missing and room already exists.
            - False -> database error occurred.
    """
    return Rooms.add_room(server, room, tv, class_name)


def update_room(server, room, new_room, tv, staff, new_class):
    """
    Update details of an existing room.

    Args:
        server (dict): Connection parameters for the database.
        room (str): Current room name (must exist).
        new_room (str | None): New room name (optional).
        tv (str | int | None): Updated TV availability (optional).
        staff (str | None): Updated staff assignment (optional).
        new_class (str | None): Updated pricing class (optional).

    Returns:
        bool | int:
            - True  -> room updated successfully.
            - -1    -> old room not found.
            - -2    -> new class not found.
            - -3    -> new room name is duplicate.
            - False -> database error occurred.
    """
    return Rooms.update_room(server, room, new_room, tv, staff, new_class)
