import sys
from pathlib import Path
import tkinter as tk
from tkinter import PhotoImage, Label
from .login import LoginFrame
from .dashboard import DashFrame
# Main Application Logic ====================================
class Application(tk.Tk):
    """
    The main Tkinter application for the Omakase system.

    This class serves as the entry point for the GUI layer. It manages
    the login screen, background image, and the dashboard display
    after successful login. It also handles the callback logic to exit the 
    application.

    Attributes:
        bg (tk.PhotoImage | None): Background image for the login screen.
        bg_label (tk.Label | None): Label widget used to display the background image.
        login (LoginFrame): The login frame displayed on startup.
        server (dict | None): Connection information for the Omakase database.
        dash (DashFrame | None): The dashboard frame, created after login.

    Args:
        title (str): The window title for the application.
        geo (str): The geometry string for window size (e.g., "1200x800").
    """
    def __init__(self, title:str, geo:str):
        super().__init__()
        # General setting
        self.title(title)
        self.geometry(geo)

        # Configure the grid of the root ( 1 row and 1 column)
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        # Create background image
        BASE_PATH = Path(__file__).resolve().parent / "images"
        self.bg = PhotoImage(file=str(BASE_PATH/"login-bg.gif"))
        self.bg_label = Label(self, image=self.bg)
        # Take up 100% width and height of parent
        self.bg_label.place(relx=0, rely=0, relwidth=1, relheight=1)

        # Use place() function to position log in frame
        self.login = LoginFrame(self, self.connectable_db, self.on_cancel)
        self.login.place(relx=0.12, rely=0.21, relwidth=0.4, relheight=0.6)

        self.server = None
        self.dash = None

    def connectable_db(self, res):
        """
        The callback triggered after attempting database connection.

        If connection succeeds, removes the login screen and background
        image, and loads the dashboard.

        Args:
            res (dict | None): Connection information if successful, 
                otherwise None.
        """
        self.server = res
        if self.server:
            self.login.destroy()       # Destroy log in frame
            self.bg_label.destroy()    # Destroy log in background
            self.show_dash()           # Show dashboard
            self.bg = None

    # Call back function to receive the exit command from login child or dashboard
    def on_cancel(self, res):
        """
        Handle exits from login or dashboard.

        If `res` is None, destroys the application window and
        exits the program.

        Args:
            res (Any): Result passed by child frame; if None,
                triggers application exit.
        """ 
        if res is None:
            self.destroy()
            sys.exit()

    def show_dash(self):
        """
        Display the dashboard after a successful login.

        Creates and displays a `DashFrame` that provides access
        to the main application dashboard.
        """
        if self.server:
            self.dash = DashFrame(self, self.server, self.on_cancel)
            self.dash.place(relx=0, rely=0, relwidth=1, relheight=1)