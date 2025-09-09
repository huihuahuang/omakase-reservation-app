"""
Entry point for the Omakase reservation application.
"""
from .gui import Application
# Main function to create and run application instance
def main():
    """
    Initialize and start the Omakase servation application.

    Creates an `Application` instance with the configured window title and 
    size, then runs the Tkinter main loop.
    """
    app = Application("Huang's Omakase Application -- Created By Huihua Huang",
                      "1000x750")
    app.mainloop()

if __name__ == "__main__":
    main()