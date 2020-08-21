"""
This hold the SQLalchemy ORM designs
for Settings
"""

import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine

Base = declarative_base()


class Settings(Base):
    __tablename__ = "Settings"
    ServerID = sqlalchemy.Column(sqlalchemy.String(), primary_key=True, unique=True, nullable=False)
    CaptainRoleID = sqlalchemy.Column(sqlalchemy.String(), unique=True)
    BotChannelID = sqlalchemy.Column(sqlalchemy.String(), unique=True)
    BattlefyFieldID = sqlalchemy.Column(sqlalchemy.String())
    BattlefyTournamentID = sqlalchemy.Column(sqlalchemy.String())
    AutoAssignCaptainRole = sqlalchemy.Column(sqlalchemy.Boolean())


def buildTables(DBConnectStr: str):
    engine = create_engine(DBConnectStr)
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
