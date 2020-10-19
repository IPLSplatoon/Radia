"""Stores the server model."""

from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base

from radia.db import connector

Base = declarative_base()


class Server(Base):
    """Settings table model."""

    __tablename__ = "server"
    id = Column(Integer, primary_key=True, unique=True, nullable=False)
    active_tournament = 0  # TODO: the tournament that's currently set as the active one
    tournaments = 0  # TODO: an array of tournament models
    bot_channel = Column(String, unique=True)


Base.metadata.create_all(connector.engine)
