"""Stores the registration table model."""

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import *

from radia.db import connector

Base = declarative_base()


class Registration(Base):
    """Registration table model."""

    __tablename__ = "registration"
    id = Column(
        Integer, primary_key=True, unique=True, nullable=False)

    tournament = Column(
        Integer, ForeignKey("tournament.id"))
    
    bracket = Column(
        Integer, default=0)

    team = Column(
        Integer, ForeignKey("team.id"))

    name = Column(
        String, nullable=False)

    joined_at = sqlalchemy.Column(
        DateTime)

    checked_in = Column(
        Boolean, default=False)

Base.metadata.create_all(connector.engine)
