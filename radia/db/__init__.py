"""Initializes the database connector."""

import os
import logging
from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class Connector:
    """Database connector."""

    def __init__(self):
        if not (postgres := os.getenv("POSTGRES")):
            logging.error(".env - 'POSTGRES' key not found. Cannot start database.")
            raise EnvironmentError

        self.engine = create_engine(f"postgresql://postgres:{os.getenv('POSTGRES')}@db:5432")

        self.sessionmaker = sessionmaker(self.engine)
        logging.debug("Loaded db.connector")

    @contextmanager
    def open(self):
        """
        Open a new session using a with statement.
        
        Usage: `with db.connector.open() as session:`
        """
        try:
            session = self.sessionmaker()
            yield session
        except:
            session.rollback()
            raise
        finally:
            session.close()


connector = Connector()
