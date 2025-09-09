from .connection import DBconnection
# Advanced Feature - export all details view to csv
class CreateCSV:
    """
    A class to export reservation details into CSV files.

    This class wraps the stored procedure `exportDetails`, which returns
    the full `alldetails` view formatted for CSV export (including headers).
    It enables advanced features like generating CSV reports for external
    analysis or sharing.
    """
    @staticmethod
    def export_details(server):
        """
        Export all reservation details for CSV generation.

        Args:
            server (dict): Connection kwargs for `mysql.connector.connect`.

        Returns:
            list[tuple]: A list of rows with column headers included as
            the first row (depending on stored procedure definition).
        """
        db = DBconnection(server)
        cur = db.con.cursor()
        cache = []
        # Export csv with headers
        cur.callproc("export_details")
        for res in cur.stored_results():
            for r in res.fetchall():
                cache.append(r)
        cur.close()
        db.disconnect()
        return cache
