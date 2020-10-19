"""Stores the tournament table model."""

from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base

from radia.db import connector

Base = declarative_base()


class Tournament(Base):
    """Tournament table model."""

    __tablename__ = "tournament"
    id = Column(String, primary_key=True, unique=True, nullable=False)
    server = 0  # TODO: link to server model that holds this tournament
    captain_role_id = Column(Integer, unique=True)


Base.metadata.create_all(connector.engine)
