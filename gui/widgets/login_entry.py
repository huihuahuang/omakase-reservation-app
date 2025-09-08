import tkinter as tk
from tkinter import ttk

# Reusable Widgets ====================================
class LoginEntry(ttk.Frame):
    """
    A reusable form field widget consisting of a label and an entry box with 
    placeholder support and input validation.

    Attributes:
        chars (tk.StringVar): Variable bound to the entry widget text.
        label (ttk.Label): The label displayed beside the entry field.
        style (ttk.Style): The style configuration for the entry widget.
        entry (ttk.Entry): The entry widget used for user input.
        lbl (str): Style name for the entry widget, derived from `lbl`.
    """
    def __init__(self, parent, lbl, lr, lc, er, ec, holder):
        """
        Initialize login entry widget.

        rgs:
        parent (tk.Widget): The parent container widget.
        lbl (str): The label text (e.g., "User Name:").
        lr (int): The grid row index for the label.
        lc (int): The grid column index for the label.
        er (int): The grid row index for the entry widget.
        ec (int): The grid column index for the entry widget.
        holder (str): The placeholder text shown in the entry field.
        """
        super().__init__(parent)

        self.chars = tk.StringVar()
        self.chars.trace_add("write", self.limit)

        self.label = ttk.Label(parent, text=lbl, background="#ffffff",
                               font=("Helvetica", 12, "bold"), foreground="#eda186")
        self.label.grid(row=lr, column=lc, padx=10, pady=10, sticky="e")

        # Style placeholder
        self.style = ttk.Style()
        self.lbl = f"{lbl.replace(' ', '')}.TEntry"
        self.style.configure(self.lbl, foreground="#A9A9A9", background="#ffffff",
                             padding=5)

        self.entry = ttk.Entry(parent, textvariable=self.chars, style=self.lbl)
        self.entry.grid(row=er, column=ec, padx=10, pady=10, sticky="w")

        # Show default placeholder for the first time
        self.entry.insert(0, holder)
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
        Get the current value of the entry field.

        Returns:
            str: The text currently entered in the entry widget.
        """
        return self.chars.get()

    def delete_input(self, _=None):
        """
        Clear the entry field and reset its style.

        Args:
            _ (tk.Event, optional): Event from the `<FocusIn>` binding.
                Defaults to None.
        """
        self.style.configure(self.lbl,foreground="black")
        return self.entry.delete(0, tk.END)
