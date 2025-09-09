import tkinter as tk
from tkinter import ttk, messagebox
from ..widgets import Button, ButtonEntryFrame
from ..logs import ActionLogFrame
from ...bll import get_all_rooms, get_searched_room, add_room, update_room
# For Rooms Table ----------------------------
class RoomsFrame(ttk.LabelFrame):
    """
    The panel for listing, searching, adding, and updating rooms.

    Renders a `ttk.Treeview` of rooms and provides:
      • Quick search (by room name)  
      • Add form (room name, has TV, class name)  
      • Update form (rename room, staff, TV flag, class name)

    All successes and errors are written to the shared `ActionLogFrame`.

    Attributes:
        server (dict): Database connection configuration passed from the dashboard.
        log (ActionLogFrame): Log panel to display success/error messages.
        rooms (ttk.Treeview): Tree view showing rows (Room, Staff, Class, HasTV).
        x_scroll (ttk.Scrollbar | None): Horizontal scrollbar for the tree view.
        y_scroll (ttk.Scrollbar | None): Vertical scrollbar for the tree view.
        button_frame (ttk.Frame): Container for the list/search controls row.
        full_btn (Button): Button that reloads the full rooms list.
        search_name (ButtonEntryFrame): Search input + button for room name.
        add_frame (ttk.LabelFrame): Container for the add-room form.
        name_entry (ttk.Entry): Input for room name (add).
        tv_options (list[str]): Display values for TV selection ("Yes 1", "No 0").
        tv_box (ttk.Combobox): Selector for TV flag (add).
        class_entry (ttk.Entry): Input for class name (add).
        add_btn (ttk.Button): Submits the add-room action.
        update_frame (ttk.LabelFrame): Container for the update form.
        update_name_entry (ttk.Entry): Input for new room name.
        update_tv_box (ttk.Combobox): Selector for TV flag (update).
        update_staff_entry (ttk.Entry): Input for staff name (update).
        update_class_entry (ttk.Entry): Input for class name (update).
        update_btn (ttk.Button): Submits the update-room action.
        notice1 (ttk.Label): Instruction about selecting a row before update.
        notice2 (ttk.Label): Instruction about optional update fields.

    Args:
        parent (tk.Widget): Parent container.
        server (dict): Database connection details used by BLL calls.
        logs (ActionLogFrame): Shared action log instance.
    """
    def __init__(self, parent, server, logs:ActionLogFrame):
        super().__init__(parent, text="Full Rooms List",
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

        # Display rooms tree view ----------------------
        # First row
        self.rooms = ttk.Treeview(self, padding=(0, 0, 10, 10))
        self.rooms.grid(row=0, column=0, columnspan=4, padx=10, pady=10,
                         sticky="nsew")
        self.rooms["columns"] = ("Room", "Staff", "Class", "HasTV")

        self.rooms.column("#0", width=0, stretch=False)
        self.rooms.column("Room", anchor="center", width=50)
        self.rooms.column("Staff", anchor="center", width=100)
        self.rooms.column("Class", anchor="center", width=150)
        self.rooms.column("HasTV", anchor="center", width=150)

        self.rooms.heading("#0", text="", anchor="center")
        self.rooms.heading("Room", text="Room", anchor="center")
        self.rooms.heading("Staff", text="Staff", anchor="center")
        self.rooms.heading("Class", text="Class", anchor="center")
        self.rooms.heading("HasTV", text="HasTV", anchor="center")

        self.x_scroll = None
        self.y_scroll = None
        self.create_scroll_bars()
        self.load_full_data()

        # Display action buttons  ----------------------
        # Second row
        self.button_frame = ttk.Frame(self)
        self.button_frame.grid(row=1, column=0, columnspan=4, sticky="ew")
        self.button_frame.rowconfigure(0, weight=1)
        self.button_frame.columnconfigure(0, weight=1)
        self.button_frame.columnconfigure(1, weight=1)
        self.button_frame.columnconfigure(2, weight=1)
        self.button_frame.columnconfigure(3, weight=1)
        self.button_frame.columnconfigure(4, weight=1)
        self.full_btn = Button(self.button_frame, "Full List",
                               self.load_full_data, 0, 1)

        self.search_name = ButtonEntryFrame(self.button_frame,
                                            "Search By Room Name",
                                            self.load_searched_data)
        self.search_name.grid(row=0, column=2, columnspan=2, padx=(30,0), sticky="ew")

        # Third row - add new room form
        self.add_frame = ttk.LabelFrame(self, text="Add New Rooms",padding=3)
        self.add_frame.grid(row=2, column=0, columnspan=4, padx=5, sticky="ew")
        self.add_frame.rowconfigure(0, weight=1)
        self.add_frame.rowconfigure(1, weight=1)
        self.add_frame.columnconfigure(0, weight=1)
        self.add_frame.columnconfigure(1, weight=1)
        self.add_frame.columnconfigure(2, weight=1)
        self.add_frame.columnconfigure(3, weight=1)

        self.add_name = ttk.Label(self.add_frame,text="Room Name:",
                                  font=("Helvetica", 11))
        self.add_name.grid(row=0, column=0, sticky="e", padx=5)
        self.name_entry = ttk.Entry(self.add_frame)
        self.name_entry.grid(row=0, column=1, sticky="w", padx=5, ipadx=3, ipady=3)

        self.add_tv = ttk.Label(self.add_frame, text="Has TV:",
                                   font=("Helvetica", 11))
        self.add_tv.grid(row=0, column=2, sticky="e", padx=5)
        self.tv_options = ["Yes 1", "No 0"]
        self.tv_box = ttk.Combobox(self.add_frame, values=self.tv_options, state="readonly")
        self.tv_box.grid(row=0, column=3, sticky="w", padx=5, ipadx=3, ipady=3)
        self.tv_box.set(self.tv_options[0])   # Default value is yes

        self.add_class = ttk.Label(self.add_frame, text="Class Name:",
                                  font=("Helvetica", 11))
        self.add_class.grid(row=1, column=0, sticky="e", padx=5)
        self.class_entry = ttk.Entry(self.add_frame)
        self.class_entry.grid(row=1, column=1, sticky="w", padx=5, ipadx=3,
                             ipady=3)

        self.add_btn = ttk.Button(self.add_frame, text="Add New Room",
                                  command=self.add_room, style="Special.TButton")
        self.add_btn.grid(row=1, column=4, sticky="ew", padx=15)

        # Fourth row - update room form
        self.update_frame = ttk.LabelFrame(self, text="Update Rooms",padding=3)
        self.update_frame.grid(row=3, column=0, columnspan=4, padx=5,sticky="ew")
        self.update_frame.rowconfigure(0, weight=1)
        self.update_frame.rowconfigure(1, weight=1)
        self.update_frame.columnconfigure(0, weight=1)
        self.update_frame.columnconfigure(1, weight=1)
        self.update_frame.columnconfigure(2, weight=1)
        self.update_frame.columnconfigure(3, weight=1)
        self.update_frame.columnconfigure(4, weight=1)


        self.update_name = ttk.Label(self.update_frame, text="Update Room Name:",
                                  font=("Helvetica", 11))
        self.update_name.grid(row=0, column=0, sticky="e", padx=5)
        self.update_name_entry = ttk.Entry(self.update_frame)
        self.update_name_entry.grid(row=0, column=1, sticky="w", padx=5, ipadx=3,
                             ipady=3)

        self.update_tv = ttk.Label(self.update_frame, text="Has TV:",
                                font=("Helvetica", 11))
        self.update_tv.grid(row=0, column=2, sticky="e", padx=5)
        self.update_tv_box = ttk.Combobox(self.update_frame, values=self.tv_options,
                                   state="readonly")
        self.update_tv_box.grid(row=0, column=3, sticky="w", padx=5, ipadx=3, ipady=3)
        self.update_tv_box.set(self.tv_options[0])

        self.update_staff = ttk.Label(self.update_frame, text="Update Staff:",
                                font=("Helvetica", 11))
        self.update_staff.grid(row=1, column=0, sticky="e", padx=5)
        self.update_staff_entry = ttk.Entry(self.update_frame)
        self.update_staff_entry.grid(row=1, column=1, sticky="w", padx=5,
                                     ipadx=3, ipady=3)

        self.update_class = ttk.Label(self.update_frame, text="Update Class:",
                                      font=("Helvetica", 11))
        self.update_class.grid(row=1, column=2, sticky="e", padx=5)
        self.update_class_entry = ttk.Entry(self.update_frame)
        self.update_class_entry.grid(row=1, column=3, sticky="w", padx=5,
                                     ipadx=3, ipady=3)


        self.update_btn = ttk.Button(self.update_frame, text="Update Room",
                                  command=self.update_room,
                                  style="Special.TButton")
        self.update_btn.grid(row=1, column=4, sticky="ew", padx=15)

        self.notice1 = ttk.Label(self.update_frame,
                                text="Please choose a record on full list before "
                                     "clicking the update button.",
                                font=("Helvetica", 8))
        self.notice1.grid(row=2, column=0, columnspan=5, pady=2)
        self.notice2 = ttk.Label(self.update_frame,
                                 text="You can leave fields blank if not "
                                      "necessary to change. It supposes staff "
                                      "name is on employees record.",
                                 font=("Helvetica", 8))
        self.notice2.grid(row=3, column=0, columnspan=5, pady=2)

    def create_scroll_bars(self):
        """
        Attach horizontal/vertical scrollbars to the rooms tree view.

        Configures the tree view to use the created scrollbars.
        """
        # Scroll bars configuration
        self.x_scroll = ttk.Scrollbar(self.rooms, orient="horizontal",
                                      command=self.rooms.xview)
        self.y_scroll = ttk.Scrollbar(self.rooms, orient="vertical",
                                      command=self.rooms.yview)
        self.x_scroll.pack(side="bottom", fill="x")
        self.y_scroll.pack(side="right", fill="y")
        self.rooms.configure(xscrollcommand=self.x_scroll.set,
                       yscrollcommand=self.y_scroll.set)

    def load_full_data(self):
        """
        Load and display the full rooms list.

        Fetches all rooms via the BLL and populates the tree view.
        Uses alternating row tags ("odd"/"even") for readability and
        sets the label frame title to "Full Rooms List".
        """
        self.rooms.delete(*self.rooms.get_children())
        self.configure(text="Full Rooms List")
        rooms = get_all_rooms(self.server)
        self.rooms.tag_configure("odd", background="white")
        self.rooms.tag_configure("even", background="#E6E6E6")
        for i, r in enumerate(rooms):
            if i % 2 != 0:
                self.rooms.insert(parent="", index="end", values=r, tags=("odd",))
            else:
                self.rooms.insert(parent="", index="end", values=r, tags=("even",))

    def load_searched_data(self):
        """
        Search rooms by name and display the filtered list.

        Reads the search input, normalizes it (title-case), and queries the
        BLL for matches. If results are found, repopulates the tree view and
        sets the title to "Search Results List"; otherwise, logs a failure.

        Validation:
            - Warns if the search box is empty.

        Side Effects:
            - Writes a success/error line into `self.log`.
            - Clears the search input at the end.
        """
        name = self.search_name.get_input().strip().title()
        if name != "":
            res = get_searched_room(self.server, name)

            if res is not None:
                self.rooms.delete(*self.rooms.get_children())
                self.configure(text="Search Results List")
                for i, r in enumerate(res):
                    if i % 2 != 0:
                        self.rooms.insert(parent="", index="end", values=r,
                                           tags=("odd",))
                    else:
                        self.rooms.insert(parent="", index="end", values=r,
                                           tags=("even",))

                self.log.add_message(f"Successful Search: {name} room is on the rooms table.")
            else:
                self.log.add_message(f"Failed Search: {name} room is not on the "
                                     f"rooms table.", False)
        else:
            messagebox.showwarning("Warning Message:", "Room name "
                                                       "cannot be empty.")
        # Clear search box
        self.search_name.delete_input()

    def clear_record_for_add(self):
        """
        Clear the add-room form inputs.

        Resets room name, class name, and TV selection to defaults.
        """
        self.name_entry.delete(0, tk.END)
        self.class_entry.delete(0, tk.END)
        self.tv_box.set(self.tv_options[0])

    def clear_record_for_update(self):
        """
        Clear the update-room form inputs.

        Resets new room name, class name, staff name, and TV selection.
        """
        self.update_name_entry.delete(0, tk.END)
        self.update_class_entry.delete(0, tk.END)
        self.update_tv_box.set(self.tv_options[0])
        self.update_staff_entry.delete(0, tk.END)

    def add_room(self):
        """
        Validate inputs and add a new room.

        Validates the add-form inputs and calls the BLL to insert a room.
        On success, reloads the full list and logs the result. On error,
        logs an appropriate message and clears the form.

        Validation:
            - Room name and class name cannot be empty.
            - Room name and class name must be ≤ 50 characters.
            - TV flag is derived from combobox ("Yes 1" → 1, "No 0" → 0).

        Side Effects:
            - On success, refreshes the tree view.
            - Always logs the outcome to `self.log`.
            - Clears the add-form fields at the end.
        """
        name = self.name_entry.get().strip().title()
        class_name = self.class_entry.get().strip().title()
        tv = self.tv_box.get().lower()
        tv = 1 if tv == "yes 1" else 0

        # Input validation: warning for empty fields
        if name == "" or class_name == "":
            messagebox.showwarning("Warning Message:",
                                   "Room name or Class name cannot be empty.")
            return

        # Result messages mapper
        mes_mapper = {
            True: [f"Successful to add room: {name} was added to the rooms "
                   f"table.", True],
            -2: [f"Failed to add room: {class_name} class is not on the prices "
                "table.", False],
            -3: [f"Failed to add room: {name} room is already on the rooms "
                "table.", False],
            -4: [f"Failed to add room: {name} room is already on the rooms table"
                f" and {class_name} class does not exist", False],
            False: ["Failed to add room: Error occurred while working with "
                    "database. Please contact tech support.", False],
            "long":["Failed to add room: room name or class name is too long.", False],
        }

        # Input validation: names are too long
        if len(name) > 50 or len(class_name) > 50:
            mes1 = mes_mapper.get("long")
            self.log.add_message(mes1[0], mes1[1])
            self.clear_record_for_add()
            return

        res = add_room(self.server, name, tv, class_name)
        mes2 = mes_mapper.get(res)
        if res is True:
            self.load_full_data()

        self.log.add_message(mes2[0], mes2[1])
        self.clear_record_for_add()

    def update_room(self):
        """
        Validate inputs and update the selected room.

        Reads the selected row and applies optional updates:
        - Rename room  
        - Change staff  
        - Toggle TV flag  
        - Change class name

        Handles no effective change and input validation
        before calling the BLL to perform the update. On success, the
        full list is reloaded and the outcome is logged.

        Validation:
            - A row must be selected before updating (user is warned if not).
            - Updated room/staff/class names (if provided) must be ≤ 50 characters.
            - TV flag is parsed from combobox selection.

        Side Effects:
            - On success, refreshes the tree view.
            - Always logs the outcome to `self.log`.
            - Clears the update-form fields at the end.
        """
        selected = self.rooms.focus()
        if selected:
            res = self.rooms.item(selected, "values")

            selected_room = res[0].strip()
            selected_staff = res[1].strip()
            selected_class = res[2].strip()
            selected_tv = res[3].strip().lower()
            selected_tv = 1 if selected_tv == "yes" else 0

            # Get inputs
            update_name_input= self.update_name_entry.get().strip().title()
            update_staff_input= self.update_staff_entry.get().strip().title()
            update_class_input = self.update_class_entry.get().strip().title()
            update_tv_input = self.update_tv_box.get().lower()

            # Modify inputs
            update_name= update_name_input if update_name_input != "" else None
            update_staff = update_staff_input if update_staff_input != "" else None
            update_class_name = update_class_input if update_class_input != "" else None
            update_tv = 1 if update_tv_input == "yes 1" else 0

            # Result messages mapper
            mes_map = {
                True: [f"Successful update: The original {selected_room} room was"
                       f" updated.", True],
                -1: [f"Failed to update: {selected_room} is not found on the"
                    f" rooms table.",False],
                -2: [f"Failed to update: {update_class_name} is not on the prices "
                    f"table.", False],
                -3: [f"Failed to update: {update_name} is already on the rooms"
                    f" table.", False],
                False: ["Failed to update room: Error occurred while working with "
                        "database. Please contact tech support.", False],
                "no_change": [f"No need to update {selected_room} room: the updated "
                              f"record is the same as the previous record.", True],
                "long": [f"Failed to update {selected_class}: because the updated"
                        f" room name or staff name or class name is too long.", False]
            }


            # Input validation: no change made
            if ((update_name is None or update_name == selected_room)
                and (update_staff is None or update_staff == selected_staff)
                and (update_tv is None or update_tv == selected_tv)
                and (update_class_name is None or update_class_name == selected_class)):
                mes1 = mes_map.get("no_change")
                self.log.add_message(mes1[0], mes1[1])
                self.clear_record_for_update()
                return

            # Input validation: inputs are too long
            if ((update_name is not None and len(update_name) > 50)
                    or (update_staff is not None and len(update_staff) > 50))\
                    or (update_class_name is not None and len(update_class_name) > 50):
                mes2 = mes_map.get("long")
                self.log.add_message(mes2[0], mes2[1])
                self.clear_record_for_update()
                return


            res = update_room(self.server, selected_room, update_name,
                              update_tv, update_staff, update_class_name )
            mes3 = mes_map.get(res)
            if res is True:
                # Successfully update
                self.load_full_data()
            self.log.add_message(mes3[0], mes3[1])

        else:
            messagebox.showwarning("Warning Message",
            "Please select a record before clicking update button.")
        self.clear_record_for_update()
