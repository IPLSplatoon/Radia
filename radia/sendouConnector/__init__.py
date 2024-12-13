"""Initializes the Sendou connector."""

import logging
import sendou
from aiohttp_client_cache.backends import RedisBackend
from os import environ

from .objects import Tournament

class Connector:
    def __init__(self):
        self.__api_key = environ.get("SENDOU_API_KEY")
        if not self.__api_key:
            logging.error("No Sendou API Key found.")
            raise ValueError("No Sendou API Key found.")
        if redis_uri := environ.get("REDIS_URI"):
            self.__redis_uri = redis_uri
        else:
            self.__redis_uri = "redis://redis:6379/"
        self.client = sendou.Client(self.__api_key)
        self.client.cache = RedisBackend(cache_name="sendou", redis_uri=self.__redis_uri, expire_after=300)
        logging.debug("Loaded sendou.connector")

    async def get_tournament(self, tournament_id: str):
        """ Get tournament object from sendou api.

        :param tournament_id: The sendou tournament ID
        :rtype: Tournament
        """
        tournament_data = await self.client.get_tournament(tournament_id)
        teams = await tournament_data.get_teams()
        return Tournament(tournament_data, teams)

    async def get_teams(self, tournament_id: str):
        """ Helper function that simply returns the ".teams" attribute of a tournament.

        :return: List[Team]
        """
        tourney = await self.get_tournament(tournament_id)
        return tourney.teams