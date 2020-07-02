import datetime
import dateutil.parser
from .player import Player


class Team:
    """
    Defines a team object
    """
    def __init__(self, ID: int = -1, battlefyID: str = "None", teamName: str = "None", teamIcon: str = "None",
                 joinDate: str = "1970-01-01T00:00:00.000Z", captainDiscord: str = "Unknown",
                 captainFC: str = "Unknown", players: list = None, manualPlayers: list = None,
                 allowCheckin: bool = False, checkin: bool = False, bracket: int = -1):
        self.ID = ID
        self.battlefyID = battlefyID
        self.teamName = teamName
        self.teamIcon = teamIcon
        self.joinDate = joinDate
        self.captainDiscord = captainDiscord
        self.captainFC = captainFC
        self.players = players
        self.manualPlayers = manualPlayers
        self.allowCheckin = allowCheckin
        self.checkin = checkin
        self.bracket = bracket

    def setID(self, ID: int):
        self.ID = ID

    def setBattlefyID(self, battlefyID: str):
        self.battlefyID = battlefyID

    def setTeamName(self, teamName: str):
        self.teamName = teamName

    def setTeamIcon(self, teamIcon: str):
        self.teamIcon = teamIcon

    def setJoinDate(self, joinDate: str):
        self.joinDate = dateutil.parser.isoparse(joinDate)

    def setCaptainDiscord(self, captainDiscord: str):
        self.captainDiscord = captainDiscord

    def setCaptainFC(self, captainFC: str):
        self.captainFC = captainFC

    def addPlayers(self, player: Player):
        self.players.append(player)

    def addManualPlayer(self, manualPlayer: str):
        self.manualPlayers.append(manualPlayer)
