from mysql.connector import Error
from .connection import DBconnection
# Diners Table
class Diners:
    """
    A class to interact with the `diners` table. 

    It manages interactions including retrieval, search, insertion and deletion.
    """
    @staticmethod
    def get_diner_id(server, diner):
        """
        Get the unique ID for a diner by name. 

        Args:
            server (dict): Connection kwargs for `mysql.connector.connect`.
            diner (str): The diner's name.

        Returns:
            int: The diner ID if found; `-1` if the diner does not exist.
        """
        db = DBconnection(server)
        query = "SELECT getDinerId(%s)"
        cur = db.execute_query(query, [diner])
        res = cur.fetchone()[0]
        cur.close()
        db.disconnect()
        return res

    @staticmethod
    def get_all_diners(server):
        """
        Retrieve all diners by executing the stored procedure `getAllDiners`.

        Args:
            server (dict): Connection kwargs for `mysql.connector.connect`.

        Returns:
            list[tuple]: A list of rows returned by `getAllDiners`. Each tuple
            containes `(id, diner, phone)`).
        """
        db = DBconnection(server)
        cur = db.con.cursor()
        cur.callproc("getAllDiners")
        cache = []
        for diners in cur.stored_results():
            for d in diners.fetchall():
                cache.append(d)
        cur.close()
        db.disconnect()
        return cache

    @staticmethod
    def get_searched_diner(server, diner):
        """
        Filter diners by exact name.

        Args:
            server (dict): Connection kwargs for `mysql.connector.connect`.
            diner (str): Exact name to match.

        Returns:
            list[list]: A list of `[id, diner, phone]` for rows whose `name`
            equals `diner`. Returns an empty list if no matches.
        """
        cache = []
        res = Diners.get_all_diners(server)
        for (i, name, phone) in res:
            if name == diner:
                cache.append([i, name, phone])
        return cache

    @staticmethod
    def add_diner(server, name, phone):
        """
        Add a new diner if it does not already exist.

        Args:
            server (dict): Connection kwargs for `mysql.connector.connect`.
            name (str): Diner's name (must be unique per DB rules).
            phone (str): Diner's phone number.

        Returns:
            bool | int:
                * True  -> diner added successfully (committed)
                * -1    -> diner already exists (no changes made)
                * False -> unexpected DB error (exception caught)
        """
        db = DBconnection(server)
        cur = db.con.cursor()
        try:
            diner_id = Diners.get_diner_id(server, name)
            if diner_id == -1:
                cur.callproc("addDiner", [name, phone])
                db.commit()
                # Successfully added
                mes = True
            else:
                # Diner already exists
                mes = -1
        except Error:
                # Failed
                mes = False
        cur.close()
        db.disconnect()
        return mes

    @staticmethod
    def delete_diner(server, name):
        """
        Delete an existing diner by name.

        Args:
            server (dict): Connection kwargs for `mysql.connector.connect`.
            name (str): Exact diner name to delete.

        Returns:
            bool | int:
                * True  -> diner deleted successfully (committed)
                * -1    -> diner not found (no changes made)
                * False -> unexpected DB error (exception caught)
        """
        db = DBconnection(server)
        cur = db.con.cursor()
        try:
            diner_id = Diners.get_diner_id(server, name)
            if diner_id != -1:
                cur.callproc("deleteDiner", [name])
                db.commit()
                # Successfully deleted
                mes = True
            else:
                # Diner is not on diners file
                mes = -1
        except Error:
            # Failed
            mes = False
        cur.close()
        db.disconnect()
        return mes