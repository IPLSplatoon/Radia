"""
Contains utilities for parsing Battlefy data
"""
from .battlefyConnector import BattlefyAIO
from typing import Optional
from .teamDesign import Player, Team
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
            for players in teams["players"]:
                tempPlayer = Player()
                tempPlayer.load(field_check("persistentPlayerID", players), field_check("userSlug", players),
                                field_check("inGameName", players), dateutil.parser.isoparse(players["createdAt"]))
                teamRoaster.append(tempPlayer)
            captain = Player()
            if "captain" in teams:
                captain.load(teams["captain"]["persistentPlayerID"], teams["captain"]["userSlug"],
                             teams["captain"]["inGameName"],
                             dateutil.parser.isoparse(teams["captain"]["createdAt"]))
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

            team = Team(teams["name"], teams["persistentTeamID"], discord, FCCode, captain, teamRoaster, logo)
            teamList.append(team)
        return teamList
