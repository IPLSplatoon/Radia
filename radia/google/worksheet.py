"""Contains the Worksheet class."""

import asyncio
import pandas as pd

from . import HollowSheet


class Worksheet:
    """ Represents a google sheets worksheet.

    :param gspread.models.Spreadsheet gsheet: The google sheets object
    :param str name: The name of a specific sheet
    """

    def __init__(self, gsheet, name):
        self.gsheet = gsheet
        self.name = name
        if self.gsheet:
            self.worksheet = self.gsheet.worksheet(self.name)
            self.dataframe = pd.DataFrame(self.worksheet.get_all_records())

    async def refresh(self):
        """Refresh the worksheet and records by reinitializing them."""
        if not self.gsheet:
            raise HollowSheet("Cannot refresh worksheets, google sheet is hollow.")

        loop = asyncio.get_running_loop()

        def call_gsheet():
            self.worksheet = self.gsheet.worksheet(self.name)
            self.dataframe = pd.DataFrame(self.worksheet.get_all_records())

        await loop.run_in_executor(None, call_gsheet)


class Responses(Worksheet):
    """Represents a google sheets worksheet with prefixes and responses."""

    def options(self):
        """Return the response options."""
        if not self.gsheet:
            raise HollowSheet("Cannot get response options, google sheet is hollow.")

        return self.dataframe["prefix0"]

    def get(self, prefix: str):
        """ Return the responses section with the given prefix.

        :param str prefix: One of the possible prefixes of the response
        :return tuple: (Prefix, Response, Image)
        """
        if not self.gsheet:
            raise HollowSheet("Cannot get responses, google sheet is hollow.")

        for i, row in self.dataframe.iterrows():
            if prefix in [p for p in row[:5] if p != '']:
                return row["prefix0"], row["Response"], row["ImageLink"]
