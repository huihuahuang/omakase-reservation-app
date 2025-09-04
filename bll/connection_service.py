from dal import DBconnection
# Test server if it is connectable
def connected_db(server):
    """
    Test whether the database server is reachable.

    Attempts to create a `DBconnection` with the provided server
    configuration. If the connection succeeds, a success message is returned.
    If the connection fails, the exception is caught and converted into a
    user-friendly error message in GUI layer.

    Args:
        server (dict): Connection parameters for `mysql.connector.connect`,
            typically including host, user, password, and database.

    Returns:
        tuple | str:
            - (dict, str): On success, returns the original `server`
              dictionary and a success message.
            - str: On failure, returns a formatted error message string
              that includes the reason for the failure.
    """
    try:
        DBconnection(server)
        mes = "Successfully connected with Omakase database!\n"
        return server, mes
    except Exception as e:
        # Error message will be displayed in the GUI layer
        return (f"Failed to connect!\n"
                f"Reason: {e}")