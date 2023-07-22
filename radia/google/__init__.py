"""Initializes the Google Sheets connector."""

import os
import logging

import gspread

from .exc import HollowSheet
from .worksheet import Worksheet, Responses


class Connector:
    """Google connector."""

    def __init__(self):
        debug = os.getenv("DEBUG", "false").lower() != "false"
        try:
            # In debug mode allows for stating a file path to google.json to cover come linking issue
            if not ((google_file := os.getenv("GOOGLE_FILE_LOCATION")) and debug):
                google_file = 'google.json'
            self.service = gspread.service_account(filename=google_file)
        except FileNotFoundError:
            logging.error("google.json - file not found, google sheet will be hollow.")
            logging.error("is the correct working dir been set?")
            self.gsheet = None
        else:
            self.gsheet = self.service.open_by_key(os.getenv("GSHEET"))

        self.rules = Responses(self.gsheet, "Rules")
        self.whatis = Responses(self.gsheet, "Canned Responses")
        logging.debug("Loaded google.connector")


connector = Connector()
