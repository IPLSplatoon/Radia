"""
Utils file to handle all the environment variables in one place.
"""
import os
from dotenv import load_dotenv

import gSheetConnector
import DBConnector
import battlefyConnector

load_dotenv("files/.env")

class Env:

    def __init__(self):
        self.low_ink_discord_token = os.environ.get("low_ink_discord_token")
        self.google_sheet_name = os.environ.get("google_sheet_name")
        self.DB_String = os.environ.get("DB_String")
        self.system_environment = os.environ.get("system_environment")

        self.gsheet = gSheetConnector.SheetConnector("files/googleAuth.json", self.google_sheet_name)
        self.db = DBConnector.DBConnect(self.DB_String)
        self.battlefy = battlefyConnector.BattlefyUtils()


env = Env()