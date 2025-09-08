import tkinter as tk
from tkinter import ttk
class ButtonEntryFrame(ttk.Frame):
    """
    A composite widget combining an entry field and a button.

    This widget is useful for cases where a user must type input
    and immediately trigger an action via a button (e.g., search
    or submit). Input is validated to a maximum of 50 characters,
    consistent with the `oma` database schema.

    Attributes:
        chars (tk.StringVar): Variable bound to the entry widget text.
        btn (ttk.Button): The button widget instance.
        entry (ttk.Entry): The entry widget instance.

    Args:
        parent (tk.Widget): The parent container widget.
        title (str): The text displayed on the button.
        command (Callable): The function executed when the button is clicked.
    """
    def __init__(self, parent, title, command):
        super().__init__(parent)

        self.chars = tk.StringVar()
        self.chars.trace_add("write", self.limit)

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        self.btn = ttk.Button(self,
                              text=title,
                              command=command,
                              style="Special.TButton")
        self.btn.grid(row=0, column=1, sticky="ew", padx=7)

        self.entry = ttk.Entry(self, textvariable=self.chars)
        self.entry.grid(row=0, column=0, sticky="ew", ipadx=5, ipady=4, padx=5)

        self.entry.bind("<FocusIn>", self.delete_input)


    # Maximum character input is 50, aligned with oma database
    def limit(self, *_):
        """
        Truncate entry input to 50 characters.

        Ensures that user input does not exceed the maximum allowed
        length of 50 characters. Extra characters are discarded.

        Args:
            *_: Unused arguments passed from `trace_add`.
        """
        inputs = self.chars.get()
        if len(inputs) > 50:
            self.chars.set(inputs[:50])

    def get_input(self):
        """
        Retrieve the current text value from the entry field.

        Returns:
            str: The text currently entered in the entry widget.
        """
        return self.chars.get()

    def delete_input(self, _=None):
        """
        Clear the entry field.

        Args:
            _ (tk.Event, optional): Event from the `<FocusIn>` binding.
                Defaults to None.
        """
        return self.entry.delete(0, tk.END)
