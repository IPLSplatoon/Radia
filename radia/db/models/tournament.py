"""Stores the tournament table model."""

from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base

from radia.db import connector

Base = declarative_base()


class Tournament(Base):
    """Tournament table model."""

    __tablename__ = "tournament"
    id = Column(Integer, primary_key=True, unique=True, nullable=False)
    battlefy_id = Column(String, unique=True)
    date = Column(DateTime)
    guild = Column(String)
    role = Column(String)


Base.metadata.create_all(connector.engine)
