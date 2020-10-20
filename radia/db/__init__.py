"""Initializes the database connector."""

import os
import logging
from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound

from . import models


class Connector:
    """Database connector."""

    def __init__(self):
        if not (postgres := os.getenv("POSTGRES")):
            logging.error(".env - 'POSTGRES' key not found. Cannot start database.")
            raise EnvironmentError

        self.engine = create_engine(f"postgresql://postgres:{postgres}@db:5432")

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
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.commit()
            session.close()


class Utils:
    """ Here lies all of the ugly queries.
    
    The reason why this is not part of the connector class is because of circular imports.
    """

    def __init__(self, connector):
        self.connector = connector
    
    def query_server(self, id):
        with self.connector.open() as session:
            try:
                return session.query(models.Server).filter(models.Server.id == id).one()
            except NoResultFound:
                return None
    
    def add_server(self, **kwargs):
        with self.connector.open() as session:
            new = models.Server(**kwargs)
            session.add(new)
        return new
    
    def query_tournament(self):
        pass
    
    def query_active_tournament(self, server_id):
        server = self.query_server(server_id)
        # TODO: Get active tournament from server
    

connector = Connector()
utils = Utils(connector)
