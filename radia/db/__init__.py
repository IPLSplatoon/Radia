"""Initializes the database connector."""

import os
import logging

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class Connector:
    """Database connector."""

    def __init__(self):
        self.engine = create_engine(f"postgresql://postgres:{os.getenv('POSTGRES')}@db:5432")
        self.sessionmaker = sessionmaker(bind=self.engine)
        self.session = self.sessionmaker()
        logging.info("Loaded DB Connector: Session Created")


connector = Connector()
