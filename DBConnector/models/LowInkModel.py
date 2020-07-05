from sqlalchemy.ext.declarative import declarative_base
import sqlalchemy.dialects.postgresql as postgres  # For postgres specific data types
from sqlalchemy.orm import relationship
import sqlalchemy
from sqlalchemy import create_engine

Base = declarative_base()


class Tournament(Base):
    __tablename__ = "Tournament"
    tournamentID = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, unique=True, nullable=False)
    battlefyID = sqlalchemy.Column(sqlalchemy.String(24), unique=True)
    date = sqlalchemy.Column(sqlalchemy.DateTime)
    guildID = sqlalchemy.Column(sqlalchemy.String(20))
    roleID = sqlalchemy.Column(sqlalchemy.String(20))
    teams = relationship("TournamentTeam")


class Team(Base):
    __tablename__ = "Team"
    teamID = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, unique=True, nullable=False)
    battlefyID = sqlalchemy.Column(sqlalchemy.String(24), unique=True)
    teamName = sqlalchemy.Column(sqlalchemy.String(64), nullable=False)
    iconURL = sqlalchemy.Column(sqlalchemy.String(255), nullable=True)
    tournaments = relationship("TournamentTeam")


class TournamentTeam(Base):
    __tablename__ = "TournamentTeam"
    ID = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, unique=True, nullable=False)
    tournamentID = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("Tournament.tournamentID"))
    teamID = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("Team.teamID"))
    joinDate = sqlalchemy.Column(sqlalchemy.DateTime)
    captainDiscord = sqlalchemy.Column(sqlalchemy.String(37), nullable=False)
    captainFC = sqlalchemy.Column(sqlalchemy.String(20), nullable=False)
    bracket = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    allowCheckin = sqlalchemy.Column(sqlalchemy.Boolean, default=False)
    checkin = sqlalchemy.Column(sqlalchemy.Boolean, default=False)
    manualPlayers = sqlalchemy.Column(sqlalchemy.ARRAY(sqlalchemy.String(32)))
    players = relationship("TeamPlayer")


class Player(Base):
    __tablename__ = "Player"
    playerID = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, unique=True, nullable=False)
    battlefyID = sqlalchemy.Column(sqlalchemy.String(24), unique=True)
    inGameName = sqlalchemy.Column(sqlalchemy.String(15), nullable=False)
    battlefyUserslug = sqlalchemy.Column(sqlalchemy.String(30), nullable=False)
    previousIGN = sqlalchemy.Column(sqlalchemy.ARRAY(sqlalchemy.String(15)))
    discordID = sqlalchemy.Column(sqlalchemy.String(20))
    teams = relationship("TeamPlayer")


class TeamPlayer(Base):
    __tablename__ = "TeamPlayer"
    ID = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, unique=True, nullable=False)
    tournamentTeamID = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("TournamentTeam.ID"))
    playerID = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("Player.playerID"))
    joinDate = sqlalchemy.Column(sqlalchemy.DateTime)
    admin = sqlalchemy.Column(sqlalchemy.Boolean, default=False)


def buildTables(DBConnectStr: str):
    engine = create_engine(DBConnectStr)
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
