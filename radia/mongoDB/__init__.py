import logging
import os
import motor.motor_asyncio

from .database import CheckinDB
from .errors import *
from .objects import *


class DBConnector:
    def __init__(self):
        if not (mongo_string := os.getenv("MONGO_STRING")):
            logging.error(".env - 'MONGO_STRING' key not found. Cannot start bot.")
            raise EnvironmentError

        if not (db_name := os.getenv("DATABASE_NAME")):
            logging.error(".env - 'DATABASE_NAME' key not found. Cannot start bot.")
            raise EnvironmentError

        self.mongo = motor.motor_asyncio.AsyncIOMotorClient(mongo_string)
        self.checkin = CheckinDB(self.mongo, db_name)


db_connector = DBConnector()
