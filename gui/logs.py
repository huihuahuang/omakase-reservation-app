import tkinter as tk
from tkinter import ttk
from datetime import datetime
# Action Log layer to track add/update/delete actions ====================
class ActionLogFrame(ttk.LabelFrame):
    """
    A log panel for tracking user actions in the Omakase system.

    This frame provides a scrollable text area where log messages
    are displayed, such as successful or failed add, update,
    delete, or search actions. The most recent messages are
    inserted at the top of the log for easy visibility.

    Attributes:
        txt_box (tk.Text): The text widget used to display log messages.
        y_scroll (ttk.Scrollbar): Vertical scrollbar for navigating log content.

    Args:
        parent (tk.Widget): The parent container in which this frame is placed.
    """
    def __init__(self, parent):
        super().__init__(parent, text="Logs For "
                                      "Add/Update/Delete/Search Actions",
                         style="Custom.TLabelframe", padding=5)

        # Grid layer of output frame (2 rows and 2 columns)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=0)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=0)

        self.txt_box = tk.Text(self, wrap="word")
        self.txt_box.grid(row=0, column=0, sticky="nsew")
        self.txt_box.tag_config("welcome", foreground="blue")
        self.txt_box.tag_config("success", foreground="blue")
        self.txt_box.tag_config("error", foreground="red")
        # Welcome message is displayed once log in successfully
        self.txt_box.insert(
            "1.0", f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} "
               f"Welcome to Huang's Omakase Database.","welcome")

        # Scroll bars configuration
        self.y_scroll = ttk.Scrollbar(self, orient="vertical",
                                      command=self.txt_box.yview)
        self.y_scroll.grid(row=0, column=1, sticky="ns")
        self.txt_box.configure(yscrollcommand=self.y_scroll.set)

    # Add messages to the top (shown from latest)
    def add_message(self, mes, success=True):
        """
        Insert a new message into the log.

        Adds a timestamped log message at the top of the log display.
        Messages are styled according to their status (blue for success,
        red for errors).

        Args:
            mes (str): The log message to display.
            success (bool, optional): Whether the action was successful.
                Defaults to True. If False, the message is tagged as an error.
        """
        text = f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} {mes}\n"
        tag = "success" if success else "error"
        self.txt_box.insert("1.0", text, tag)