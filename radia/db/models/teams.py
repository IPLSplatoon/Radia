"""
This hold the SQLalchemy ORM designs
for Low Ink Team's Database
"""
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import sqlalchemy
from radia.db import connector

Base = declarative_base()


class Tournament(Base):
    __tablename__ = "Tournament"
    tournament_ID = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, unique=True, nullable=False)
    battlefy_ID = sqlalchemy.Column(sqlalchemy.String(24), unique=True)
    date = sqlalchemy.Column(sqlalchemy.DateTime)
    guild_ID = sqlalchemy.Column(sqlalchemy.String(20))
    role_ID = sqlalchemy.Column(sqlalchemy.String(20))
    teams = relationship("TournamentTeam")


class Team(Base):
    __tablename__ = "Team"
    team_ID = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, unique=True, nullable=False)
    battlefy_ID = sqlalchemy.Column(sqlalchemy.String(24), unique=True)
    team_name = sqlalchemy.Column(sqlalchemy.String(64), nullable=False)
    icon_URL = sqlalchemy.Column(sqlalchemy.String(255), nullable=True)
    tournaments = relationship("TournamentTeam")


class TournamentTeam(Base):
    __tablename__ = "TournamentTeam"
    ID = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, unique=True, nullable=False)
    tournament_ID = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("Tournament.tournamentID"))
    team_ID = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("Team.teamID"))
    join_date = sqlalchemy.Column(sqlalchemy.DateTime)
    captain_discord = sqlalchemy.Column(sqlalchemy.String(37), nullable=False)
    captain_FC = sqlalchemy.Column(sqlalchemy.String(40), nullable=False)
    bracket = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    allow_checkin = sqlalchemy.Column(sqlalchemy.Boolean, default=False)
    check_in = sqlalchemy.Column(sqlalchemy.Boolean, default=False)
    manual_players = sqlalchemy.Column(sqlalchemy.ARRAY(sqlalchemy.String(32)))
    players = relationship("TeamPlayer")
    tournament = relationship("Tournament")
    team = relationship("Team")


class Player(Base):
    __tablename__ = "Player"
    player_ID = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, unique=True, nullable=False)
    in_game_name = sqlalchemy.Column(sqlalchemy.String(30), nullable=False)
    battlefy_userslug = sqlalchemy.Column(sqlalchemy.String(50), nullable=False, unique=True)
    previous_IGN = sqlalchemy.Column(sqlalchemy.ARRAY(sqlalchemy.String(30)))
    discord_ID = sqlalchemy.Column(sqlalchemy.String(20))
    teams = relationship("TeamPlayer")


class TeamPlayer(Base):
    __tablename__ = "TeamPlayer"
    ID = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, unique=True, nullable=False)
    tournament_team_ID = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("TournamentTeam.ID"))
    player_ID = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("Player.playerID"))
    join_date = sqlalchemy.Column(sqlalchemy.DateTime)
    admin = sqlalchemy.Column(sqlalchemy.Boolean, default=False)
    Player = relationship("Player")
    TournamentTeam = relationship("TournamentTeam")

Base.metadata.create_all(connector.engine)
