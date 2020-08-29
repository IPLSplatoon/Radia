"""Stores the tournament table model."""

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Boolean

from radia.db import connector

Base = declarative_base()


class Team(Base):
    """Team table model."""

    __tablename__ = "team"
    id = Column(
        sqlalchemy.Integer, primary_key=True, unique=True, nullable=False)

    battlefy = Column(
        String, unique=True)
    
    name = Column(
        String, nullable=False)
    
    icon = Column(
        String, nullable=True)


Base.metadata.create_all(connector.engine)
