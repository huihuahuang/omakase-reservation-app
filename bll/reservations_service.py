from datetime import datetime, time, timedelta
from dal import Reservations
from .rooms_service import room_existing

"""
Business Logic Layer (BLL) for Reservations.

This module provides higher-level wrappers around the DAL `Reservations` class.
It enforces business rules such as booking windows, minimum lead times,
and valid group sizes. These methods return clean, user-friendly values
for consumption by the GUI layer.
"""


def res_existing(server, dtime, room):
    """
    Check whether a reservation exists for a given datetime and room.

    Args:
        server (dict): Connection parameters for the database.
        dtime (datetime.datetime): Target reservation datetime.
        room (str): Room name.

    Returns:
        int: Reservation existence flag. Non-`-1` value if found;
        `-1` if not found.
    """
    return Reservations.get_res_existence(server, dtime, room)


def get_all_reservations(server):
    """
    Retrieve all reservations.

    Args:
        server (dict): Connection parameters for the database.

    Returns:
        list[list]: A list of `[date_time_str, room, diner, group_size]`
        for all reservations in the system.
    """
    return Reservations.get_all_reservations(server)


def get_searched_reservation(server, dtime, room):
    """
    Search for a reservation by datetime and room.

    Performs additional checks to ensure the room exists before
    querying reservations.

    Args:
        server (dict): Connection parameters for the database.
        dtime (datetime.datetime): Target reservation datetime.
        room (str): Room name.

    Returns:
        list[list] | int | None:
            - A list of `[date_time_str, room, diner, group_size]` if found.
            - 0 if the room exists but no reservation matches.
            - None if the room does not exist in the rooms table.
    """
    res1 = room_existing(server, room)
    if res1 == -1:
        return None  # room not found

    res2 = res_existing(server, dtime, room)
    if res2 == -1:
        return 0  # no record
    return Reservations.get_searched_reservation(server, dtime, room)


def add_reservation(server, dtime: datetime, room, diner, group):
    """
    Add a new reservation with business rules enforced.

    Rules:
        - Booking date must be at least 2 days in advance.
        - Each omakase experience lasts 1.5 hours.
        - Store hours are 17:00 - 23:00; reservations must start
          between 17:00 and 21:30.
        - Group size must be positive.
        - Overlapped reservations are not allowed.

    Args:
        server (dict): Connection parameters for the database.
        dtime (datetime.datetime): Desired reservation datetime.
        room (str): Room name.
        diner (str): Diner name.
        group (int): Number of people.

    Returns:
        bool | int:
            - True  -> reservation created successfully.
            - -1    -> invalid date/time (too early, too soon, or outside allowed hours).
            - -2    -> invalid group size (<= 0).
            - -3…-8 -> DAL-layer codes for diner/room not found or overlaps.
            - False -> database error occurred.
    """
    start = time(17, 0)
    end = time(21, 30)
    valid_date = datetime.now() + timedelta(days=2)

    if dtime < valid_date or dtime.time() < start or dtime.time() > end:
        mes = -1  # invalid time/date
    elif group <= 0:
        mes = -2  # invalid group size
    else:
        mes = Reservations.add_reservation(server, dtime, room, diner, group)

    return mes


def cancel_reservation(server, dtime, room):
    """
    Cancel an existing reservation.

    Args:
        server (dict): Connection parameters for the database.
        dtime (datetime.datetime): Target reservation datetime.
        room (str): Room name.

    Returns:
        bool | int:
            - True  -> reservation canceled successfully.
            - -1    -> reservation not found.
            - False -> database error occurred.
    """
    return Reservations.cancel_reservation(server, dtime, room)
