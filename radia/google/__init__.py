"""Initializes the Google Sheets connector."""

import json
import logging


class Connector:
    """Database connector."""

    def __init__(self):
        try:
            with open(".googleenv.json") as infile:
                creds = json.load(infile)

        except FileNotFoundError:
            logging.error(".googleenv.json - file not found.")
            raise EnvironmentError

        else:
            pass  # Authorization

        logging.debug("Loaded google.connector")


connector = Connector()
