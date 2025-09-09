from tkinter import ttk, PhotoImage, Label
from pathlib import Path
from .logs import ActionLogFrame
from .tables import DinersFrame, PricesFrame, RoomsFrame, AllergiesFrame
from .tables import ReservationsFrame, AllDetailsFrame, RevenuesFrame
# Data manipulation layer ====================================
class DataFrame(ttk.LabelFrame):
    def __init__(self, parent, server, func_num, logs:ActionLogFrame):
        super().__init__(parent, style="Custom.TLabelframe", padding=5)

        self.server = server
        self.log = logs

        # Grid layer of output frame (1 row and 1 column)
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.num = func_num

        # Title mapper - titles will be matched with different tables/views
        titles = {
            1: "Diners Table",
            2: "Prices Table",
            3: "Rooms Table",
            4: "Allergies Table",
            5: "Reservations Table",
            6: "View All Reservation Details",
            7: "View Revenues By Class"
            # Default: SAKURA OMAKASE DATABASE
        }
        self.configure(text=titles.get(self.num, "SAKURA OMAKASE DATABASE"))

        if self.num == 1:
            self.diners = DinersFrame(self, self.server, self.log)
            self.diners.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        elif self.num == 2:
            self.prices = PricesFrame(self, self.server, self.log)
            self.prices.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        elif self.num == 3:
            self.rooms = RoomsFrame(self, self.server, self.log)
            self.rooms.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        elif self.num == 4:
            self.allergies = AllergiesFrame(self, self.server, self.log)
            self.allergies.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        elif self.num == 5:
            self.reservations = ReservationsFrame(self, self.server, self.log)
            self.reservations.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        elif self.num == 6:
            self.details = AllDetailsFrame(self, self.server, self.log)
            self.details.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        elif self.num == 7:
            self.revenues = RevenuesFrame(self, self.server, self.log)
            self.revenues.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        else:
            # Default Look
            # Create background image for data manipulation when loaded
            BASE_PATH = Path(__file__).resolve().parent / "images"
            self.bg = PhotoImage(file=str(BASE_PATH/"dash-bg.gif"))
            self.bg_label = Label(self, image=self.bg)
            # Take up 100% width and height of parent
            self.bg_label.place(relx=0, rely=0, relwidth=1, relheight=1)
