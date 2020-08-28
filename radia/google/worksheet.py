"""Contains the Worksheet class."""

import asyncio
import pandas as pd


class Worksheet:
    """Represents a google sheets worksheet."""

    def __init__(self, gsheet, name):
        self.gsheet = gsheet
        self.name = name
        self.worksheet = self.gsheet.worksheet(self.name)
        self.dataframe = pd.DataFrame(self.worksheet.get_all_records())

    async def refresh(self):
        """Refresh the worksheet and records by reinitializing them."""
        
        async def task():
            self.worksheet = self.gsheet.worksheet(self.name)
            self.dataframe = pd.DataFrame(self.worksheet.get_all_records())

        await asyncio.create_task(task())


class Responses(Worksheet):
    """Represents a google sheets worksheet with prefixes and responses."""

    def options(self):
        """Return the response options."""
        return self.dataframe["prefix0"]
    
    def get(self, prefix):
        """Return the responses section with the given prefix."""
        for i, row in self.dataframe.iterrows():
            if prefix in [p for p in row[:5] if p != '']:
                return row["prefix0"], row["Response"], row["ImageLink"]
