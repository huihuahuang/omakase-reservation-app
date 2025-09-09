import tkinter as tk
import os
from datetime import datetime
from tkinter import ttk, messagebox
from ..widgets import Button
from ..logs import ActionLogFrame
from ...bll import get_all_details, get_searched_details, export_details
# For All Details View (advanced feature csv included) --------------
class AllDetailsFrame(ttk.LabelFrame):
    """
    The panel for listing, searching, and exporting the 'All Details' view.

    Renders a `ttk.Treeview` containing the combined reservation details
    (datetime, room, diner, phone, class, group size, staff, allergy, bill).
    Provides:
      - Full list loader  
      - Search by begin datetime + room name  
      - CSV export of the full details data

    All successes and errors are written to the shared `ActionLogFrame`.

    Attributes:
        server (dict): Database connection configuration from the dashboard.
        log (ActionLogFrame): Log panel to display success/error messages.
        details (ttk.Treeview): Grid of the 'All Details' view fields.
        x_scroll (ttk.Scrollbar | None): Horizontal scrollbar for the tree view.
        y_scroll (ttk.Scrollbar | None): Vertical scrollbar for the tree view.
        button_frame (ttk.Frame): Container for the full-list button.
        full_btn (Button): Reloads the full details list.
        search (ttk.LabelFrame): Container for the search inputs.
        dtime_entry (ttk.Entry): Search input for datetime ("YYYY-MM-DD HH:MM").
        search_room_entry (ttk.Entry): Search input for room name.
        csv_frame (ttk.LabelFrame): Container for CSV export controls.
        path_entry (ttk.Entry): Input for export file path.
        csv_btn (ttk.Button): Triggers CSV export.

    Args:
        parent (tk.Widget): Parent container.
        server (dict): Database connection details used by BLL calls.
        logs (ActionLogFrame): Shared action log instance.
    """
    def __init__(self, parent, server, logs:ActionLogFrame):
        super().__init__(parent, text="Full Details List",
                         style="Custom.TLabelframe")
        self.server = server
        self.log = logs

        # Grid layout (4 rows and 4 columns)
        self.rowconfigure(0, weight=2, minsize=150)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.columnconfigure(3, weight=1)


        # Display all details tree view ----------------------
        # First row
        self.details = ttk.Treeview(self, padding=(0, 0, 10, 10))
        self.details.grid(row=0, column=0, columnspan=4, padx=10, pady=10,
                         sticky="nsew")
        self.details["columns"] = ("Date and Time", "Room Name", "Diner Name",
                                  "Phone", "Class Name", "Total Diners", "Staff",
                                  "Allergy", "Bill")

        self.details.column("#0", width=0, stretch=False)
        self.details.column("Date and Time", anchor="center", width=150)
        self.details.column("Room Name", anchor="center", width=100)
        self.details.column("Diner Name", anchor="center", width=150)
        self.details.column("Phone", anchor="center", width=100)
        self.details.column("Class Name", anchor="center", width=100)
        self.details.column("Total Diners", anchor="center", width=100)
        self.details.column("Staff", anchor="center", width=100)
        self.details.column("Allergy", anchor="center", width=100)
        self.details.column("Bill", anchor="center", width=100)

        self.details.heading("#0", text="", anchor="center")
        self.details.heading("Date and Time", text="Date and Time", anchor="center")
        self.details.heading("Room Name", text="Room Name",anchor="center")
        self.details.heading("Diner Name", text="Diner Name", anchor="center")
        self.details.heading("Phone", text="Phone", anchor="center")
        self.details.heading("Class Name", text="Class Name", anchor="center")
        self.details.heading("Total Diners", text="Total Diners", anchor="center")
        self.details.heading("Staff", text="Staff", anchor="center")
        self.details.heading("Allergy", text="Allergy", anchor="center")
        self.details.heading("Bill", text="Bill", anchor="center")

        self.x_scroll = None
        self.y_scroll = None
        self.create_scroll_bars()
        self.load_full_data()

        # Display action buttons  ----------------------
        # Second row
        self.button_frame = ttk.Frame(self)
        self.button_frame.grid(row=1, column=1, columnspan=2, sticky="ew")
        self.button_frame.rowconfigure(0, weight=1)
        self.button_frame.columnconfigure(0, weight=1)
        self.button_frame.columnconfigure(1, weight=1)
        self.button_frame.columnconfigure(2, weight=1)
        self.full_btn = Button(self.button_frame, "Full List",
                               self.load_full_data, 0, 1)


        # Third row - search form
        self.search = ttk.LabelFrame(self, text="Search Details By "
                                                "DateAndTime (Begin date and time)"
                                                " and Room Name",
                                     padding=3)
        self.search.grid(row=2, column=0, columnspan=4, padx=5, sticky="ew")
        self.search.rowconfigure(0, weight=1)
        self.search.columnconfigure(0, weight=1)
        self.search.columnconfigure(1, weight=1)
        self.search.columnconfigure(2, weight=1)
        self.search.columnconfigure(3, weight=1)
        self.search.columnconfigure(4, weight=1)

        self.dtime = ttk.Label(self.search, text="Date and Time:",
                               font=("Helvetica", 11))
        self.dtime.grid(row=0, column=0, sticky="e", padx=5)
        self.dtime_entry = ttk.Entry(self.search)
        self.dtime_entry.grid(row=0, column=1, sticky="w", padx=5, ipadx=3,
                              ipady=3)

        self.search_room = ttk.Label(self.search, text="Room Name:",
                                     font=("Helvetica", 11))
        self.search_room.grid(row=0, column=2, sticky="e", padx=5)
        self.search_room_entry = ttk.Entry(self.search)
        self.search_room_entry.grid(row=0, column=3, sticky="w", padx=5,
                                    ipadx=3,
                                    ipady=3)

        self.search_btn = ttk.Button(self.search, text="Search Details",
                                     command=self.load_searched_data,
                                     style="Special.TButton")
        self.search_btn.grid(row=0, column=4, sticky="ew", padx=15)
        self.notice1 = ttk.Label(self.search,
                                 text="Date and time input must be in "
                                      "'YYYY-MM-DD HH:MM' format."
                                      "For example: 2025-07-01 18:00.",
                                 font=("Helvetica", 8))
        self.notice1.grid(row=2, column=0, columnspan=5, pady=2)

        # Fourth row - export csv
        self.csv_frame = ttk.LabelFrame(self, text="Export to CSV", padding=3)
        self.csv_frame.grid(row=3, column=0, columnspan=4, padx=5, sticky="ew")
        self.csv_frame.rowconfigure(0, weight=1)
        self.csv_frame.columnconfigure(0, weight=1)
        self.csv_frame.columnconfigure(1, weight=1)
        self.csv_frame.columnconfigure(2, weight=1)
        self.csv_frame.columnconfigure(3, weight=1)
        self.csv_frame.columnconfigure(4, weight=1)

        self.add_path = ttk.Label(self.csv_frame,text="Path Name:",
                                  font=("Helvetica", 11))
        self.add_path.grid(row=0, column=0, sticky="e", padx=5)
        self.path_entry = ttk.Entry(self.csv_frame)
        self.path_entry.grid(row=0, column=1, columnspan=3, sticky="ew", padx=5,
                             ipadx=3, ipady=3)

        self.csv_btn = ttk.Button(self.csv_frame, text="Export CSV",
                                  command=self.export_csv, style="Special.TButton")
        self.csv_btn.grid(row=0, column=4, sticky="ew", padx=15)
        self.notice2 = ttk.Label(self.csv_frame,
                                text="Please make sure the input path is valid "
                                     "in your system. ",
                                font=("Helvetica", 8))
        self.notice2.grid(row=1, column=1, columnspan=3, pady=2)
        self.notice3 = ttk.Label(self.csv_frame,
                                 text="You can leave it blank if you want to "
                                      "export it with default name "
                                      "(exported_details.csv) in current folder. ",
                                 font=("Helvetica", 8))
        self.notice3.grid(row=2, column=1, columnspan=3, pady=2)

    def create_scroll_bars(self):
        """
        Attach horizontal/vertical scrollbars to the details tree view.

        Configures the tree view to use the created scrollbars.

        Side Effects:
            Modifies `self.details` to connect x/y scroll commands.
            Creates and assigns `self.x_scroll` and `self.y_scroll`.
        """
        # Scroll bars configuration
        self.x_scroll = ttk.Scrollbar(self.details, orient="horizontal",
                                      command=self.details.xview)
        self.y_scroll = ttk.Scrollbar(self.details, orient="vertical",
                                      command=self.details.yview)
        self.x_scroll.pack(side="bottom", fill="x")
        self.y_scroll.pack(side="right", fill="y")
        self.details.configure(xscrollcommand=self.x_scroll.set,
                       yscrollcommand=self.y_scroll.set)

    def load_full_data(self):
        """
        Load and display the full 'All Details' list.

        Fetches all combined details via the BLL and populates the tree view.
        Uses alternating row tags ("odd"/"even") for readability and sets the
        label frame title to "Full Detail List".
        """
        self.details.delete(*self.details.get_children())
        self.configure(text="Full Detail List")
        records = get_all_details(self.server)
        self.details.tag_configure("odd", background="white")
        self.details.tag_configure("even", background="#E6E6E6")
        for i, r in enumerate(records):
            if i % 2 != 0:
                self.details.insert(parent="", index="end", values=r, tags=("odd",))
            else:
                self.details.insert(parent="", index="end", values=r, tags=("even",))

    def clear_search_form(self):
        """Clear the search inputs (datetime and room)."""
        self.dtime_entry.delete(0, tk.END)
        self.search_room_entry.delete(0, tk.END)

    def load_searched_data(self):
        """
        Search the 'All Details' view by begin datetime and room name.

        Parses the datetime input, validates room length, and queries the BLL.
        Handles three outcomes:
        - `None` → room not found in rooms table  
        - `0`    → no matching reservation at that time for that room  
        - list   → one or more matching rows

        Validation:
            - Both datetime and room must be non-empty.
            - Datetime must match ``YYYY-MM-DD HH:MM``.
            - Room length must be ≤ 50 characters.

        Side Effects:
            - Writes a success/error line into `self.log`.
            - Repopulates the tree view when matches are found.
            - Clears the search inputs at the end.
        """
        dtime_input = self.dtime_entry.get().strip()
        room = self.search_room_entry.get().strip().title()

        if dtime_input != "" and room != "":

            try:
                dtime = datetime.strptime(dtime_input, "%Y-%m-%d %H:%M")
            except ValueError:
                self.log.add_message(f"Failed Search: {dtime_input} "
                                     f"must be in the 'YYYY-MM-DD HH:MM' format",
                                     False)
                self.clear_search_form()
                return

            if len(room) > 50:
                self.log.add_message(f"Failed Search: room name is too long",
                                     False)
                self.clear_search_form()
                return

            res = get_searched_details(self.server, dtime, room)
            # Room is not on the rooms table

            # Result messages mapper for getting searched details
            mes_mapper = {
                None: [f"Failed Search: reservation does not exist since"
                      f" {room} is not on rooms table", False],
                0: [f"Failed Search: {room} is not reserved at {dtime}.", False],
                True: [f"Successful Search: the reservation detail of {room} at "
                       f"{dtime} is found on the reservations table.", True]
            }

            if res is None:
                mes = mes_mapper.get(None)
                self.log.add_message(mes[0], mes[1])
                self.clear_search_form()
                return

            # Room is on rooms table but has no reservation made
            if res == 0:
                mes = mes_mapper.get(0)
                self.log.add_message(mes[0], mes[1])

            else:
                # Room is on rooms table and has reservation made
                self.details.delete(*self.details.get_children())
                self.configure(text="Search Results List")
                for i, r in enumerate(res):
                    if i % 2 != 0:
                        self.details.insert(parent="", index="end",
                                                 values=r,
                                                 tags=("odd",))
                    else:
                        self.details.insert(parent="", index="end",
                                                 values=r,
                                                 tags=("even",))
                mes = mes_mapper.get(True)
                self.log.add_message(mes[0], mes[1])
        else:
            messagebox.showwarning("Warning Message:",
                                   "Date and Time and Room cannot be empty.")

        self.clear_search_form()


# Advanced feature CSV (export the all details view into csv file) ===========
    def export_csv(self):
        """
        Export the 'All Details' data to a CSV file.

        Uses the provided path if specified; otherwise writes to
        ``exported_details.csv`` in the current working directory.
        If the file already exists, the user is prompted to confirm overwrite.

        The actual CSV contents are returned from the BLL call and written here.

        Side Effects:
            - Shows a confirmation dialog if the target file exists.
            - Writes a CSV file to disk on success.
            - Logs the outcome (message, success flag) to `self.log`.
            - Clears the path input at the end.
        """
        # Take the file path from the user
        path_str = self.path_entry.get().strip()

        # default path in current directory
        if path_str == "":
            path_str = "exported_details.csv"

        # if the path already exists, ask the users if continue
        if os.path.exists(path_str):
            response = messagebox.askyesno("Request Message: ",
                                      "The file already exists, would "
                                      "you like to overwrite it? ")
            if response is False:
                self.path_entry.delete(0, tk.END)
                return

        # Write the all details into the file path provided by user
        res = export_details(self.server, path_str)
        self.log.add_message(res[0], res[1])
        self.path_entry.delete(0, tk.END)