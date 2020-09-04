"""
Stores the team table model.
"""

from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base

from radia.db import connector

Base = declarative_base()


class Team(Base):
    """Team table model."""

    __tablename__ = "team"
    id = Column(Integer, primary_key=True, unique=True, nullable=False)
    name = Column(String, nullable=False)
    battlefy_id = Column(String, unique=True)
    icon = Column(String)
    

Base.metadata.create_all(connector.engine)
