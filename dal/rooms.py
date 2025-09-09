from mysql.connector import Error
from .connection import DBconnection
from .prices import Prices
# Rooms Table
class Rooms:
    """
    A class to interact with the `rooms` table.

    It manages interactions including existence checks, search, retrieval, insertion, and updates.
    """
    # Since name works as primary key
    # The getter is designed to check existence
    @staticmethod
    def get_room_existence(server, name):
        """
        Check if a room exists by name.

        Args:
            server (dict): Connection kwargs for `mysql.connector.connect`.
            name (str): The room name to check.

        Returns:
            int: A room existence flag (ID or non-`-1` if exists; `-1` if not found).
        """
        db = DBconnection(server)
        query = "SELECT get_room_existence(%s)"
        cur = db.execute_query(query, [name])
        res = cur.fetchone()[0]
        cur.close()
        db.disconnect()
        return res

    @staticmethod
    def get_all_rooms(server):
        """
        Retrieve details for all rooms.

        Args:
            server (dict): Connection kwargs for `mysql.connector.connect`.

        Returns:
            list[tuple]: A list of tuples containing room details. The tuple
            shape is determined by the stored procedure (e.g.,
            `(room, staff, classID, tv)`).
        """
        db = DBconnection(server)
        cur = db.con.cursor()
        cur.callproc("get_all_rooms")
        cache = []
        for rooms in cur.stored_results():
            for r in rooms.fetchall():
                cache.append(r)
        cur.close()
        db.disconnect()
        return cache

    @staticmethod
    def get_searched_room(server, room_name):
        """
        Search for a specific room by exact name.

        Args:
            server (dict): Connection kwargs for `mysql.connector.connect`.
            room_name (str): The room name to match.

        Returns:
            list[list]: A list of `[room, staff, classID, tv]`
            for the matched room. Empty list if no match.
        """
        cache = []
        res = Rooms.get_all_rooms(server)
        for (room, staff, class_name, tv) in res:
            if room == room_name:
                cache.append([room, staff, class_name, tv])
        return cache

    @staticmethod
    def add_room(server, room_name, tv, class_name):
        """
        Add a new room if it does not already exist.

        Args:
            server (dict): Connection kwargs for `mysql.connector.connect`.
            room_name (str): The room name (unique).
            tv (str): TV availability flag ("Yes" => 1, "No" => 0).
            class_name (str): Associated pricing class.

        Returns:
            bool | int:
                * True  -> room added successfully
                * -2    -> class does not exist
                * -3    -> duplicate room name
                * -4    -> class missing AND room already exists
                * False -> DB error occurred
        """
        db = DBconnection(server)
        cur = db.con.cursor()
        try:
            class_id = Prices.get_class_id(server, class_name)
            room_id = Rooms.get_room_existence(server, room_name)

            # When class exists and room name does not exist, add new room
            if class_id != -1 and room_id == -1:
                cur.callproc("add_room", [room_name, tv, class_name])
                db.commit()
                # Successfully added
                mes = True
            elif class_id == -1 and room_id == -1:
                # class does not exist
                mes = -2
            elif class_id != -1 and room_id != -1:
                # duplicate room name
                mes = -3
            else:
                # class name does not exist and room name exists
                mes = -4
        except Error:
                # Failed
                mes = False
        cur.close()
        db.disconnect()
        return mes

    @staticmethod
    def update_room(server, room, new_room=None, tv=None, staff=None, new_class=None):
        """
        Update an existing room's attributes.

        Args:
            server (dict): Connection kwargs for `mysql.connector.connect`.
            room (str): Current room name (must exist).
            new_room (str, optional): New room name. Defaults to None.
            tv (str, optional): Updated TV flag. Defaults to None.
            staff (str, optional): Updated staff assignment. Defaults to None.
            new_class (str, optional): New associated pricing class. Defaults to None.

        Returns:
            bool | int:
                * True  -> room updated successfully
                * -1    -> old room not found
                * -2    -> new class name not found
                * -3    -> new room name is duplicate
                * False -> DB error occurred
        """
        db = DBconnection(server)
        cur = db.con.cursor()
        try:
            old_name_ex = Rooms.get_room_existence(server, room)

            if old_name_ex != -1:
                new_class_id = Prices.get_class_id(server, new_class)
                if new_class is not None and new_class_id == -1:
                    # class name does not exist
                    mes = -2
                else:
                    new_room_ex = Rooms.get_room_existence(server, new_room)
                    if (new_room is not None and new_room_ex != -1
                            and new_room != room):
                        # updated room name is duplicate
                        mes = -3
                    else:
                        cur.callproc(
                            "update_room",
                            [room, new_room, tv, staff, new_class])
                        db.commit()
                            # Successfully update
                        mes = True
            else:
                # old room Not on file
                mes = -1
        except Error:
            # Failed
            mes = False
        cur.close()
        db.disconnect()
        return mes
