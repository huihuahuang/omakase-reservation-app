from tkinter import ttk
class Button:
    """
    A styled wrapper for ttk.Button with grid placement.

    Attributes:
        btn (ttk.Button): The underlying ttk.Button widget instance.

    Args:
        parent (tk.Widget): The parent container where the button is placed.
        title (str): The text displayed on the button.
        command (Callable): The function to be executed when the button is clicked.
        r (int): The grid row index for placing the button.
        c (int): The grid column index for placing the button.
    """
    def __init__(self, parent, title, command, r, c):
        self.btn = ttk.Button(parent,
                              text=title,
                              command=command,
                              style="Special.TButton")
        style = ttk.Style()
        style.configure("Special.TButton", padding=5,
                        font=("Helvetica", 11))
        self.btn.grid(row=r, column=c, padx=5, pady=5, sticky="nsew")