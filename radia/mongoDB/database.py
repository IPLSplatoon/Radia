import motor.motor_asyncio
import pymongo
from radia import battlefy
from typing import List, Optional
from .objects import MongoTeam


class CheckinDB:
    """Handled all the data for the checkin Database"""
    def __init__(self, connection: motor.motor_asyncio, db_name: str):
        """
        Init
        :param connection: MongoDB connection
        :param db_name: Database Name
        """
        self._connection = connection[db_name]
        self.db = self._connection.teams

    async def load_teams(self, tournament_teams: List[battlefy.objects.Team], battlefy_id: str):
        """
        Load teams from a Battlefy Tournament
        :param tournament_teams: teams from battlefy
        :param battlefy_id: Battlefy ID
        :return: None
        """
        write_list = []  # Stores teams before writing to DB
        for team in tournament_teams:
            instance = {
                "$set": {
                    "battlefyTournamentId": battlefy_id,
                    "name": team.name,
                    "logoUrl": team.logo,
                    "captainDiscord": team.captain.discord,
                }
            }
            write_list.append(pymongo.UpdateOne({"_id": team.id}, instance, upsert=True))
        if len(write_list) > 0:
            await self.db.bulk_write(write_list)

    async def get_team(self, team_name: str, battlefy_id: str) -> Optional[MongoTeam]:
        """
        Get battlefy Team for tournament
        :param team_name: Team's Name
        :param battlefy_id: Tournament ID
        :return: Optional[MongoTeam]
        """
        team = await self.db.find_one({"name": team_name, "battlefyTournamentId": battlefy_id})
        if team:
            return MongoTeam(team, self.db)

    async def get_discord_team(self, discord: list, battlefy_id: str) -> Optional[MongoTeam]:
        """
        Get team via discord username#tag or ID
        :param discord: list of search prams
        :param battlefy_id: Tournament ID
        :return: Optional[MongoTeam]
        """
        for x in discord:
            # looks if captain discord wit the value
            if team := await self.db.find_one({"captainDiscord": x, "battlefyTournamentId": battlefy_id}):
                return MongoTeam(team, self.db)
            elif team := await self.db.find_one(  # looks for it additional discord would have the value
                    {"additionalDiscord": {"$in": [x]}, "battlefyTournamentId": battlefy_id}):
                return MongoTeam(team, self.db)

    async def get_bracket_teams(self, battlefy_id: str, bracket: int = None) -> List[MongoTeam]:
        """
        Bracket
        :param battlefy_id: Tournament ID
        :param bracket: bracket to get teams for
        :return: List[MongoTeam]
        """
        if not bracket:
            # If no bracket is specified we look for all brackets in a tournament that are greater than 0
            db_teams = self.db.find({"battlefyTournamentId": battlefy_id, "bracket": {"$gt": 0}})
        else:
            db_teams = self.db.find({"battlefyTournamentId": battlefy_id, "bracket": bracket})
        mongo_team_objects = []
        # for team in await db_teams.to_list(length=100):
        async for team in db_teams:
            mongo_team_objects.append(MongoTeam(team, self.db))
        return mongo_team_objects
