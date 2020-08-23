"""Stores the settings table model."""

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Boolean

Base = declarative_base()


class Settings(Base):
    """Settings table model."""

    __tablename__ = "settings"
    server = Column(
        String(), primary_key=True, unique=True, nullable=False)

    captain_role = Column(
        String(), unique=True)

    bot_channel = Column(
        String(), unique=True)

    battlefy_field = Column(
        String())

    battlefy_tourney = Column(
        String())

    auto_assign_captain_role = Column(
        Boolean())