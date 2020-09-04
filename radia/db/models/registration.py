"""
Stores the registration table model.

tournament-teams
"""

from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base

from radia.db import connector

Base = declarative_base()


class Registration(Base):
    """Registration table model."""

    __tablename__ = "registration"
    id = Column(Integer, primary_key=True, unique=True, nullable=False)
    tournament = Column(Integer, ForeignKey("tournament.id"))
    team = Column(Integer, ForeignKey("team.id"))
    bracket = Column(Integer, default=-1)
    checked_in = Column(Boolean, default=False)
    joined_at = Column(DateTime)
    # For players manually added that can't have a user object created from them.
    manual_players = Column(ARRAY(String))
    # Holds the username and discriminator for the account stated on the registration.
    discord_rep = Column(String)


Base.metadata.create_all(connector.engine)
