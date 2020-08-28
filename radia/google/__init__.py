"""Initializes the Google Sheets connector."""

import os
import json
import logging

import gspread

from .worksheet import Worksheet


class Connector:
    """Google connector."""

    def __init__(self):
        try:
            self.service = gspread.service_account(filename='google.json')
        except FileNotFoundError:
            logging.error("google.json - file not found.")
            raise EnvironmentError
        else:

            self.gsheet = self.service.open_by_key(os.getenv("GSHEET"))
            self.rules = self.get_worksheet("Rules")
            self.canned = self.get_worksheet("Canned Responses")

        logging.debug("Loaded google.connector")

    def get_worksheet(self, name):
        """Return a worksheet with the linked google sheet and passed name."""
        return Worksheet(self.gsheet, name)

connector = Connector()
