from mysql.connector import Error
from .connection import DBconnection
from .diners import Diners
# Allergies Table
class Allergies:
    """
    A class to interact with the `allergies` table.

    It manages interactions including retrieval, search, insertion and deletion.
    """
    @staticmethod
    def get_allergy_id(server, diner, allergy_type):
        """
        Get the allergy record ID for a diner/type pair.

        Args:
            server (dict): Connection kwargs for `mysql.connector.connect`.
            diner (str): Diner's name.
            allergy_type (str): Allergy category (e.g., 'Dairy', 'Shellfish').

        Returns:
            int: The allergy ID if found; `-1` if not found.
        """
        db = DBconnection(server)
        query = "SELECT getAllergyId(%s, %s)"
        cur = db.execute_query(query, [diner, allergy_type])
        res = cur.fetchone()[0]
        cur.close()
        db.disconnect()
        return res

    @staticmethod
    def get_all_allergies(server):
        """
        Retrieve all allergy records.

        Args:
            server (dict): Connection kwargs for `mysql.connector.connect`.

        Returns:
            list[tuple]: A list of tuples representing allergy rows.
        """
        db = DBconnection(server)
        cur = db.con.cursor()
        cur.callproc("getAllAllergies")
        cache = []
        for allergies in cur.stored_results():
            for allergy in allergies.fetchall():
                cache.append(allergy)
        cur.close()
        db.disconnect()
        return cache

    @staticmethod
    def get_searched_allergy(server, diner_name):
        """
        Filter allergy records by diner name (exact match).

        Args:
            server (dict): Connection kwargs for `mysql.connector.connect`.
            diner_name (str): Diner's name to match.

        Returns:
            list[list]: A list of `[id, diner, allergy_type, level]`
            records for the given diner. Empty list if none.
        """
        cache = []
        res = Allergies.get_all_allergies(server)
        for (i, diner, allergy_type, level) in res:
            if diner == diner_name:
                cache.append([i, diner, allergy_type, level])
        return cache

    @staticmethod
    def add_Allergy(server, diner_name, allergy_type, allergy_level):
        """
        Add a new allergy record for a diner.

        Args:
            server (dict): Connection kwargs for `mysql.connector.connect`.
            diner_name (str): Diner's name.
            allergy_type (str): Allergy category.
            allergy_level (str): Severity level.

        Returns:
            bool | int:
                * True  -> inserted successfully
                * -1    -> invalid allergy type or level
                * -2    -> diner not found
                * -3    -> allergy already exists for diner
                * False -> database error occurred
        """
        db = DBconnection(server)
        cur = db.con.cursor()
        # Though GUI has implemented the dropdown boxes, these types and
        # levels checks work as safety guard
        # If allergy type is other, the server will call diner to confirm 
        types = ['Dairy','Shellfish','Nuts','Eggs','Sesame','Wheat','Soy', 'Other']
        levels = ['Sensitive','Mild','Severe']
        try:
            diner_id = Diners.get_diner_id(server, diner_name)
            allergy_id = Allergies.get_allergy_id(server,diner_name, allergy_type)

            if allergy_type not in types or allergy_level not in levels:
                # allergy type or level not on the related lists
                mes = -1
            elif diner_id == -1:
                # Diner not on the diners table
                mes = -2
            elif allergy_id != -1:
                # Allergy already exists for that diner
                mes = -3
            else:
                cur.callproc("addAllergy",
                             [diner_name, allergy_type, allergy_level])
                db.commit()
                mes = True
        except Error:
                # Failed
                mes = False
        cur.close()
        db.disconnect()
        return mes

    @staticmethod
    def delete_allergy(server, diner_name, allergy_type):
        """
        Delete a diner's allergy record by type.

        Args:
            server (dict): Connection kwargs for `mysql.connector.connect`.
            diner_name (str): Diner's name.
            allergy_type (str): Allergy category to delete.

        Returns:
            bool | int:
                * True  -> deleted successfully
                * -1    -> allergy record not found
                * False -> database error occurred
        """
        db = DBconnection(server)
        cur = db.con.cursor()
        try:
            allergy_id = Allergies.get_allergy_id(server, diner_name,
                                                  allergy_type)
            if allergy_id != -1:
                cur.callproc("deleteAllergy",
                             [diner_name, allergy_type])
                db.commit()
                # Successfully deleted
                mes = True
            else:
                # Allergy record not on file
                mes = -1
        except Error:
            # Failed
            mes = False
        cur.close()
        db.disconnect()
        return mes
