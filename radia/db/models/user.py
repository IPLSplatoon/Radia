"""Stores the user table model."""

from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base

from radia.db import connector

Base = declarative_base()


class User(Base):
    """User table model."""

    __tablename__ = "user"
    id = Column(
        Integer, primary_key=True, unique=True, nullable=False)

    ign = Column(
        String, nullable=False)

    ign_old = Column(
        ARRAY(String))

    battlefy = Column(
        String, nullable=False)

    icon = Column(
        String, nullable=True)

    discord = Column(
        String)
    
    admin = Column(
        Boolean, default=False)


Base.metadata.create_all(connector.engine)
