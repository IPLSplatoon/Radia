import datetime
import dateutil.parser


class Player:
    def __init__(self, ID: int = -1, battlefyPlayerID: str = "None", battlefyUserslug: str = "None",
                 inGameName: str = "None", previousIGN: list = None, createdAt: str = "1970-01-01T00:00:00.000Z",
                 admin: bool = False):
        if previousIGN is None:
            previousIGN = []
        self.ID = ID
        self.battlefyPlayerID = battlefyPlayerID
        self.battlefyUserslug = battlefyUserslug
        self.inGameName = inGameName
        self.previousIGN = previousIGN
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

    def __str__(self):
        return "ID: {}\nPlayerID: {}\nUserSlug: {}\nIGN: {}\nPreviousIGN: {}\nCreated @: {}\nAdmin{}" \
               "".format(self.ID, self.battlefyPlayerID, self.battlefyUserslug, self.inGameName,
                         self.previousIGN, self.createdAt, self.admin)
