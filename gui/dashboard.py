from tkinter import ttk
from .side_bar import Functionality
from .logs import ActionLogFrame
from .data_display import DataFrame
# Dashboard layer ====================================
"""
This layer will appear if users successfully log in
There are three sections: 
Functionality to hold 8 buttons
Action logs to present results of add/update/delete/search actions
Data Frame to manipulate tables
"""

class DashFrame(ttk.Frame):
    """
    Main dashboard frame displayed after successful login.

    The dashboard is divided into three sections:
    - **Functionality**: Sidebar containing navigation buttons
      for core database operations and views.
    - **Action logs**: Panel that displays logs of add, update,
      delete, and search actions.
    - **Data frame**: Central area for interacting with tables
      and displaying query results.

    Attributes:
        on_exit (Callable): Callback function executed when the user exits.
        func_num (int | None): Identifier for the currently selected functionality.
        server (dict): Database connection information passed from the login frame.
        func (Functionality): Sidebar widget with navigation buttons.
        logs (ActionLogFrame): Log panel for displaying action results.
        data (DataFrame): Data display panel for table operations.

    Args:
        parent (tk.Widget): The parent container in which this frame is placed.
        server (dict): Database connection details.
        on_cancel (Callable): Callback to handle exit requests.
    """
    def __init__(self, parent, server, on_cancel):
        super().__init__(parent)

        # Grid layout (2 rows and 2 columns)
        self.rowconfigure(0, weight=4, minsize=600)
        self.rowconfigure(1, weight=1, minsize=150)
        self.columnconfigure(0, weight=1, minsize=200)
        self.columnconfigure(1, weight=4, minsize=800)

        self.on_exit = on_cancel
        self.func_num = None
        self.server = server

        # Position three sections
        self.func = Functionality(self, self.server, self.update_func_num,
                                  self.on_exit)
        self.func.grid(row=0, rowspan=2, column=0, padx=10, pady=5, sticky="nsew")

        self.logs = ActionLogFrame(self)
        self.logs.grid(row=1, column=1, padx=10, pady=5, sticky="nsew")

        self.data = DataFrame(self, self.server, self.func_num,self.logs)
        self.data.grid(row=0, column=1, padx=10, pady=5,sticky="nsew")

    def update_func_num(self, func):
        """
        Update the current functionality and refresh the data panel.

        Destroys the existing DataFrame and replaces it with a new one
        corresponding to the selected functionality.

        Args:
            func (int | None): Identifier for the selected functionality, passed
                from the Functionality sidebar (e.g., 1 for Diners,
                2 for Prices, etc. None to exit).
        """
        self.func_num = func
        if self.data:
            self.data.destroy()
        self.data = DataFrame(self, self.server, self.func_num, self.logs)
        self.data.grid(row=0, column=1, padx=10, pady=5, sticky="nsew")