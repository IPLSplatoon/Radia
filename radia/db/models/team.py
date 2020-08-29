"""Stores the team table model."""

from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base

from radia.db import connector

Base = declarative_base()


class Team(Base):
    """Team table model."""

    __tablename__ = "team"
    id = Column(
        Integer, primary_key=True, unique=True, nullable=False)

    name = Column(
        String, nullable=False)
    
    battlefy = Column(
        String, unique=True)
    
    captain = Column(
        Integer, ForeignKey("user.id"), nullable=False)

    members = relationship("user")

    icon = Column(
        String)
    

Base.metadata.create_all(connector.engine)
