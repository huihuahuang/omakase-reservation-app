import tkinter as tk
from tkinter import ttk, messagebox

from .config import server_defaults
from .widgets import LoginEntry, Button
from ..bll import connected_db
# Login form layer ====================================
# This layer will disappear if users successfully log in
class LoginFrame(ttk.Frame):
    """
    Login form for connecting to the Omakase database.

    This frame provides a user interface for entering database connection 
    parameters (user, host, password, port). It is displayed on startup and 
    disappears when a successful login occurs. Defaults are prefilled from 
    environment variables via ``server_defaults()``.

    Attributes:
        title (ttk.Label): Title label for the login form.
        lb1 (LoginEntry): Entry field for the database user name.
        lb2 (LoginEntry): Entry field for the host name.
        lb3 (LoginEntry): Entry field for the password.
        lb4 (LoginEntry): Entry field for the port number.
        login_btn_frame (tk.Frame): Container frame for action buttons.
        connect_btn (Button): Connect button that triggers the DB connection.
        cancel_btn (Button): Exit button to cancel login and quit the app.
        on_success (Callable): Callback executed on successful login.
        on_cancel (Callable): Callback executed on cancel or failed login.

    Args:
        parent (tk.Widget): The parent container for this frame.
        on_success (Callable): Function called with connection info
            when login succeeds.
        on_cancel (Callable): Function called when login fails or user exits.
    """
    def __init__(self, parent, on_success, on_cancel):
        super().__init__(parent,style="Special.TFrame")

        # Style
        style = ttk.Style()
        style.configure("Special.TFrame", background="#ffffff")

        # Configure the grid of Login Frame (6 rows and 2 column)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, weight=1)
        self.rowconfigure(4, weight=1)
        self.rowconfigure(5, weight=1)

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        # Ask for configuration parameters - log in form
        self.title = ttk.Label(self, text="Log In To Connect OMA Database",
                               font=("Helvetica", 17, "bold"), background="#ffffff",
                               foreground="#eda186")
        
        # Default server value from config
        default_server = server_defaults()

        self.title.grid(row=0, column=0, columnspan=2, padx=5)
        self.lb1 = LoginEntry(self, "User Name: ",
                              1, 0, 1, 1, default_server["user"])
        self.lb2 = LoginEntry(self, "Host Name: ",
                              2, 0, 2, 1, default_server["host"])
        self.lb3 = LoginEntry(self, "Password: ", 3, 0, 3, 1,
                              default_server["password"])
        self.lb4 = LoginEntry(self, "Port Number: ",
                              4, 0, 4, 1, default_server["port"])

        # Command button frame
        self.login_btn_frame = tk.Frame(self, background="#ffffff")
        self.login_btn_frame.grid(row=5, column=1)
        self.login_btn_frame.rowconfigure(0, weight=1)
        self.login_btn_frame.columnconfigure(2, weight=1)
        self.connect_btn = Button(self.login_btn_frame, "Connect",
                                  self.connect_database, 0, 2)
        self.cancel_btn = Button(self.login_btn_frame, "Exit",
                                 self.exit_program, 0, 1)

        # Call back functions get passed from the parent
        self.on_success = on_success
        self.on_cancel = on_cancel

    def get_info(self):
        """
        Retrieve connection information from the login form.

        Returns:
            dict: Dictionary with connection parameters including
            ``user``, ``host``, ``password``, ``database``, and ``port``.
        """
        user = self.lb1.get_input().strip()
        host = self.lb2.get_input().strip()
        password = self.lb3.get_input().strip()
        port = self.lb4.get_input().strip()
        return {"user": user, "host": host, "password": password,
                "database": "oma",
                "port": port}

    def connect_database(self):
        """
        Attempt to connect to the Omakase database.

        Uses the current form values to establish a connection.
        If successful, shows a messagebox and calls ``on_success``.
        If failed, prompts the user to retry or cancel.
        """
        res = connected_db(self.get_info())
        if len(res) == 2:
            messagebox.showinfo("Connection Information:",
                                res[1])
            # Result should be dbconnection instance
            # Destroy the login form and bring up the dashboard
            self.on_success(res[0])
        else:
            answer = messagebox.askyesno("Failure Connection Information:",
                                      "Failed to connect with OMA. \nPlease make sure"
                                      " you enter valid information. \n" +
                                      "Do you want to try again?")
            # Result should be true or false
            if answer:
                self.reset_value()
            else:
                self.on_cancel(None)

    def reset_value(self): 
        """
        Reset all login fields to default server values.
        """
        default_server = server_defaults()
        # clear and re-insert
        self.lb1.delete_input()
        self.lb1.insert_input(default_server["user"])
        self.lb2.delete_input()
        self.lb2.insert_input(default_server["host"])
        self.lb3.delete_input()
        self.lb3.insert_input(default_server["password"])
        self.lb4.delete_input()
        self.lb4.insert_input(default_server["port"])

    def exit_program(self):
        """
        Exit the login process and trigger cancellation.

        Calls the ``on_cancel`` callback with ``None`` to signal
        that the application should quit.
        """
        self.on_cancel(None)