from .connection import DBconnection
# Total Revenue By Class View
class Revenues:
    """
    A class to interact with `totalrevenuebyclass` view.

    The `totalrevenuebyclass` view provides aggregated financial
    information, grouped by menu class. It is typically used for
    reporting and analytics, such as displaying revenue by class
    type in dashboards or exports.
    """
    @staticmethod
    def get_all_revenues(server):
        """
        Retrieve all revenue records grouped by class.

        Args:
            server (dict): Connection kwargs for `mysql.connector.connect`.

        Returns:
            list[tuple]: A list of rows, where each row typically contains:
                (class_name, total_revenue)

            The exact tuple shape depends on how the database view
            `totalrevenuebyclass` is defined.
        """
        db = DBconnection(server)
        query = "SELECT * FROM totalRevenueByClass"
        cur = db.execute_query(query)
        res = cur.fetchall()
        cur.close()
        db.disconnect()
        return res