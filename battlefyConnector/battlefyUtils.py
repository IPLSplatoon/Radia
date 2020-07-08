"""
Contains utilities for parsing Battlefy data
"""
from .battlefyConnector import BattlefyAIO
from .models.tournament import Tournament
from typing import Optional
from DBConnector import TeamObject, PlayerObject
import dateutil.parser


def field_check(key, data) -> str:
    if key in data:
        return data[key]
    else:
        return "Unknown"


class BattlefyUtils:
    def __init__(self):
        self.battlefy = BattlefyAIO()

    async def get_custom_field(self, tournamentID: str, fieldID: str) -> Optional[list]:
        """
        Get a list of entries from a Battlefy custom field
        :param tournamentID: str
            The TournamentID
        :param fieldID: str
            The fieldID of the field you want to get
        :return: list
            list of all the entries (None if invalid tournamentID or fieldID)
        """
        request = await self.battlefy.getTournamentTeams(tournamentID)
        if not request:  # Check if the return has data
            return None
        returnList = []
        for teams in request:
            if "customFields" in teams:
                customFields = teams["customFields"]
                for fields in customFields:
                    if fields["_id"] == fieldID:
                        returnList.append(fields["value"])
                        pass
        return returnList

    async def get_captains_team(self, tournamentID: str, fieldID: str) -> Optional[dict]:
        """
        Get a dict with the team of the username
        :param tournamentID: str
            The TournamentID
        :param fieldID: str
            The fieldID of the field you want to get
        :return: dict
            dict with key:captain-username and value:team-name  (None if invalid tournamentID or fieldID)
        """
        request = await self.battlefy.getTournamentTeams(tournamentID)
        if not request:  # Check if the return has data
            return None
        returnDict = {}
        for teams in request:
            if "customFields" in teams:
                customFields = teams["customFields"]
                for fields in customFields:
                    if fields["_id"] == fieldID:
                        returnDict[fields["value"]] = teams["name"]
                        pass
        return returnDict

    async def get_tournament(self, tournamentID: str) -> Optional[Tournament]:
        """
        Get a tournament's details
        :param tournamentID: str
            Battlefy ID of the tournament
        :return: Tournament
        Tournament object with the data
        """
        request = await self.battlefy.getTournament(tournamentID)
        if not request:  # Check if the return has data
            return None
        return Tournament(startTime=dateutil.parser.isoparse(request["startTime"]))

    async def get_list_of_teams(self, tournamentID: str, DiscordFieldID: str, FCFieldID: str) -> Optional[list]:
        """
        Get a list of teams fully registered on battlefy
        :param tournamentID: str
            The TournamentID
        :param DiscordFieldID: str
            The DiscordFieldID of the battlefy signup
        :param FCFieldID:
            The fieldID that contain's the friend code
        :return: list
            List of Team objects
        """
        request = await self.battlefy.getTournamentTeams(tournamentID)
        if not request:  # Check if the return has data
            return None
        teamList = []
        for teams in request:
            teamRoaster = []
            manualPlayers = []
            for players in teams["players"]:
                # This is how we tell players with account from players that are added by staff
                if "userID" not in players:
                    manualPlayers.append(field_check("inGameName", players)[:30])
                else:
                    tempPlayer = PlayerObject(battlefyPlayerID=field_check("persistentPlayerID", players),
                                              battlefyUserslug=field_check("userSlug", players)[:50],
                                              inGameName=field_check("inGameName", players)[:30],
                                              createdAt=players["createdAt"])
                    teamRoaster.append(tempPlayer)
            createdAt = dateutil.parser.isoparse(teams["createdAt"])
            customFields = teams["customFields"]
            persistentTeam = teams["persistentTeam"]
            discord = "Unknown"
            FCCode = "Unknown"
            for fields in customFields:
                if fields["_id"] == DiscordFieldID:
                    discord = fields["value"]
                elif fields["_id"] == FCFieldID:
                    FCCode = fields["value"]

            logo = persistentTeam["logoUrl"]
            if not logo:
                logo = "Unknown"

            team = TeamObject(battlefyID=teams["persistentTeamID"], teamName=teams["name"], teamIcon=logo[:255],
                              joinDate=createdAt, captainDiscord=discord[:37], captainFC=FCCode[:40],
                              players=teamRoaster, manualPlayers=manualPlayers)
            teamList.append(team)
        return teamList
