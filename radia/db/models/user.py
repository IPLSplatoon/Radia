"""Stores the user table model."""

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, ARRAY

from radia.db import connector

Base = declarative_base()


class User(Base):
    """User table model."""

    __tablename__ = "user"
    id = Column(
        Integer, primary_key=True, unique=True, nullable=False)

    ign = Column(
        String, nullable=False)

    battlefy = Column(
        String, nullable=False)

    ign_old = Column(
        ARRAY(String))
    
    discord = Column(
        String)


Base.metadata.create_all(connector.engine)
