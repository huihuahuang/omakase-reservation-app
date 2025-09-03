import mysql.connector

class DBconnection:
    """
    A simple class to represent a connection object from a MySQL server.
    
    This class provides a simple database connection object to manage activities
    such as open a database connection, execute queries and manage commits and 
    disconnect. It is designed to be used within the DAL layer to standardize 
    database interactions.

    Attributes:
        con (mysql.connector.connection_cext.CMySQLConnection): the active 
        connection object
    """
    def __init__(self, server):
        """
        Initialize a connection object based on the server information.

        The server information includes: host, user, password and database.
        Example:
        server = {
        "host": "localhost", 
        "user": "root", 
        "password": "pwd", 
        "database": "omakase"
        }
        """
        self.con = mysql.connector.connect(**server)

    def execute_query(self, query, params=None):
        """
        Execute a SQL query with optional parameters.

        Args:
            query (str): The SQL query string to execute.
            params (list | tuple | None): Optional parameters to safely
            substitute into the query. Defaults to None.

        Returns:
            cursor(mysql.connector.cursor.MySQLCursor): A cursor object with the
            results of the executed query.
        """
        cursor = self.con.cursor()
        cursor.execute(query, params or [])
        return cursor

    def disconnect(self):
        """
        Deactivate the connection object to MySQL.
        """
        # Cursor is already closed before closing connection
        # Since every method closes cursor at the end in this DAL.py design
        if self.con.is_connected():
            self.con.close()

    def commit(self):
        """
        Commit the current transactions to database. 

        Use this method after executing INSERT, UPDATE, or DELETE
        queries to make sure changes are saved.
        """
        self.con.commit()
