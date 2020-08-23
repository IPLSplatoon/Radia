"""Open"""

import logging
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class Connector:
    def __init__(self):
        self.engine = create_engine(f"db://postgres:{os.getenv('POSTGRES')}@localhost:8080")
        self.sessionmaker = sessionmaker(bind=self.engine)
        self.session = self.sessionmaker()
        logging.info("Loaded DB Connector: Session Created")


connector = Connector()
