"""Contains the Worksheet class."""

import pandas as pd


class Worksheet:
    """Represents a google sheets worksheet."""

    def __init__(self, gsheet, name):
        self.gsheet = gsheet
        self.worksheet = self.gsheet.worksheet("Rules")
        self.records = pd.DataFrame(self.worksheet.get_all_records())
    
    def refresh(self):
        """Refresh the worksheet and records by reinitializing them."""
        self.worksheet = self.gsheet.worksheet("Rules")
        self.records = pd.DataFrame(self.worksheet.get_all_records())
