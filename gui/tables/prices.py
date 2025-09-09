import tkinter as tk
from tkinter import ttk, messagebox
from ..logs import ActionLogFrame
from ..widgets import Button, ButtonEntryFrame
from ...bll import get_all_prices, get_searched_class, add_class, update_class
# For Prices Table ----------------------------
class PricesFrame(ttk.LabelFrame):
    """
    The panel for listing, searching, adding, and updating class prices.

    Attributes:
        server (dict): Database connection configuration passed from the dashboard.
        log (ActionLogFrame): Log panel to display success/error messages.
        prices (ttk.Treeview): Tree view showing rows (ID, class name, cost per person).
        x_scroll (ttk.Scrollbar | None): Horizontal scrollbar for the tree view.
        y_scroll (ttk.Scrollbar | None): Vertical scrollbar for the tree view.
        button_frame (ttk.Frame): Container for the list/search controls row.
        full_btn (Button): Button that reloads the full price list.
        search_name (ButtonEntryFrame): Search input + button for class name.
        add_frame (ttk.LabelFrame): Container for the add-class form.
        name_entry (ttk.Entry): Input for class name (add).
        price_entry (ttk.Entry): Input for cost per person (add).
        add_btn (ttk.Button): Submits the add-class action.
        update_frame (ttk.LabelFrame): Container for the update form.
        new_name_entry (ttk.Entry): Input for new class name (update).
        new_price_entry (ttk.Entry): Input for new cost per person (update).
        update_btn (ttk.Button): Submits the update action.
        notice1 (ttk.Label): Instruction about selecting a row before update.
        notice2 (ttk.Label): Instruction about optional update fields.

    Args:
        parent (tk.Widget): Parent container.
        server (dict): Database connection details used by BLL calls.
        logs (ActionLogFrame): Shared action log instance.
    """
    def __init__(self, parent, server, logs:ActionLogFrame):
        super().__init__(parent, text="Full Prices List",
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

        # Display prices tree view ----------------------
        # First row
        self.prices = ttk.Treeview(self, padding=(0, 0, 10, 10))
        self.prices.grid(row=0, column=0, columnspan=4, padx=10, pady=10,
                         sticky="nsew")
        self.prices["columns"] = ("ID", "Class Name", "Cost Per Person")

        self.prices.column("#0", width=0, stretch=False)
        self.prices.column("ID", anchor="center", width=50)
        self.prices.column("Class Name", anchor="center", width=100)
        self.prices.column("Cost Per Person", anchor="center", width=150)

        self.prices.heading("#0", text="", anchor="center")
        self.prices.heading("ID", text="ID", anchor="center")
        self.prices.heading("Class Name", text="Class Name", anchor="center")
        self.prices.heading("Cost Per Person", text="Cost Per Person", anchor="center")
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
                                            "Search By Class Name",
                                            self.load_searched_data)
        self.search_name.grid(row=0, column=2, columnspan=2, padx=(30,0), sticky="ew")

        # Third row - add new class form
        self.add_frame = ttk.LabelFrame(self, text="Add New Classes", padding=3)
        self.add_frame.grid(row=2, column=0, columnspan=4, padx=5, sticky="ew")
        self.add_frame.rowconfigure(0, weight=1)
        self.add_frame.columnconfigure(0, weight=1)
        self.add_frame.columnconfigure(1, weight=1)
        self.add_frame.columnconfigure(2, weight=1)
        self.add_frame.columnconfigure(3, weight=1)
        self.add_frame.columnconfigure(4, weight=1)

        self.add_name = ttk.Label(self.add_frame,text="Class Name:",
                                  font=("Helvetica", 11))
        self.add_name.grid(row=0, column=0, sticky="e", padx=5)
        self.name_entry = ttk.Entry(self.add_frame)
        self.name_entry.grid(row=0, column=1, sticky="w", padx=5, ipadx=3, ipady=3)

        self.add_price = ttk.Label(self.add_frame, text="Cost Per Person:",
                                   font=("Helvetica", 11))
        self.add_price.grid(row=0, column=2, sticky="e", padx=5)
        self.price_entry = ttk.Entry(self.add_frame)
        self.price_entry.grid(row=0, column=3, sticky="w", padx=5, ipadx=3, ipady=3)

        self.add_btn = ttk.Button(self.add_frame, text="Add New Class",
                                  command=self.add_class, style="Special.TButton")
        self.add_btn.grid(row=0, column=4, sticky="ew", padx=15)

        # Fourth row - update class form
        self.update_frame = ttk.LabelFrame(self, text="Update Classes", padding=3)
        self.update_frame.grid(row=3, column=0, columnspan=4, padx=5, sticky="ew")
        self.update_frame.rowconfigure(0, weight=1)
        self.update_frame.columnconfigure(0, weight=1)
        self.update_frame.columnconfigure(1, weight=1)
        self.update_frame.columnconfigure(2, weight=1)
        self.update_frame.columnconfigure(3, weight=1)
        self.update_frame.columnconfigure(4, weight=1)

        self.update_name = ttk.Label(self.update_frame, text="Update Class Name:",
                                  font=("Helvetica", 11))
        self.update_name.grid(row=0, column=0, sticky="e", padx=5)
        self.new_name_entry = ttk.Entry(self.update_frame)
        self.new_name_entry.grid(row=0, column=1, sticky="w", padx=5, ipadx=3,
                             ipady=3)

        self.update_price = ttk.Label(self.update_frame, text="Update Cost/Per:",
                                   font=("Helvetica", 11))
        self.update_price.grid(row=0, column=2, sticky="e", padx=5)
        self.new_price_entry = ttk.Entry(self.update_frame)
        self.new_price_entry.grid(row=0, column=3, sticky="w", padx=5, ipadx=3,
                              ipady=3)

        self.update_btn = ttk.Button(self.update_frame, text="Update Class",
                                  command=self.update_class,
                                  style="Special.TButton")
        self.update_btn.grid(row=0, column=4, sticky="ew", padx=15)
        self.notice1 = ttk.Label(self.update_frame,
                                text="Please choose a record on full list before "
                                     "clicking the update button.",
                                font=("Helvetica", 8))
        self.notice1.grid(row=1, column=0, columnspan=5, pady=2)
        self.notice2 = ttk.Label(self.update_frame,
                                 text="You can leave either the update class name "
                                      "or new cost/per blank if not necessary"
                                      " to change.",
                                 font=("Helvetica", 8))
        self.notice2.grid(row=2, column=0, columnspan=5, pady=2)

    def create_scroll_bars(self):
        """
        Attach horizontal/vertical scrollbars to the prices tree view.

        Configures the tree view to use the created scrollbars.
        """
        # Scroll bars configuration
        self.x_scroll = ttk.Scrollbar(self.prices, orient="horizontal",
                                      command=self.prices.xview)
        self.y_scroll = ttk.Scrollbar(self.prices, orient="vertical",
                                      command=self.prices.yview)
        self.x_scroll.pack(side="bottom", fill="x")
        self.y_scroll.pack(side="right", fill="y")
        self.prices.configure(xscrollcommand=self.x_scroll.set,
                       yscrollcommand=self.y_scroll.set)

    def load_full_data(self):
        """
        Load and display the full prices list.

        Fetches all class prices via the BLL and populates the tree view.
        Uses alternating row tags ("odd"/"even") for readability and sets
        the label frame title to "Full Prices List".
        """
        self.prices.delete(*self.prices.get_children())
        self.configure(text="Full Prices List")
        prices = get_all_prices(self.server)
        self.prices.tag_configure("odd", background="white")
        self.prices.tag_configure("even", background="#E6E6E6")
        for i, p in enumerate(prices):
            if i % 2 != 0:
                self.prices.insert(parent="", index="end", values=p, tags=("odd",))
            else:
                self.prices.insert(parent="", index="end", values=p, tags=("even",))

    def load_searched_data(self):
        """
        Search classes by name and display the filtered list.

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
            res = get_searched_class(self.server, name)
            if res is not None:
                self.prices.delete(*self.prices.get_children())
                self.configure(text="Search Results List")
                for i, r in enumerate(res):
                    if i % 2 != 0:
                        self.prices.insert(parent="", index="end", values=r,
                                           tags=("odd",))
                    else:
                        self.prices.insert(parent="", index="end", values=r,
                                           tags=("even",))

                self.log.add_message(f"Successful Search: {name} class is on the prices table.")
            else:
                self.log.add_message(f"Failed Search: {name} class is not on the "
                                     f"prices table.", False)
        else:
            messagebox.showwarning("Warning Message:", "Class name "
                                                       "cannot be empty.")
        # Clear search box
        self.search_name.delete_input()

    def clear_record_for_add(self):
        """Clear the add-class form inputs (name and price)."""
        self.name_entry.delete(0, tk.END)
        self.price_entry.delete(0, tk.END)

    def clear_record_for_update(self):
        """Clear the update-class form inputs (new name and new price)."""
        self.new_name_entry.delete(0, tk.END)
        self.new_price_entry.delete(0, tk.END)

    def add_class(self):
        """
        Validate inputs and add a new price class.

        Validates the add-form inputs and calls the BLL to insert a class.
        On success, reloads the full list and logs the result. On error,
        logs an appropriate message and clears the form.

        Validation:
            - Class name cannot be empty and must be ≤ 50 characters.
            - Cost per person cannot be empty and must parse to a positive float.

        Side Effects:
            - On success, refreshes the tree view.
            - Always logs the outcome to `self.log`.
            - Clears the add-form fields at the end.
        """
        name = self.name_entry.get().strip().title()
        price = self.price_entry.get().strip()
        if name == "" or price == "":
            messagebox.showwarning("Warning Message:",
                                   "Class name or cost per person "                                                     
                                 " cannot be empty.")
            self.clear_record_for_add()
            return

        # Result message mapper
        mes_map = {
            True: [f"Successful to add class: {name} was "
                   f"added to the prices table.", True],
            -1: [f"Failed to add class: {name} class is "
                f"already on the prices table.", False],
            -2: ["Failed to add class: Cost Per Person must be positive", False],
            False: ["Failed to add class: Error occurred while working with "
                    "database. Please contact tech support", False],
            "long": ["Failed to add class: class name is too long.", False],
            "format": ["Failed to add class: Cost Per Person "
                       "must be a positive float or integer", False]
        }

        # Input validation: Class name is too long
        if len(name) > 50:
            mes1 = mes_map.get("long")
            self.log.add_message(mes1[0], mes1[1])
            self.clear_record_for_add()
            return

        # Input validation: Convert price to float
        try:
            price = float(price)
        except ValueError:
            mes2 = mes_map.get("format")
            self.log.add_message(mes2[0], mes2[1])
            self.clear_record_for_add()
            return

        # Add a price class by calling BLL method
        res = add_class(self.server, name, price)
        mes3 = mes_map.get(res)

        if res is True:
            self.load_full_data()

        self.log.add_message(mes3[0], mes3[1])
        self.clear_record_for_add()

    def update_class(self):
        """
        Validate inputs and update the selected price class.

        Reads the currently selected row and applies optional updates:
        - Rename class (if provided)
        - Change cost per person (if provided)

        Handles no-op cases (no effective change) and input validation
        before calling the BLL to perform the update. On success, the
        full list is reloaded and the outcome is logged.

        Validation:
            - A row must be selected before updating (user is warned if not).
            - New price, if provided, must parse to a positive float.
            - New class name, if provided, must be ≤ 50 characters.
            - Detects no-change scenarios and logs a friendly message.

        Side Effects:
            - On success, refreshes the tree view.
            - Always logs the outcome to `self.log`.
            - Clears the update-form fields at the end.
        """
        selected = self.prices.focus()
        if selected:
            res = self.prices.item(selected, "values")
            selected_class = res[1].strip()
            selected_price = res[2].replace("$", "")
            selected_price = float(selected_price)

            new_name_input= self.new_name_entry.get().strip().title()
            new_price_input= self.new_price_entry.get().strip()
            new_name = new_name_input if new_name_input != "" else None
            new_price = None

            # Result messages mapper
            mes_map = {
                True:[f"Successful update: The original "
                    f"{selected_class} class was updated.", True],
                -1: [f"Failed to update: {selected_class} is not found.",False],
                -2: [f"Failed to update {selected_class}: New class name already"
                     f" exists.", False],
                -3: [f"Failed to update {selected_class}: Inputs are unable to "
                     f"update record. Please try again.", False],
                -4: [f"Failed to update {selected_class}: "
                    f"the updated new cost must be positive.", False],
                False: ["Failed to update class: Error occurred while working with "
                    "database. Please contact tech support", False],
                "format": [f"Failed to update {selected_class}:Invalid type input. "
                        f"The new cost must be positive float or integer.", False],
                "no_change": [f"No need to update {selected_class} class: "
                    f"the updated record is the same as the previous record.", True],
                "long": [f"Failed to update {selected_class}: "
                f"because the updated class name is too long.", False]
            }

            # Input validation: new price input is not valid
            if new_price_input != "":
                try:
                    new_price = float(new_price_input)
                    if new_price <= 0:
                        # New price is not positive
                        mes1 = mes_map.get(-4)
                        self.log.add_message(mes1[0], mes1[1])
                        self.clear_record_for_update()
                        return
                except ValueError:
                    # New price is not integer or float
                    mes2 = mes_map.get("format")
                    self.log.add_message(mes2[0], mes2[1])
                    self.clear_record_for_update()
                    return

            # Input validation: no change made
            if ((new_name is None and new_price is None)
                or (new_name is None and new_price == selected_price)
                or (new_name == selected_class and new_price is None)
                or (new_name == selected_class and new_price == selected_price)):
                mes3 = mes_map.get("no_change")
                self.log.add_message(mes3[0], mes3[1])
                self.clear_record_for_update()
                return

            # Input validation: long name
            if new_name is not None and len(new_name) > 50:
                mes4 = mes_map.get("long")
                self.log.add_message(mes4[0], mes4[1])
                self.clear_record_for_update()
                return

            # Add price class by calling BLL method
            res = update_class(self.server, selected_class, new_name, new_price)

            mes5 = mes_map.get(res)

            if res is True:
                self.load_full_data()
            self.log.add_message(mes5[0], mes5[1])

        else:
            messagebox.showwarning("Warning Message",
            "Please select a record before clicking update button.")

        self.clear_record_for_update()