"""
Contains utilities for parsing Battlefy data
"""
from .battlefyConnector import BattlefyAIO
from typing import Optional


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
