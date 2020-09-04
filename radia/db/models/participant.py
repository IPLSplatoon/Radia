"""
Stores the participant table model.

registration-user
This holds the many to many relationship for users to registrations.
"""

from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base

from radia.db import connector

Base = declarative_base()


class Participant(Base):
    """Participant table model."""

    __tablename__ = "participant"
    id = Column(Integer, primary_key=True, unique=True, nullable=False)
    registration = Column(Integer, ForeignKey("registration.id"))
    user = Column(Integer, ForeignKey("user.id"))
    joined_at = Column(DateTime)
    # Allowed to do admin duties for a team (To be used)
    admin = Column(Boolean)


Base.metadata.create_all(connector.engine)
