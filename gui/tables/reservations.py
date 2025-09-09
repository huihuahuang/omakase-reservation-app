import tkinter as tk
from datetime import datetime
from tkinter import ttk, messagebox
from ..widgets import Button
from ..logs import ActionLogFrame
from ...bll import get_all_reservations, get_searched_reservation
from ...bll import cancel_reservation, add_reservation
# For Reservations Table ----------------------------
class ReservationsFrame(ttk.LabelFrame):
    """
    The panel for listing, searching, adding, and deleting reservations.

    Renders a `ttk.Treeview` of reservations and provides:
      - Quick deletion of selected reservation  
      - Search by begin datetime + room name  
      - Add form (datetime, room, diner, group size)

    All successes and errors are written to the shared `ActionLogFrame`.

    Attributes:
        server (dict): Database connection configuration from the dashboard.
        log (ActionLogFrame): Log panel to display success/error messages.
        reservations (ttk.Treeview): Grid of (Date and Time, Room, Diner, Total).
        x_scroll (ttk.Scrollbar | None): Horizontal scrollbar for the tree view.
        y_scroll (ttk.Scrollbar | None): Vertical scrollbar for the tree view.
        button_frame (ttk.Frame): Container for list/delete controls.
        full_btn (Button): Reloads the full reservations list.
        delete_btn (Button): Deletes the selected reservation.
        search (ttk.LabelFrame): Container for search inputs.
        dtime_entry (ttk.Entry): Search input for datetime ("YYYY-MM-DD HH:MM").
        search_room_entry (ttk.Entry): Search input for room name.
        add_frame (ttk.LabelFrame): Container for the add-reservation form.
        add_dtime_entry (ttk.Entry): Add form datetime input.
        add_room_entry (ttk.Entry): Add form room input.
        add_diner_entry (ttk.Entry): Add form diner input.
        add_guests_entry (ttk.Entry): Add form group size input.
        add_btn (ttk.Button): Submits the add-reservation action.
        notice1 (ttk.Label): Format hint for search datetime.
        notice2 (ttk.Label): Business rules hint for add form.
        notice3 (ttk.Label): Duration/required-fields hint for add form.

    Args:
        parent (tk.Widget): Parent container.
        server (dict): Database connection details used by BLL calls.
        logs (ActionLogFrame): Shared action log instance.
    """
    def __init__(self, parent, server, logs:ActionLogFrame):
        super().__init__(parent, text="Full Reservations List",
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


        # Display reservations tree view ----------------------
        # First row
        self.reservations = ttk.Treeview(self, padding=(0, 0, 10, 10))
        self.reservations.grid(row=0, column=0, columnspan=4, padx=10, pady=10,
                         sticky="nsew")
        self.reservations["columns"] = ("Date and Time", "Room Name",
                                     "Diner Name", "Total Diners")

        self.reservations.column("#0", width=0, stretch=False)
        self.reservations.column("Date and Time", anchor="center", width=150)
        self.reservations.column("Room Name", anchor="center", width=150)
        self.reservations.column("Diner Name", anchor="center", width=150)
        self.reservations.column("Total Diners", anchor="center", width=50)

        self.reservations.heading("#0", text="", anchor="center")
        self.reservations.heading("Date and Time", text="Date and Time", anchor="center")
        self.reservations.heading("Room Name", text="Room Name", anchor="center")
        self.reservations.heading("Diner Name", text="Diner Name", anchor="center")
        self.reservations.heading("Total Diners", text="Total Diners", anchor="center")

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

        self.full_btn = Button(self.button_frame, "Full List",
                               self.load_full_data,0,0)
        self.delete_btn = Button(self.button_frame, "Delete Reservation",
                                 self.delete_reservation,
                                 0, 1)

        # Third row - search form
        self.search = ttk.LabelFrame(self,
                                     text="Search Reservations "
                                          "By DateAndTime (Begin date time) and "
                                          "Room Name",
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
        self.search_room_entry.grid(row=0, column=3, sticky="w", padx=5, ipadx=3,
                              ipady=3)

        self.search_btn = ttk.Button(self.search, text="Search Reservation",
                                  command=self.load_searched_data,
                                  style="Special.TButton")
        self.search_btn.grid(row=0, column=4, sticky="ew", padx=15)
        self.notice1 = ttk.Label(self.search,
                                 text="Date and time input must be in "
                                      "'YYYY-MM-DD HH:MM' format. "
                                      "For example: 2025-07-01 18:00",
                                 font=("Helvetica", 8))
        self.notice1.grid(row=2, column=0, columnspan=5, pady=2)

        # Fourth row - add reservation form
        self.add_frame = ttk.LabelFrame(self, text="Add Reservations", padding=3)
        self.add_frame.grid(row=3, column=0, columnspan=4, padx=5,
                               sticky="ew")
        self.add_frame.rowconfigure(0, weight=1)
        self.add_frame.rowconfigure(1, weight=1)
        self.add_frame.columnconfigure(0, weight=1)
        self.add_frame.columnconfigure(1, weight=1)
        self.add_frame.columnconfigure(2, weight=1)
        self.add_frame.columnconfigure(3, weight=1)
        self.add_frame.columnconfigure(4, weight=1)

        self.add_dtime = ttk.Label(self.add_frame,
                                     text="Date And Time:",
                                     font=("Helvetica", 11))
        self.add_dtime.grid(row=0, column=0, sticky="e", padx=5)
        self.add_dtime_entry = ttk.Entry(self.add_frame)
        self.add_dtime_entry.grid(row=0, column=1, sticky="w", padx=5,
                                    ipadx=3,
                                    ipady=3)

        self.add_room = ttk.Label(self.add_frame, text="Room Name:",
                                   font=("Helvetica", 11))
        self.add_room.grid(row=0, column=2, sticky="e", padx=5)
        self.add_room_entry = ttk.Entry(self.add_frame)
        self.add_room_entry.grid(row=0, column=3, sticky="w", padx=5,
                                  ipadx=3, ipady=3)


        self.add_diner = ttk.Label(self.add_frame, text="Diner Name:",
                                      font=("Helvetica", 11))
        self.add_diner.grid(row=1, column=0, sticky="e", padx=5)
        self.add_diner_entry = ttk.Entry(self.add_frame)
        self.add_diner_entry.grid(row=1, column=1, sticky="w", padx=5,
                                     ipadx=3, ipady=3)

        self.add_guests = ttk.Label(self.add_frame, text="Total Diners:",
                                      font=("Helvetica", 11))
        self.add_guests.grid(row=1, column=2, sticky="e", padx=5)
        self.add_guests_entry = ttk.Entry(self.add_frame)
        self.add_guests_entry.grid(row=1, column=3, sticky="w", padx=5,
                                     ipadx=3, ipady=3)

        self.add_btn = ttk.Button(self.add_frame, text="Add Reservation",
                                     command=self.add_reservation,
                                     style="Special.TButton")
        self.add_btn.grid(row=1, column=4, sticky="ew", padx=15)

        self.notice2 = ttk.Label(self.add_frame,
        text="All reservation times must be made between "
            "17:00 to 21:30 and at least two days prior. Store closes at 23:00. ",
        font=("Helvetica", 8))

        self.notice2.grid(row=2, column=0, columnspan=5, pady=2)
        self.notice3 = ttk.Label(self.add_frame,
                                 text="Each Omakase experience lasts 1.5 hours. "
                                      "All the input fields must be filled.",
                                 font=("Helvetica", 8))
        self.notice3.grid(row=3, column=0, columnspan=5, pady=2)



    def create_scroll_bars(self):
        """
        Attach horizontal/vertical scrollbars to the reservations tree view.

        Configures the tree view to use the created scrollbars.

        Side Effects:
            Modifies `self.reservations` to connect x/y scroll commands.
            Creates and assigns `self.x_scroll` and `self.y_scroll`.
        """
        # Scroll bars configuration
        self.x_scroll = ttk.Scrollbar(self.reservations, orient="horizontal",
                                      command=self.reservations.xview)
        self.y_scroll = ttk.Scrollbar(self.reservations, orient="vertical",
                                      command=self.reservations.yview)
        self.x_scroll.pack(side="bottom", fill="x")
        self.y_scroll.pack(side="right", fill="y")
        self.reservations.configure(xscrollcommand=self.x_scroll.set,
                       yscrollcommand=self.y_scroll.set)

    def load_full_data(self):
        """
        Load and display the full reservations list.

        Fetches all reservations via the BLL and populates the tree view.
        Uses alternating row tags ("odd"/"even") for readability and sets the
        label frame title to "Full Reservations List".
        """
        self.reservations.delete(*self.reservations.get_children())
        self.configure(text="Full Reservations List")
        records = get_all_reservations(self.server)
        self.reservations.tag_configure("odd", background="white")
        self.reservations.tag_configure("even", background="#E6E6E6")
        for i, r in enumerate(records):
            if i % 2 != 0:
                self.reservations.insert(parent="", index="end", values=r, tags=("odd",))
            else:
                self.reservations.insert(parent="", index="end", values=r, tags=("even",))

    def clear_search_form(self):
        """Clear the search inputs (datetime and room)."""
        self.dtime_entry.delete(0, tk.END)
        self.search_room_entry.delete(0, tk.END)

    def load_searched_data(self):
        """
        Search reservations by begin datetime and room name.

        Parses the datetime input, validates the room name length, and queries
        the BLL. Handles three outcomes:
        - `None` → room not found in rooms table  
        - `0`    → no reservation exists at that time for that room  
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

        # Input validation : empty fields are not allowed
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

            res = get_searched_reservation(self.server, dtime, room)

            # Result messages mapper
            mes_mapper = {
                None:[f"Failed Search: reservation does not exist since {room} is"
                      f" not on rooms table",False],
                0: [f"Failed Search: {room} is not reserved at {dtime}.",False],
                True: [f"Successful Search: the reservation of {room} at "
                       f"{dtime} is found on the reservations table.", True]
            }

            # Room is not on the rooms table
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
                self.reservations.delete(*self.reservations.get_children())
                self.configure(text="Search Results List")
                for i, r in enumerate(res):
                    if i % 2 != 0:
                        self.reservations.insert(parent="", index="end", values=r,
                                              tags=("odd",))
                    else:
                        self.reservations.insert(parent="", index="end", values=r,
                                              tags=("even",))

                mes = mes_mapper.get(True)
                self.log.add_message(mes[0], mes[1])
        else:
            messagebox.showwarning("Warning Message:",
                                   "Date and Time and Room cannot be empty.")

        self.clear_search_form()

    def delete_reservation(self):
        """
        Delete the currently selected reservation.

        Prompts for confirmation, then calls the BLL to delete by
        (datetime, room) from the selected row. Logs success or failure
        and reloads the full list to reflect changes.

        User Feedback:
            - Warns if no row is selected.
            - Confirmation dialog precedes deletion.

        Side Effects:
            - Refreshes the tree view after attempting deletion.
        """
        selected = self.reservations.focus()
        if selected:
            res = self.reservations.item(selected, "values")

            selected_dtime = res[0]
            selected_room = res[1]
            reaction = messagebox.askyesno("Confirmation Message:",
            f"Are you sure to delete {selected_room} reservation at "
            f"{selected_dtime}?")

            # Result messages mapper
            mes_mapper = {
                True: [f"Successful deletion: the reservation of {selected_room} "
                       f"at {selected_dtime} was cancelled.", True],
                -1 : [f"Failed deletion: the reservation of {selected_room} "
                      f"at {selected_dtime} is not found.", False],
                False: ["Failed to delete reservation: Error occurred while working "
                    "with database. Please contact tech support.", False]
            }

            if reaction:
                res = cancel_reservation(self.server, selected_dtime, selected_room)
                mes = mes_mapper.get(res)
                self.log.add_message(mes[0], mes[1])
            # Load full list to reflect change and clear focus
            self.load_full_data()
        else:
            messagebox.showwarning("Warning Message",
                                   "Please select a record before clicking "
                                   "delete button.")

    def clear_add_record(self):
        """Clear the add-reservation form inputs."""
        self.add_dtime_entry.delete(0, tk.END)
        self.add_room_entry.delete(0, tk.END)
        self.add_diner_entry.delete(0, tk.END)
        self.add_guests_entry.delete(0, tk.END)

    def add_reservation(self):
        """
        Validate inputs and add a new reservation.

        Validates and converts inputs, then calls the BLL to insert a new
        reservation. On success, reloads the full list and logs the result.

        Validation:
            - All fields are required (datetime, room, diner, total).
            - Datetime must match ``YYYY-MM-DD HH:MM``.
            - Room and diner names must be ≤ 50 characters.
            - Total diners must parse to an integer.
            - Business rules are enforced in BLL:
                * Reservations must be ≥ 2 days in advance.
                * Allowed times: 17:00 - 21:30 (store closes at 23:00).
                * Duration is 1.5 hours; overlaps are rejected.

        Side Effects:
            - On success, refreshes the tree view.
            - Always logs the outcome to `self.log`.
            - Clears the add form at the end.
        """
        dtime_str = self.add_dtime_entry.get().strip()
        room_input = self.add_room_entry.get().strip().title()
        diner_input = self.add_diner_entry.get().strip().title()
        guests_input = self.add_guests_entry.get().strip()

        # Input validation: empty inputs are not allowed
        if (dtime_str == "" or room_input == "" or diner_input == ""
                or guests_input == ""):
            messagebox.showwarning("Warning Message:",
                                   "Blank input field on update form "
                                   "is not allowed.")
            self.clear_add_record()
            return

        # Result messages mapper for validation
        mes_mapper1 = {
            "long": ["Failed to add reservation: diner or room name is too long.", False],
            "dformat": [f"Failed to add reservation: {dtime_str} must be in the"
                      f" 'YYYY-MM-DD HH:MM' format.", False],
            "format": [f"Failed to add reservation: Total diners must be integer.", False]
        }

        # Input validation : names are too long
        if len(room_input) > 50 or len(diner_input) > 50:
            mes1 = mes_mapper1.get("long")
            self.log.add_message(mes1[0], mes1[1])
            self.clear_add_record()
            return

        # Input validation: convert data type
        try:
            dtime = datetime.strptime(dtime_str, "%Y-%m-%d %H:%M")
        except ValueError:
            mes2 = mes_mapper1.get("dformat")
            self.log.add_message(mes2[0], mes2[1])
            self.clear_add_record()
            return


        try:
            guest_num = int(guests_input)
        except ValueError:
            mes3 = mes_mapper1.get("format")
            self.log.add_message(mes3[0], mes3[1])
            self.clear_add_record()
            return

        # Add reservation by calling BLL method
        res = add_reservation(self.server, dtime, room_input, diner_input, guest_num)

        # Result messages mapper for adding reservation
        mes_mapper2 = {
            True: [f"Successful to add reservation: {diner_input} has booked  "
                  f"{room_input} room with the group of {guest_num} at {dtime}.", True],
            -1: ["Failed to add reservation: the reserved time must be at least two"
                " days prior within available hours(17:00 - 21:30).", False],
            -2: ["Failed to add reservation: the group of diners must be one"
                " or more people. ", False],
            -3: [f"Failed to add reservation: the diner {diner_input} is "
                f"not on the diners list.", False],
            -4: [f"Failed to add reservation: the room {room_input} is not on"
                f" the rooms list.", False],
            -5: [f"Failed to add reservation: Both the room {room_input} and"
                f" the diner {diner_input} are not on the record. ", False],
            -6: [f"Failed to add reservation: Both the room {room_input} and"
                f" the diner {diner_input} are double-booked at {dtime}. ", False],
            -7: [f"Failed to add reservation: the room {room_input} is"
                f" double-booked at {dtime}. ", False],
            -8: [f"Failed to add reservation: the diner {diner_input} is"
                f" double-booked at {dtime}. ", False],
            False: ["Failed to add reservation: Error occurred while working "
                    "with database. Please contact tech support.", False]
        }

        if res is True:
            # Successfully added
            self.load_full_data()
        mes4 = mes_mapper2.get(res)
        self.log.add_message(mes4[0], mes4[1])
        self.clear_add_record()
