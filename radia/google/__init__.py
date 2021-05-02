"""Initializes the Google Sheets connector."""

import os
import logging

import gspread

from .exc import HollowSheet
from .worksheet import Worksheet, Responses


class Connector:
    """Google connector."""

    def __init__(self):
        try:
            self.service = gspread.service_account(filename='google.json')
        except FileNotFoundError:
            self.gsheet = self.service.open_by_key(os.getenv("GSHEET"))
            logging.error("google.json - file not found, google sheet will be hollow.")
        else:
            self.gsheet = None

        self.rules = Responses(self.gsheet, "Rules")
        self.whatis = Responses(self.gsheet, "Canned Responses")
        logging.debug("Loaded google.connector")


connector = Connector()
