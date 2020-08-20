"""
Utils file to handle all the environment variables in one place.
"""
import os
from dotenv import load_dotenv

from gSheetConnector import SheetConnector
from DBConnector import DBConnect
from battlefyConnector import BattlefyUtils

load_dotenv("files/.env")

class Env:

    def __init__(self):
        self.low_ink_discord_token = os.environ.get("low_ink_discord_token")
        self.google_sheet_name = os.environ.get("google_sheet_name")
        self.DB_String = os.environ.get("DB_String")
        self.system_environment = os.environ.get("system_environment")

        self.gsheet = SheetConnector("files/googleAuth.json", self.google_sheet_name)
        self.db = DBConnect(self.DB_String)
        self.battlefy = BattlefyUtils()


env = Env()