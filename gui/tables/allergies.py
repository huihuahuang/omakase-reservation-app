import tkinter as tk
from tkinter import ttk, messagebox
from ..widgets import Button, ButtonEntryFrame
from ..logs import ActionLogFrame
from ...bll import get_all_allergies, get_searched_allergy, delete_allergy, add_allergy
# For Allergies Table ----------------------------
class AllergiesFrame(ttk.LabelFrame):
    """
    The panel for listing, searching, adding, and deleting allergies.

    Renders a `ttk.Treeview` of allergy records and provides:
      - Quick search by diner name  
      - Add form (diner, type, level)  
      - Delete action for the selected row

    All successes and errors are written to the shared `ActionLogFrame`.

    Attributes:
        server (dict): Database connection configuration from the dashboard.
        log (ActionLogFrame): Log panel to display success/error messages.
        allergies (ttk.Treeview): Tree view (ID, Diner Name, Allergy Type, Level).
        x_scroll (ttk.Scrollbar | None): Horizontal scrollbar for the tree view.
        y_scroll (ttk.Scrollbar | None): Vertical scrollbar for the tree view.
        button_frame (ttk.Frame): Container for list/delete controls.
        full_btn (Button): Reloads the full allergies list.
        delete_btn (Button): Deletes the selected allergy record.
        search_name (ButtonEntryFrame): Search input + button (by diner name).
        notice1 (ttk.Label): Hint that a diner may have multiple allergies.
        add_frame (ttk.LabelFrame): Container for the add form.
        name_entry (ttk.Entry): Input for diner name (add).
        types (list[str]): Allowed allergy types.
        levels (list[str]): Allowed allergy levels.
        type_box (ttk.Combobox): Selector for allergy type (add).
        level_box (ttk.Combobox): Selector for allergy level (add).
        add_btn (ttk.Button): Submits the add-allergy action.

    Args:
        parent (tk.Widget): Parent container.
        server (dict): Database connection details used by BLL calls.
        logs (ActionLogFrame): Shared action log instance.
    """
    def __init__(self, parent, server, logs:ActionLogFrame):
        super().__init__(parent, text="Full Allergies List",
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


        # Display allergies tree view ----------------------
        # First row
        self.allergies = ttk.Treeview(self, padding=(0, 0, 10, 10))
        self.allergies.grid(row=0, column=0, columnspan=4, padx=10, pady=10,
                         sticky="nsew")
        self.allergies["columns"] = ("ID", "Diner Name", "Allergy Type", "Level")

        self.allergies.column("#0", width=0, stretch=False)
        self.allergies.column("ID", anchor="center", width=50)
        self.allergies.column("Diner Name", anchor="center", width=150)
        self.allergies.column("Allergy Type", anchor="center", width=150)
        self.allergies.column("Level", anchor="center", width=100)

        self.allergies.heading("#0", text="", anchor="center")
        self.allergies.heading("ID", text="ID", anchor="center")
        self.allergies.heading("Diner Name", text="Diner Name", anchor="center")
        self.allergies.heading("Allergy Type", text="Allergy Type", anchor="center")
        self.allergies.heading("Level", text="Level", anchor="center")

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
        self.delete_btn = Button(self.button_frame, "Delete Allergy",
                                 self.delete_allergy,
                                 0, 1)

        # Third row - search by diner name form
        self.search_name = ButtonEntryFrame(self, "Search By Diner Name",
                                       self.load_searched_data)
        self.search_name.grid(row=2, column=1, columnspan=2, sticky="ew")
        self.notice1 = ttk.Label(self.search_name,
                                 text="A diner might have multiple allergies.",
                                 font=("Helvetica", 8))
        self.notice1.grid(row=1, column=0, columnspan=2, pady=2)

        # Fourth row - add new allergy form
        self.add_frame = ttk.LabelFrame(self, text="Add New Allergies", padding=3)
        self.add_frame.grid(row=3, column=0, columnspan=4, padx=5, sticky="ew")
        self.add_frame.rowconfigure(0, weight=1)
        self.add_frame.rowconfigure(1, weight=1)
        self.add_frame.columnconfigure(0, weight=1)
        self.add_frame.columnconfigure(1, weight=1)
        self.add_frame.columnconfigure(2, weight=1)
        self.add_frame.columnconfigure(3, weight=1)
        self.add_frame.columnconfigure(4, weight=1)

        self.add_name = ttk.Label(self.add_frame,text="Diner Name:",
                                  font=("Helvetica", 11))
        self.add_name.grid(row=0, column=0, sticky="e", padx=5)
        self.name_entry = ttk.Entry(self.add_frame)
        self.name_entry.grid(row=0, column=1, sticky="w", padx=5, ipadx=3, ipady=3)

        self.add_type = ttk.Label(self.add_frame, text="Allergy Type:",
                                   font=("Helvetica", 11))
        self.add_type.grid(row=0, column=2, sticky="e", padx=5)

        self.types = ['Dairy', 'Shellfish', 'Nuts', 'Eggs', 'Sesame', 'Wheat', 'Soy']
        self.levels = ['Sensitive', 'Mild', 'Severe']

        self.type_box = ttk.Combobox(self.add_frame, values=self.types, state="readonly")
        self.type_box.grid(row=0, column=3, sticky="w", padx=5, ipadx=3, ipady=3)
        self.type_box.set(self.types[0])

        self.add_level = ttk.Label(self.add_frame, text="Allergy Level:",
                                  font=("Helvetica", 11))
        self.add_level.grid(row=1, column=0, sticky="e", padx=5)

        self.level_box = ttk.Combobox(self.add_frame, values=self.levels,
                                     state="readonly")
        self.level_box.grid(row=1, column=1, sticky="w", padx=5, ipadx=3,
                           ipady=3)
        self.level_box.set(self.levels[0])

        self.add_btn = ttk.Button(self.add_frame, text="Add New Record",
                                  command=self.add_allergy, style="Special.TButton")
        self.add_btn.grid(row=1, column=4, sticky="ew", padx=15)


    def create_scroll_bars(self):
        """
        Attach horizontal/vertical scrollbars to the allergies tree view.

        Configures the tree view to use the created scrollbars.

        Side Effects:
            Modifies `self.allergies` to connect x/y scroll commands.
            Creates and assigns `self.x_scroll` and `self.y_scroll`.
        """
        # Scroll bars configuration
        self.x_scroll = ttk.Scrollbar(self.allergies, orient="horizontal",
                                      command=self.allergies.xview)
        self.y_scroll = ttk.Scrollbar(self.allergies, orient="vertical",
                                      command=self.allergies.yview)
        self.x_scroll.pack(side="bottom", fill="x")
        self.y_scroll.pack(side="right", fill="y")
        self.allergies.configure(xscrollcommand=self.x_scroll.set,
                       yscrollcommand=self.y_scroll.set)

    def load_full_data(self):
        """
        Load and display the full allergies list.

        Fetches all allergy records via the BLL and populates the tree view.
        Uses alternating row tags ("odd"/"even") for readability and sets the
        label frame title to "Full Allergies List".
        """
        self.allergies.delete(*self.allergies.get_children())
        self.configure(text="Full Allergies List")
        records = get_all_allergies(self.server)
        self.allergies.tag_configure("odd", background="white")
        self.allergies.tag_configure("even", background="#E6E6E6")
        for i, p in enumerate(records):
            if i % 2 != 0:
                self.allergies.insert(parent="", index="end", values=p, tags=("odd",))
            else:
                self.allergies.insert(parent="", index="end", values=p, tags=("even",))

    def load_searched_data(self):
        """
        Search allergies by diner name and display filtered results.

        Reads the search input, normalizes it (title-case), and queries the BLL.
        Handles three outcomes:
        - `None`  → diner not found in diners table  
        - `0`     → diner has no allergies  
        - list    → one or more allergy rows

        Validation:
            - Warns if the search box is empty.

        Side Effects:
            - Writes a success/error line into `self.log`.
            - Clears the search input at the end.
        """
        name = self.search_name.get_input().strip().title()
        if name != "":

            res = get_searched_allergy(self.server, name)

            # Result messages mapper
            mes_mapper = {
                None: [f"Failed Search: the record of {name} is not on the allergies"
                       f" table since {name} is not on diners table", False],
                0: [f"Failed Search: {name} has no allergies.", False],
                True: [f"Successful Search: the record of {name} "
                      f"is on the allergies table.", True]

            }

            # Diner is not on the diners table
            # Or Diner is on diners table but has no allergy
            # Early exit
            if res is None:
                mes1 = mes_mapper.get(None)
                self.log.add_message(mes1[0], mes1[1])
                self.search_name.delete_input()
                return

            elif res == 0:
                mes2 = mes_mapper.get(0)
                self.log.add_message(mes2[0], mes2[1])
                self.search_name.delete_input()
                return

            else:
                # Diner is on diners table and has allergy record
                self.allergies.delete(*self.allergies.get_children())
                self.configure(text="Search Results List")
                mes3 = mes_mapper.get(True)
                for i, r in enumerate(res):
                    if i % 2 != 0:
                        self.allergies.insert(parent="", index="end", values=r,
                                                  tags=("odd",))
                    else:
                        self.allergies.insert(parent="", index="end", values=r,
                                                  tags=("even",))
                self.log.add_message(mes3[0], mes3[1])

        else:
            messagebox.showwarning("Warning Message:", "Diner name "
                                                       "cannot be empty.")
        # Clear search box
        self.search_name.delete_input()

    def delete_allergy(self):
        """
        Delete the currently selected allergy record.

        Prompts for confirmation, then calls the BLL to delete by
        (diner name, allergy type) taken from the selected row. Logs
        success or failure and reloads the full list.

        User Feedback:
            - Warns if no row is selected.
            - Confirmation dialog precedes deletion.

        Side Effects:
            - Refreshes the tree view after attempting deletion.
        """
        selected = self.allergies.focus()
        if selected:
            # Delete allergy by calling BLL method
            res = self.allergies.item(selected, "values")

            selected_diner = res[1]
            selected_type = res[2]
            reaction = messagebox.askyesno("Confirmation Message:",
            f"Are you sure to delete {selected_type} allergy of "
                    f"{selected_diner}?")

            if reaction:

                # Result messages mapper
                mes_mapper = {
                    True: [f"Successful deletion: {selected_diner}'s "
                           f"{selected_type} allergy was deleted.", True],
                    -1: [f"Failed deletion: The allergy record of {selected_diner}"
                        f"'s {selected_type} is not found.", False],
                    False: ["Failed to delete allergy: Error occurred while working "
                            "with database. Please contact tech support.", False]
                }

                res = delete_allergy(self.server, selected_diner, selected_type)

                mes = mes_mapper.get(res)
                self.log.add_message(mes[0], mes[1])

            # Load full list to reflect change or clear focus
            self.load_full_data()
        else:
            messagebox.showwarning("Warning Message",
                                   "Please select a record before clicking "
                                   "delete button.")

    def clear_record(self):
        """
        Clear the add-allergy form inputs and reset selectors.

        Resets diner name entry and reselects the first values in
        type and level comboboxes.
        """
        self.name_entry.delete(0, tk.END)
        self.type_box.set(self.types[0])
        self.level_box.set(self.levels[0])

    def add_allergy(self):
        """
        Validate inputs and add a new allergy record.

        Validates the add-form inputs and calls the BLL to insert an
        allergy for the specified diner. On success, reloads the full
        list and logs the result. On error, logs an appropriate message.

        Validation:
            - Diner name cannot be empty.
            - Diner name must be ≤ 50 characters.
            - Type and level must be chosen from allowed lists (enforced in BLL).

        Side Effects:
            - On success, refreshes the tree view.
            - Always logs the outcome to `self.log`.
            - Clears the add-form fields at the end.
        """
        name = self.name_entry.get().strip().title()
        allergy_type = self.type_box.get().strip().title()
        level = self.level_box.get().strip().title()

        if name == "":
            messagebox.showwarning("Warning Message:",
                                   "Diner name cannot be empty.")
            self.clear_record()
            return

        # Result messages mapper
        mes_mapper = {
            True: [f"Successful to add allergy record: {name}'s {allergy_type} allergy"
                    f" was added to the allergies table.", True],
            -1: [f"Failed to add allergy record: the {allergy_type} type or {level}"
                f" level is not on the list.", False],
            -2: [f"Failed to add allergy record: {name}'s not on the diners"
                f" table.", False],
            -3: [f"Failed to add allergy record: the {name}'s {allergy_type}"
                f" allergy record is already on the allergies table.", False],
            False: ["Failed to add allergy record: Error occurred while working "
                    "with database. Please contact tech support.", False],
            "long": ["Failed to add allergy record: diner name is too long.", False]
        }

        # Input validation: diner name is too long
        if len(name) > 50:
            mes1 = mes_mapper.get("long")
            self.log.add_message(mes1[0], mes1[1])
            self.clear_record()
            return

        # Add allergy by calling BLL method
        res = add_allergy(self.server, name, allergy_type, level)
        mes2 = mes_mapper.get(res)
        if res is True:
            # Successfully added
            self.load_full_data()
        self.log.add_message(mes2[0], mes2[1])
        self.clear_record()
