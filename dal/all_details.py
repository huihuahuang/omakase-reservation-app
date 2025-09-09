import datetime
from .connection import DBconnection
# AllDetails View
class AllDetails:
    """
    A class to interact with the `alldetails` view.

    The `alldetails` view aggregates information across reservations,
    diners, classes, rooms, staff, and billing. It is typically used
    for reporting or exporting complete reservation records.
    """
    @staticmethod
    def get_all_details(server):
        """
        Retrieve all records from the `alldetails` view.

        Args:
            server (dict): Connection kwargs for `mysql.connector.connect`.

        Returns:
            list[tuple]: A list of rows, where each row typically contains:
                (date_time, room, diner, phone, class_name,
                 group_size, staff, allergy_info, bill_total)
        """
        db = DBconnection(server)
        query = "SELECT * FROM all_details"
        cur = db.execute_query(query)
        res = cur.fetchall()
        cur.close()
        db.disconnect()
        return res

    @staticmethod
    def get_searched_detail(server, dtime: datetime, room_name):
        """
        Search for details of a reservation by datetime and room.

        Args:
            server (dict): Connection kwargs for `mysql.connector.connect`.
            dtime (datetime.datetime): Target datetime of the reservation.
            room_name (str): Room name to filter by.

        Returns:
            list[list]: A list of matching rows formatted as:
                [date_time_str, room, diner, phone, class_name,
                 group_size, staff, allergy_info, bill_total]
            Returns an empty list if no matches.

        Notes:
            - Datetime comparison is performed as a string in the format
              "YYYY-MM-DD HH:MM:SS".
            - This method fetches all rows from the view and filters
              client-side.
        """
        cache = []
        res = AllDetails.get_all_details(server)
        for (date_time, room, diner, phone, class_name, group, staff,
             allergy, bill) in res:
            # In sql, the date time is in YYYY-MM-DD HH:MM:SS format
            # Convert the string before comparison
            if (str(date_time) == dtime.strftime("%Y-%m-%d %H:%M:%S")
                    and room == room_name):
                cache.append([str(date_time), room, diner, phone, class_name,
                              group, staff, allergy, bill])
        return cache
