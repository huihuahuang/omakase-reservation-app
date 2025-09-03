from mysql.connector import Error
import datetime
from .connection import DBconnection
from .diners import Diners
from .rooms import Rooms
# Reservations Table
class Reservations:
    """
    A class to interact with the `reservations` table.

    It manages interactions including existence check, retrieval, search, 
    insertion and deletion.
    """
    @staticmethod
    def get_res_existence(server, dtime, room):
        """
        Check if a reservation exists for the given datetime and room.

        Args:
            server (dict): Connection kwargs for `mysql.connector.connect`.
            dtime (datetime.datetime | str): Reservation datetime. If a
                `datetime`, it will be passed to MySQL as a parameter.
            room (str): Room name.

        Returns:
            int: A non-`-1` value if a reservation exists; `-1` if not found.
        """
        db = DBconnection(server)
        query = "SELECT getReservationExistence(%s, %s)"
        cur = db.execute_query(query, [dtime, room])
        res = cur.fetchone()[0]
        cur.close()
        db.disconnect()
        return res

    @staticmethod
    def get_all_reservations(server):
        """
        Retrieve all reservations.

        Executes the stored procedure `getAllReservations`.

        Args:
            server (dict): Connection kwargs for `mysql.connector.connect`.

        Returns:
            list[list]: A list of `[date_time_str, room, diner, group_size]`.
                `date_time_str` is formatted like `"YYYY-MM-DD HH:MM:SS"`.
        """
        db = DBconnection(server)
        cur = db.con.cursor()
        cur.callproc("getAllReservations")
        cache = []
        for res in cur.stored_results():
            for (dt, room, diner, group)  in res.fetchall():
                cache.append([str(dt), room, diner, group])
        cur.close()
        db.disconnect()
        return cache

    @staticmethod
    def get_searched_reservation(server, dtime:datetime, room_name):
        """
        Search for a reservation by exact datetime and room.

        Args:
            server (dict): Connection kwargs for `mysql.connector.connect`.
            dtime (datetime.datetime): Target datetime.
            room_name (str): Room name to match.

        Returns:
            list[list]: A list of `[date_time_str, room, diner, group_size]`
                for matching reservations. Empty list if none.
        """
        cache = []
        res = Reservations.get_all_reservations(server)
        for (date_time, room, diner, total) in res:
            # In sql, the date time is in YYYY-MM-DD HH:MM:SS format
            # Convert the string before comparison
            if (date_time == dtime.strftime("%Y-%m-%d %H:%M:%S")
                    and room == room_name):
                cache.append([date_time, room, diner, total])
        return cache

    @staticmethod
    def add_reservation(server, dtime, room_name, diner_name, group):
        """
        Add a reservation if the diner and room exist and no overlaps occur.

        Validation steps:s
            1) Verify diner exists (`Diners.get_diner_id(...) != -1`).
            2) Verify room exists (`Rooms.get_room_existence(...) != -1`).
            3) Enforce 1.5-hour window to prevent overlaps by:
               - room (primary key constraint on `(dateAndTime, room)`)
               - diner (candidate key-like constraint on `(dateAndTime, diner)`)

        Overlap logic:
            x_start < y_end  AND  y_start < x_end
            Here, end = start + 1.5 hours.

        Args:
            server (dict): Connection kwargs for `mysql.connector.connect`.
            dtime (datetime.datetime | str): Reservation datetime.
            room_name (str): Room to reserve.
            diner_name (str): Diner making the reservation.
            group (int): Group size.

        Returns:
            bool | int:
                * True  -> reservation created (committed)
                * -3    -> diner not found
                * -4    -> room not found
                * -5    -> both diner and room not found
                * -6    -> both room and diner overlapping
                * -7    -> room overlapping
                * -8    -> diner overlapping
                * False -> DB error occurred
        """
        db = DBconnection(server)

        diner_id = Diners.get_diner_id(server, diner_name)
        room_exists = Rooms.get_room_existence(server, room_name)
        if diner_id == -1 and room_exists == 1:
            # diner not on the list
            mes = -3
        elif diner_id != -1 and room_exists == -1:
            # room not on the list
            mes = -4
        elif diner_id == -1 and room_exists == -1:
            # both diner and room not on file
            mes = -5
        else:
            try:
                # Duration of each omakase experience is 1.5 hours
                # Make sure there is no overlapped reservation

                # Logic: x_start < y_end and y_start < a_end
                # Check primary key (dateAndTime, room)
                q1 = (
                    "SELECT * FROM alldetails "
                    "WHERE room = %s "
                    "AND (%s < ADDTIME(dateAndTime, SEC_TO_TIME(1.5 * 3600)) "
                    "AND dateAndTime < ADDTIME(%s, SEC_TO_TIME(1.5 * 3600)))"
                )
                cur1 = db.execute_query(q1, [room_name, dtime, dtime])
                res1 = cur1.fetchall()
                cur1.close()

                # Check candidate key (dateAndTime, dinerId)
                q2 = (
                    "SELECT * FROM alldetails "
                    "WHERE diner = %s "
                    "AND (%s < ADDTIME(dateAndTime, SEC_TO_TIME(1.5 * 3600)) "
                    "AND dateAndTime < ADDTIME(%s, SEC_TO_TIME(1.5 * 3600)))"
                )
                cur2 = db.execute_query(q2, [diner_name, dtime, dtime])
                res2 = cur2.fetchall()
                cur2.close()
                if res1 and res2:
                    # Both room and diner are double-booked
                    mes = -6
                elif res1:
                    # Room is double-booked
                    mes = -7
                elif res2:
                    # Diner is double-booked
                    mes = -8
                else:
                    # When diner exists, room exists and record not found
                    cur = db.con.cursor()
                    cur.callproc("addReservation",
                                         [dtime, room_name, diner_name, group])
                    db.commit()
                    cur.close()
                    # Successfully added
                    mes = True
            except Error:
                mes = False
        db.disconnect()
        return mes

    @staticmethod
    def cancel_reservation(server, dtime, room_name):
        """
        Cancel a reservation by datetime and room.

        Args:
            server (dict): Connection kwargs for `mysql.connector.connect`.
            dtime (datetime.datetime | str): Reservation datetime.
            room_name (str): Room name.

        Returns:
            bool | int:
                * True  -> reservation canceled (committed)
                * -1    -> reservation not found
                * False -> DB error occurred
        """
        db = DBconnection(server)
        cur = db.con.cursor()
        try:
            res_id = Reservations.get_res_existence(server, dtime, room_name)
            if res_id != -1:
                cur.callproc("deleteReservation", [dtime, room_name])
                db.commit()
                # Successfully canceled
                mes = True
            else:
                # Not on file
                mes = -1
        except Error:
            # Failed
            mes = False
        cur.close()
        db.disconnect()
        return mes