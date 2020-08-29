"""Stores the participant table model."""

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import *

from radia.db import connector

Base = declarative_base()


class Participant(Base):
    """Participant table model."""

    __tablename__ = "participant"
    id = Column(
        Integer, primary_key=True, unique=True, nullable=False)

    tournament = Column(
        Integer, ForeignKey("tournament.id"))
    
    player = relationship("player")
   
    name = Column(
        String, nullable=False)

    joined_at = sqlalchemy.Column(
        DateTime)


Base.metadata.create_all(connector.engine)
