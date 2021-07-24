import logging
import os
import motor.motor_asyncio

from .database import CheckinDB
from .errors import *
from .objects import *


class DBConnector:
    """MongoDB Connector"""
    def __init__(self):
        if not (mongo_string := os.getenv("MONGOURI")):
            logging.error(".env - 'MONGOURI' key not found. Cannot start bot.")
            raise EnvironmentError

        if not (db_name := os.getenv("DATABASENAME")):
            logging.error(".env - 'DATABASENAME' key not found. Cannot start bot.")
            raise EnvironmentError

        self.mongo = motor.motor_asyncio.AsyncIOMotorClient(mongo_string)
        self.checkin = CheckinDB(self.mongo, db_name)


db_connector = DBConnector()
