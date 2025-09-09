from tkinter import ttk
from .widgets import Button
# Functionality frame with 8 buttons ====================================
class Functionality(ttk.LabelFrame):
    """
    Sidebar frame containing buttons for major application functions.

    This frame provides navigation and quick access to the core
    features of the Omakase system (tables, views, and exit). Each
    button triggers a callback with an associated identifier that
    allows the parent container to switch views accordingly.

    Attributes:
        server (dict): Database connection information used by child views.
        diners_btn (Button): Button to display the Diners table.
        prices_btn (Button): Button to display the Prices table.
        rooms_btn (Button): Button to display the Rooms table.
        allergies_btn (Button): Button to display the Allergies table.
        reservation_btn (Button): Button to display the Reservations table.
        details_btn (Button): Button to display the All Details view.
        revenue_btn (Button): Button to display the Revenues view.
        exit_btn (Button): Button to exit the program.
        func (Any): Placeholder for selected functionality (unused here).
        callback (Callable): Function to call when a feature button is pressed.
        on_exit (Callable): Function to call when the Exit button is pressed.

    Args:
        parent (tk.Widget): The parent container.
        server (dict): Connection details for the database.
        callback (Callable): Function called with an integer identifier
            when a feature button is pressed.
        on_exit (Callable): Function called when the Exit button is pressed.
    """

    def __init__(self, parent, server, callback, on_exit):
        super().__init__(parent, text="Functionality", style="Custom.TLabelframe")

        # Style
        style = ttk.Style()
        style.configure("Custom.TLabelframe.Label",
                        font=("Helvetica", 12, "bold"))

        # Grid layout (8 rows and 1 column)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, weight=1)
        self.rowconfigure(4, weight=1)
        self.rowconfigure(5, weight=1)
        self.rowconfigure(6, weight=1)
        self.rowconfigure(7, weight=1)
        self.columnconfigure(0, weight=1)

        self.server = server

        # Position 8 buttons
        self.diners_btn = Button(self, "Diners Table",
                                   self.view_diners, 0, 0)
        self.prices_btn = Button(self, "Prices Table",
                                     self.view_prices, 1, 0)
        self.rooms_btn = Button(self, "Rooms Table",
                                         self.view_rooms, 2, 0)
        self.allergies_btn = Button(self, "Allergies Table",
                                   self.view_allergies, 3, 0)
        self.reservation_btn = Button(self, "Reservations Table",
                                     self.view_res, 4, 0)
        self.details_btn = Button(self, "View Details",
                                   self.view_details, 5, 0)
        self.revenue_btn = Button(self, "View Revenues(Class)",
                                  self.view_revenue, 6, 0)
        self.exit_btn = Button(self, "Exit Program",
                                  self.exit_program, 7, 0)

        self.func = None
        self.callback = callback
        self.on_exit = on_exit

    def view_diners(self):
        """Trigger callback for the Diners table view."""
        self.callback(1)

    def view_prices(self):
        """Trigger callback for the Prices table view."""
        self.callback(2)

    def view_rooms(self):
        """Trigger callback for the Rooms table view."""
        self.callback(3)

    def view_allergies(self):
        """Trigger callback for the Allergies table view."""
        self.callback(4)

    def view_res(self):
        """Trigger callback for the Reservations table view."""
        self.callback(5)

    def view_details(self):
        """Trigger callback for the All Details view."""
        self.callback(6)

    def view_revenue(self):
        """Trigger callback for the Revenues view."""
        self.callback(7)

    def exit_program(self):
        """Trigger the exit callback to close the program."""
        self.on_exit(None)
