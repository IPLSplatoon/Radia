"""
This is the team object used to display data on embeds
and is used to store data coming in from battlefy
"""
import datetime
import dateutil.parser
from .player import PlayerObject


class TeamObject:
    """
    Defines a team object
    """
    def __init__(self, ID: int = -1, battlefyID: str = "None", teamName: str = "None", teamIcon: str = "None",
                 joinDate: datetime = dateutil.parser.isoparse("1970-01-01T00:00:00.000Z"),
                 captainDiscord: str = "Unknown", captainFC: str = "Unknown",
                 players: list = [],  manualPlayers: list = None, allowCheckin: bool = False,
                 checkin: bool = False, bracket: int = -1):
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

    def setJoinDate(self, joinDate: str = None, joinDateTime: datetime = None):
        if joinDate:
            self.joinDate = dateutil.parser.isoparse(joinDate)
        elif joinDateTime:
            self.joinDate = joinDateTime
        else:
            raise ValueError("Value not provided")

    def setCaptainDiscord(self, captainDiscord: str):
        self.captainDiscord = captainDiscord

    def setCaptainFC(self, captainFC: str):
        self.captainFC = captainFC

    def addPlayers(self, player: PlayerObject):
        self.players.append(player)

    def addManualPlayer(self, manualPlayer: str):
        self.manualPlayers.append(manualPlayer)

    def setAllowCheckin(self, allowCheckin: bool):
        self.allowCheckin = allowCheckin

    def setCheckin(self, checkin: bool):
        self.checkin = checkin

    def setBracket(self, bracket: int):
        self.battlefyID = bracket

    def gotPlayer(self, playerBattlefyID: str) -> bool:
        if not self.players:
            return False
        for player in self.players:
            if player.battlefyPlayerID == playerBattlefyID:
                return True
        return False

    def __str__(self):
        players = ""
        for player in self.players:
            players += "{}\n------------\n".format(str(player))
        return "ID: {}\n" \
               "BattlefyID: {}\n" \
               "teamName: {}\n" \
               "teamIcon: {}\n" \
               "joinDate: {}\n" \
               "Captain Discord: {}\n" \
               "Captain FC: {}\n" \
               "Allow Checkin: {}\n" \
               "Checkin: {}\n" \
               "Bracket: {}\n" \
               "Manual Players: {}\n" \
               "Players:\n==================\n" \
               "{}".format(self.ID, self.battlefyID, self.teamName, self.teamIcon,
                           self.joinDate.strftime("%d/%m/%Y, %H:%M:%S"), self.captainDiscord,
                           self.captainFC, self.allowCheckin, self.checkin, self.bracket,
                           self.manualPlayers, players)
