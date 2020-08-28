"""Initializes the Google Sheets connector."""

import json
import logging

import gspread


class Connector:
    """Google connector."""

    def __init__(self):
        try:
            gc = gspread.service_account(filename='google.json')
        except FileNotFoundError:
            logging.error("google.json - file not found.")
            raise EnvironmentError

        logging.debug("Loaded google.connector")


connector = Connector()
