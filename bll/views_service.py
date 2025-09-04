from dal import AllDetails
from dal import Revenues
from .rooms_service import room_existing
from .reservations_service import res_existing

"""
Business Logic Layer (BLL) for Reports.

This module provides higher-level wrappers around DAL classes that return
aggregated or reporting-oriented data, such as full reservation details
and total revenue by class. It also performs business checks to ensure
room and reservation validity before returning detailed results.
"""


# ============= All Details View ===============
def get_all_details(server):
    """
    Retrieve all records from the `alldetails` view.

    Args:
        server (dict): Connection parameters for the database.

    Returns:
        list[tuple]: A list of rows from the `alldetails` view, typically
        including (date_time, room, diner, phone, class_name, group,
        staff, allergy_info, bill).
    """
    return AllDetails.get_all_details(server)


def get_searched_details(server, dtime, room):
    """
    Search for reservation details by datetime and room.

    Checks:
        - Room existence in the rooms table.
        - Reservation existence in the reservations table.

    Args:
        server (dict): Connection parameters for the database.
        dtime (datetime.datetime): Reservation datetime to search for.
        room (str): Room name to match.

    Returns:
        list[list] | int | None:
            - A list of `[date_time, room, diner, phone, class_name,
              group, staff, allergy_info, bill]` if found.
            - 0 if the room exists but no reservation matches.
            - None if the room does not exist in the rooms table.
    """
    res1 = room_existing(server, room)
    if res1 == -1:
        return None  # room not found

    res2 = res_existing(server, dtime, room)
    if res2 == -1:
        return 0  # no reservation found
    return AllDetails.get_searched_detail(server, dtime, room)


# ============= Total Revenue By Class View ===============
def get_all_revenues(server):
    """
    Retrieve aggregated revenue data by class.

    Args:
        server (dict): Connection parameters for the database.

    Returns:
        list[tuple]: A list of rows from the `totalrevenuebyclass` view,
        typically containing (class_name, total_revenue).
    """
    return Revenues.get_all_revenues(server)
