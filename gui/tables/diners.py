import re
import tkinter as tk
from tkinter import ttk, messagebox
from ..widgets import Button, ButtonEntryFrame
from ..logs import ActionLogFrame
from ...bll import get_all_diners, get_searched_diner, add_diner, delete_diner
# For Diners Table ----------------------------
class DinersFrame(ttk.LabelFrame):
    """
    UI panel for listing, searching, adding, and deleting diners.

    This frame renders a `ttk.Treeview` with all diners, provides a
    search box (by diner name), an add form (name + phone), and a delete
    action for the selected row. All results and errors are reported to
    the shared `ActionLogFrame`.

    Attributes:
        server (dict): Database connection configuration passed from the dashboard.
        log (ActionLogFrame): Log panel to display success/error messages.
        diners (ttk.Treeview): Tree view showing diner rows (ID, name, phone).
        x_scroll (ttk.Scrollbar | None): Horizontal scrollbar for the tree view.
        y_scroll (ttk.Scrollbar | None): Vertical scrollbar for the tree view.
        button_frame (ttk.Frame): Container for the list/delete buttons row.
        full_btn (Button): Triggers full list reload.
        delete_btn (Button): Deletes the selected diner.
        search_name (ButtonEntryFrame): Search box + button (by diner name).
        add_frame (ttk.LabelFrame): Container for the add-diner form.
        name_entry (ttk.Entry): Input for diner name.
        phone_entry (ttk.Entry): Input for diner phone number.
        add_btn (ttk.Button): Submits the add-diner action.
        notice (ttk.Label): Helper text describing phone number format.

    Args:
        parent (tk.Widget): Parent container.
        server (dict): Database connection details used by BLL calls.
        logs (ActionLogFrame): Shared action log instance.
    """
    def __init__(self, parent, server, logs:ActionLogFrame):
        super().__init__(parent, text="Full Diners List",
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


        # Display diners tree view ----------------------
        # First row
        self.diners = ttk.Treeview(self, padding=(0, 0, 10, 10))
        self.diners.grid(row=0, column=0, columnspan=4, padx=10, pady=10,
                         sticky="nsew")
        self.diners["columns"] = ("ID", "Diner Name", "Phone")

        self.diners.column("#0", width=0, stretch=False)
        self.diners.column("ID", anchor="center", width=50)
        self.diners.column("Diner Name", anchor="center", width=100)
        self.diners.column("Phone", anchor="center", width=150)

        self.diners.heading("#0", text="", anchor="center")
        self.diners.heading("ID", text="ID", anchor="center")
        self.diners.heading("Diner Name", text="Diner Name", anchor="center")
        self.diners.heading("Phone", text="Phone", anchor="center")
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
        self.delete_btn = Button(self.button_frame, "Delete Diner", self.delete_diner,
                                 0, 1)

        # Third row - search by diner name form
        self.search_name = ButtonEntryFrame(self, "Search By Diner Name",
                                       self.load_searched_data)
        self.search_name.grid(row=2, column=1, columnspan=2, sticky="ew")

        # Fourth row - add new diner form
        self.add_frame = ttk.LabelFrame(self, text="Add New Diners", padding=3)
        self.add_frame.grid(row=3, column=0, columnspan=4, padx=5, sticky="ew")
        self.add_frame.rowconfigure(0, weight=1)
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

        self.add_phone = ttk.Label(self.add_frame, text="Phone Number:",
                                   font=("Helvetica", 11))
        self.add_phone.grid(row=0, column=2, sticky="e", padx=5)
        self.phone_entry = ttk.Entry(self.add_frame)
        self.phone_entry.grid(row=0, column=3, sticky="w", padx=5, ipadx=3, ipady=3)

        self.add_btn = ttk.Button(self.add_frame, text="Add New Diner",
                                  command=self.add_diner, style="Special.TButton")
        self.add_btn.grid(row=0, column=4, sticky="ew", padx=15)

        self.notice = ttk.Label(self.add_frame,
                                text="Phone number must be in xxx-xxx-xxxx format.",
                                font=("Helvetica", 8))
        self.notice.grid(row=1, column=2, columnspan=2, pady=2)

    def create_scroll_bars(self):
        """Attach horizontal/vertical scrollbars to the diners tree view."""
        # Scroll bars configuration
        self.x_scroll = ttk.Scrollbar(self.diners, orient="horizontal",
                                      command=self.diners.xview)
        self.y_scroll = ttk.Scrollbar(self.diners, orient="vertical",
                                      command=self.diners.yview)
        self.x_scroll.pack(side="bottom", fill="x")
        self.y_scroll.pack(side="right", fill="y")
        self.diners.configure(xscrollcommand=self.x_scroll.set,
                       yscrollcommand=self.y_scroll.set)

    def load_full_data(self):
        """
        Load and display the full diners list.

        Fetches all diners via the BLL and populates the tree view. Applies
        alternating row tags ("odd"/"even") for readability and updates the
        label frame title to "Full Diners List".
        """
        self.diners.delete(*self.diners.get_children())
        self.configure(text="Full Diners List")
        guests = get_all_diners(self.server)
        self.diners.tag_configure("odd", background="white")
        self.diners.tag_configure("even", background="#E6E6E6")
        for i, p in enumerate(guests):
            if i % 2 != 0:
                self.diners.insert(parent="", index="end", values=p, tags=("odd",))
            else:
                self.diners.insert(parent="", index="end", values=p, tags=("even",))

    def load_searched_data(self):
        """
        Search diners by name and display the filtered list.

        Reads the name from `self.search_name`, normalizes it (title-case),
        and queries the BLL. If results are found, the tree view is
        repopulated with "Search Results List" as the title; otherwise a log
        message indicates no match.

        Validation:
            - Warns if the search box is empty.

        Side Effects:
            - Writes a success/error line into `self.log`.
            - Clears the search input at the end.
        """
        name = self.search_name.get_input().strip().title()
        if name != "":
            res = get_searched_diner(self.server, name)
            if res is not None:
                self.diners.delete(*self.diners.get_children())
                self.configure(text="Search Results List")
                for i, r in enumerate(res):
                    if i % 2 != 0:
                        self.diners.insert(parent="", index="end", values=r,
                                           tags=("odd",))
                    else:
                        self.diners.insert(parent="", index="end", values=r,
                                           tags=("even",))

                self.log.add_message(f"Successful Search: {name} is on the diners table.")
            else:
                self.log.add_message(f"Failed Search: {name} is not on the "
                                     f"diners table.", False)
        else:
            messagebox.showwarning("Warning Message:", "Diner name "
                                                       "cannot be empty.")
        self.search_name.delete_input()

    def delete_diner(self):
        """
        Delete the currently selected diner.

        Prompts for confirmation, then calls the BLL to delete by diner name
        (selected row). Logs a success or error message, and refreshes the
        full list to reflect changes.

        User Feedback:
            - Warns if no row is selected.
            - Confirmation dialog before deletion.

        Side Effects:
            - Reloads the full diners list after attempting deletion.
            - Clears the search input at the end.
        """
        selected = self.diners.focus()
        if selected:
            res = self.diners.item(selected, "values")
            # Only delete one record each time
            selected_diner = res[1]
            reaction = messagebox.askyesno("Confirmation Message:",
                                      f"Are you sure to delete "
                                      f"{selected_diner}?")
            if reaction:
                mes = delete_diner(self.server, selected_diner)

                # Results message mapper
                mes_map = {
                    True: [f"Successful deletion: {selected_diner} was deleted.", True],
                    -1: [f"Failed deletion: {selected_diner} is not found.", False],
                    False: ["Failed deletion: Error occurred while working with "
                            "database. Please contact tech support", False]
                }
                res = mes_map.get(mes)
                self.log.add_message(res[0], res[1])

            # Load full list to reflect change and clear focus
            self.load_full_data()
        else:
            messagebox.showwarning("Warning Message",
                                   "Please select a record before clicking "
                                   "delete button.")
        # Clear search box
        self.search_name.delete_input()

    def clear_record(self):
        """Clear the add-diner form inputs (name and phone)."""
        self.name_entry.delete(0, tk.END)
        self.phone_entry.delete(0, tk.END)

    def add_diner(self):
        """
        Validate inputs and add a new diner.

        Validates the add-form inputs and calls the BLL to insert a diner.
        On success, reloads the full list and logs the result. On error,
        logs an appropriate message and clears the form.

        Validation:
            - Name and phone cannot be empty.
            - Name length must be ≤ 50 chars.
            - Phone must match US format: ``xxx-xxx-xxxx``.

        Side Effects:
            - On success, refreshes the tree view.
            - Always logs the outcome to `self.log`.
            - Clears the add-form fields at the end.
        """
        name = self.name_entry.get().strip().title()
        phone = self.phone_entry.get().strip()

        # Results message mapper
        mes_map = {
            True: [f"Successful to add diner: {name} was "
                   f"added to the diners table.", True],
            -1: [f"Failed to add diner: {name} is "
                 f"already on the diners table.", False],
            False: ["Failed to add diner: Error occurred while working with "
                    "database. Please contact tech support", False],
            "long": ["Failed to add diner: diner name is too long.", False],
            "format": ["Failed to add diner: US phone number only or it is "                   
                "not in xxx-xxx-xxxx format.", False]
        }

        # Input validation: name or phone can't be empty
        if name == "" or phone == "":
            messagebox.showwarning("Warning Message:","Diner name "
                                 "or phone number cannot be empty.")
            self.clear_record()
            return

        # Input validation: diner name is too long
        if len(name) > 50:
            mes1 = mes_map.get("long")
            self.log.add_message(mes1[0], mes1[1])
            self.clear_record()
            return

        # Input validation: phone number format does not match
        if not re.match(r"^\d{3}-\d{3}-\d{4}$", phone):
            mes2 = mes_map.get("format")
            self.log.add_message(mes2[0], mes2[1])
            self.clear_record()
            return

        # Add diner by calling BLL method
        res = add_diner(self.server, name, phone)

        mes3 = mes_map.get(res)
        if res is True:
            self.load_full_data()

        self.log.add_message(mes3[0], mes3[1])
        self.clear_record()
