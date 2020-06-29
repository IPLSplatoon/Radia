"""
Hold object design for teams design
"""
import datetime
import dateutil.parser


class Player:
    """
    Define a player object
    """
    def __init__(self):
        """
        constructor
        """
        self.persistentPlayerID = "None"
        self.battlefyUsername = "None"
        self.inGameName = "None"
        self.createdAt = dateutil.parser.isoparse("1970-01-01T00:00:00.000Z")

    def load(self, playerID: str, battlefyUsername: str, inGameName: str, createdAt: datetime):
        self.persistentPlayerID = playerID  # persistentPlayerID
        self.battlefyUsername = battlefyUsername  # userSlug
        self.inGameName = inGameName  # inGameName
        self.createdAt = createdAt  # createdAt

    def json_return(self) -> dict:
        """
        Get a dict return from this object's attributes
        :return: dict
            Dict with object's attributes
        """
        return {
            "persistentPlayerID": self.persistentPlayerID,
            "battlefyUsername": self.battlefyUsername,
            "inGameName": self.inGameName,
            "createdAt": self.createdAt.strftime("%d/%m/%Y %H:%M:%S")
        }

    def load_from_dict(self, data: dict):
        """
        Loads fields from dict
        :param data: dict
            The data to load in
        :return: None
        """
        self.persistentPlayerID = data["persistentPlayerID"]
        self.battlefyUsername = data["battlefyUsername"]
        self.inGameName = data["inGameName"]
        self.createdAt = datetime.datetime.strptime(data["createdAt"], "%d/%m/%Y %H:%M:%S")


class Team:
    """
    Defines a team object
    """
    def __init__(self, teamName: str, teamID: str, captainDiscord: str, captainFC: str, captain: Player,
                 players: list, teamIconURL: str, checkin: bool = False, allowCheckin: bool = False):
        """
        Constructor with fields
        """
        self.teamName = teamName  # name
        self.teamID = teamID  # persistentTeamID
        self.captainDiscord = captainDiscord  # 5c71dc2bc61fc30322c85caf
        self.captainFC = captainFC  # 5c71dc2bc61fc30322c85caf
        self.checkin = checkin
        self.allowCheckin = allowCheckin
        self.captain = captain  # Player: captain
        self.players = players  # Player: players
        self.teamIconURL = teamIconURL  # persistentTeam:logoUrl

    def player_list(self) -> list:
        """
        Get a list of player dicts
        :return: list
            List of player dict
        """
        playerList = []
        for player in self.players:
            playerList.append(player.json_return())
        return playerList

