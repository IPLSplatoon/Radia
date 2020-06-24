"""
Hold object design for teams design
"""
import datetime


class Player:
    def __init__(self, playerID: str, battlefyUsername: str, inGameName: str, createdAt: datetime):
        self.persistentPlayerID = playerID  # persistentPlayerID
        self.battlefyUsername = battlefyUsername  # userSlug
        self.inGameName = inGameName  # inGameName
        self.createdAt = createdAt  # createdAt


class Team:
    def __init__(self, teamName: str, teamID: str, captainDiscord: str, captainFC: str,
                 captain: Player, players: list, teamIconURL: str):
        self.teamName = teamName  # name
        self.id = teamID  # persistentTeamID
        self.captainDiscord = captainDiscord  # 5c71dc2bc61fc30322c85caf
        self.captainFC = captainFC  # 5c71dc2bc61fc30322c85caf
        self.captain = captain  # Player: captain
        self.players = players  # Player: players
        self.checkIN = None
        self.teamIconURL = teamIconURL  # persistentTeam:logoUrl

    def add_checkin_time(self, checkinTime: datetime):
        self.checkIN = checkinTime

    def remove_checkin_time(self) -> bool:
        if self.checkIN is not None:
            self.checkIN = None
            return True
        return False
