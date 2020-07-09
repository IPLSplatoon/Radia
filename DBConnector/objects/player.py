"""
This is the player object used to display data on embeds
and is used to store data coming in from battlefy
"""
import datetime
import dateutil.parser


class PlayerObject:
    def __init__(self, ID: int = -1, battlefyPlayerID: str = "None", battlefyUserslug: str = "None",
                 inGameName: str = "None", previousIGN: list = [], discordID: str = None,
                 createdAt: str = "1970-01-01T00:00:00.000Z", admin: bool = False):
        if previousIGN is None:
            previousIGN = []
        self.ID = ID
        self.battlefyPlayerID = battlefyPlayerID
        self.battlefyUserslug = battlefyUserslug
        self.inGameName = inGameName
        self.previousIGN = previousIGN
        self.discordID = discordID
        self.createdAt = dateutil.parser.isoparse(createdAt)
        self.admin = admin

    def setID(self, ID: int):
        self.ID = ID

    def setBattlefyPlayerID(self, battlefyPlayerID: str):
        self.battlefyPlayerID = battlefyPlayerID

    def setBattlefyUserslug(self, battlefyUserslug: str):
        self.battlefyUserslug = battlefyUserslug

    def setInGameName(self, inGameName: str):
        self.inGameName = inGameName

    def setPreviousIGN(self, previousIGN: list):
        self.previousIGN = previousIGN

    def addPreviousIGN(self, previousIGN: str):
        self.previousIGN.append(previousIGN)

    def setJoinDate(self, createdAtDate: str = None, createdAtDatetime: datetime = None):
        if createdAtDate:
            self.createdAt = dateutil.parser.isoparse(createdAtDate)
        elif createdAtDatetime:
            self.createdAt = createdAtDatetime
        else:
            raise ValueError("Value not provided")

    def setAdmin(self, admin: bool):
        self.admin = admin

    def setDiscordID(self, discordID):
        self.discordID = discordID

    def __str__(self):
        if self.previousIGN:
            return "UserSlug: {}\nIGN: {}\nPreviousIGN: {}\nCreated @: {}\nAdmin: {}" \
                   "".format(self.battlefyUserslug, self.inGameName, self.previousIGN,
                             self.createdAt.strftime("%d/%m/%Y, %H:%M"), self.admin)
        else:
            return "UserSlug: {}\nIGN: {}\nCreated @: {}\nAdmin: {}" \
                   "".format(self.battlefyUserslug, self.inGameName,
                             self.createdAt.strftime("%d/%m/%Y, %H:%M"), self.admin)
