import csv
from ..dal import CreateCSV

"""
Business Logic Layer (BLL) for CSV Export.

This module provides an advanced feature that exports the `alldetails`
view to a CSV file. It wraps the DAL `CreateCSV` class, handles error
cases, and ensures user-friendly messages are returned to the GUI or
other application layers.
"""


def export_details(server, file_path):
    """
    Export reservation details to a CSV file.

    Retrieves data from the DAL `CreateCSV.export_details` method, then
    attempts to write the results to the specified file path. Handles
    common file I/O errors gracefully and returns messages suitable for
    end-user display.

    Args:
        server (dict): Connection parameters for the database.
        file_path (str): Full path to the CSV file to be created.

    Returns:
        tuple[str, bool]:
            - (success_message, True) if the file was exported successfully.
            - (error_message, False) if the export failed due to:
                * No data returned from the database.
                * Invalid file path.
                * Insufficient permissions.
                * Value parsing/conversion errors.
                * CSV writer errors.
    """
    res = CreateCSV.export_details(server)

    if len(res) == 0:
        return "Error occurred while loading data. Please contact tech support", False
    elif len(res) == 1:
        return "No reservation details data return", False
    else:
        try:
            with open(file_path, "w", newline='', encoding="utf-8") as file:
                write_data = csv.writer(file)
                write_data.writerows(res)
                return f"The details file was successfully exported to {file_path}.", True
        except FileNotFoundError:
            return ("Failed to export: Invalid path, no such directory or file. "
            "Please enter valid path.", False)
        except PermissionError:
            return ("Failed to export: program does not have the necessary "
            "permissions ", False)
        except ValueError:
            return ("Failed to export: data cannot be properly parsed or "
            "converted", False)
        except csv.Error:
            return ("Failed to export: other type failure occurred. Please contact"
                    " tech support.", False)
