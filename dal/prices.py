from mysql.connector import Error
from .connection import DBconnection
# Prices Table
class Prices:
    """
    A class to interact with the `prices` table.

    It manages interactions including retrieval, search, insertion and updates.
    """
    @staticmethod
    def get_class_id(server, name):
        """
        Get the unique ID of a pricing class by name.

        Args:
            server (dict): Connection kwargs for `mysql.connector.connect`.
            name (str): Class name to search for.

        Returns:
            int: The class ID if found; `-1` if not found.
        """
        db = DBconnection(server)
        query = "SELECT getClassId(%s)"
        cur = db.execute_query(query, [name])
        res = cur.fetchone()[0]
        cur.close()
        db.disconnect()
        return res

    @staticmethod
    def get_all_prices(server):
        """
        Retrieve all pricing classes.

        Executes the stored procedure `getAllPrices`.

        Args:
            server (dict): Connection kwargs for `mysql.connector.connect`.

        Returns:
            list[list]: A list of `[Id, class, costPerPerson]`.
        """
        db = DBconnection(server)
        cur = db.con.cursor()
        cur.callproc("getAllPrices")
        cache = []
        for prices in cur.stored_results():
            for (classId, name, price) in prices.fetchall():
                cache.append([classId, name, f"${price:.2f}"])
        cur.close()
        db.disconnect()
        return cache

    @staticmethod
    def get_searched_class(server, class_name):
        """
        Search for a pricing class by exact name.

        Args:
            server (dict): Connection kwargs for `mysql.connector.connect`.
            class_name (str): Name of the class to search for.

        Returns:
            list[list]: A list of `[Id, class, costPerPerson]` for matched class.
            Returns an empty list if no matches.
        """
        cache = []
        res = Prices.get_all_prices(server)
        for (i, name, cost) in res:
            if name == class_name:
                cache.append([i, name, cost])
        return cache

    @staticmethod
    def add_class(server, name, price):
        """
        Add a new pricing class if it does not already exist.

        Args:
            server (dict): Connection kwargs for `mysql.connector.connect`.
            name (str): Class name to add.
            price (float): Class price.

        Returns:
            bool | int:
                * True  -> class added successfully
                * -1    -> class already exists
                * False -> database error occurred
        """
        db = DBconnection(server)
        cur = db.con.cursor()
        try:
            class_id = Prices.get_class_id(server, name)
            if class_id == -1:
                cur.callproc("addClass", [name, price])
                db.commit()
                # Successfully added
                mes = True
            else:
                # Already exists
                mes = -1
        except Error:
                # Failed
                mes = False
        cur.close()
        db.disconnect()
        return mes

    # Delete class does not happen frequently
    # So develop the function to update class and menu price
    @staticmethod
    def update_class(server, old_name, new_name=None, new_price=None):
        """
        Update an existing class's name and/or price.

        Args:
            server (dict): Connection kwargs for `mysql.connector.connect`.
            old_name (str): Current class name to update.
            new_name (str, optional): New class name. Defaults to None.
            new_price (float, optional): New price. Defaults to None.
        
        Returns:
            bool | int:
                * True  -> class updated successfully
                * -1    -> old class not found
                * -2    -> new class name already exists
                * -3    -> other failure cases
                * False -> database error occurred    
        """
        db = DBconnection(server)
        cur = db.con.cursor()
        try:
            old_name_id = Prices.get_class_id(server, old_name)
            new_name_id = Prices.get_class_id(server, new_name)
            if old_name_id != -1 and (new_name_id == -1 or new_name_id == old_name_id):
                cur.callproc("updateClass",
                             [old_name, new_name, new_price])
                db.commit()
                # Successfully updated
                mes = True
            elif old_name_id == -1:
                # old class is not on file
                mes = -1
            elif old_name_id != -1 and new_name_id != -1 and new_name_id != old_name_id:
                # new name already exists
                mes =  -2
            else:
                # other failure cases
                mes = -3
        except Error:
            # Failed
            mes = False
        cur.close()
        db.disconnect()
        return mes
