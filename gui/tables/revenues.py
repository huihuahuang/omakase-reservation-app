from tkinter import ttk, PhotoImage, Label
from pathlib import Path
from ..logs import ActionLogFrame
from ...bll import get_all_revenues
# For Total Revenue By Class View --------------------
class RevenuesFrame(ttk.LabelFrame):
    """
    The panel for displaying the 'Total Revenue by Class' view.

    Renders a `ttk.Treeview` showing aggregated diner counts and revenue
    per class, with a rolling total. Also places a background image to
    fill remaining space in the panel.

    Attributes:
        server (dict): Database connection configuration from the dashboard.
        log (ActionLogFrame): Log panel to display success/error messages.
        revenues (ttk.Treeview): Table widget with class/revenue info.
        x_scroll (ttk.Scrollbar | None): Horizontal scrollbar for the tree view.
        y_scroll (ttk.Scrollbar | None): Vertical scrollbar for the tree view.
        bg (PhotoImage): Background image resource for decoration.
        bg_label (Label): Label widget holding the background image.

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
        self.rowconfigure(0, weight=1, minsize=200)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.columnconfigure(3, weight=1)


        # Display all revenues tree view ----------------------
        # First row
        self.revenues = ttk.Treeview(self, padding=(0, 0, 10, 10))
        self.revenues.grid(row=0, column=0, columnspan= 4, padx=10, pady=10,
                           sticky="nsew")
        self.revenues["columns"] = ("Class Name", "Total Diners",
                                    "Total Revenue", "Rolling Total")

        self.revenues.column("#0", width=0, stretch=False)
        self.revenues.column("Class Name", anchor="center", width=100)
        self.revenues.column("Total Diners", anchor="center", width=100)
        self.revenues.column("Total Revenue", anchor="center", width=100)
        self.revenues.column("Rolling Total", anchor="center", width=100)

        self.revenues.heading("#0", text="", anchor="center")
        self.revenues.heading("Class Name", text="Class Name", anchor="center")
        self.revenues.heading("Total Diners", text="Total Diners", anchor="center")
        self.revenues.heading("Total Revenue", text="Total Revenue", anchor="center")
        self.revenues.heading("Rolling Total", text="Rolling Total", anchor="center")

        self.x_scroll = None
        self.y_scroll = None
        self.create_scroll_bars()
        self.load_full_data()

        # Second and Third row - display image
        # Fill empty space with image
        BASE_PATH = Path(__file__).resolve().parent.parent / "images"
        self.bg = PhotoImage(file=str(BASE_PATH/"revenues-bg.gif"))
        self.bg_label = Label(self, image=self.bg)
        self.bg_label.grid(row=1, column=1, rowspan=2, columnspan=2, padx=10, pady=10)


    def create_scroll_bars(self):
        """
        Attach horizontal/vertical scrollbars to the revenue tree view.

        Configures the tree view to use the created scrollbars.

        Side Effects:
            Modifies `self.revenues` to connect x/y scroll commands.
            Creates and assigns `self.x_scroll` and `self.y_scroll`.
        """
        # Scroll bars configuration
        self.x_scroll = ttk.Scrollbar(self.revenues, orient="horizontal",
                                      command=self.revenues.xview)
        self.y_scroll = ttk.Scrollbar(self.revenues, orient="vertical",
                                      command=self.revenues.yview)
        self.x_scroll.pack(side="bottom", fill="x")
        self.y_scroll.pack(side="right", fill="y")
        self.revenues.configure(xscrollcommand=self.x_scroll.set,
                               yscrollcommand=self.y_scroll.set)

    def load_full_data(self):
        """
        Load and display the full 'Total Revenue by Class' list.

        Fetches aggregated revenue data from the BLL and populates the tree view.
        Uses alternating row tags ("odd"/"even") for readability and updates the
        label frame title to "Full Revenue List".
        """
        self.revenues.delete(*self.revenues.get_children())
        self.configure(text="Full Revenue List")
        incomes = get_all_revenues(self.server)
        self.revenues.tag_configure("odd", background="white")
        self.revenues.tag_configure("even", background="#E6E6E6")
        for i, r in enumerate(incomes):
            if i % 2 != 0:
                self.revenues.insert(parent="", index="end", values=r,
                                    tags=("odd",))
            else:
                self.revenues.insert(parent="", index="end", values=r,
                                    tags=("even",))