"""Initializes the Battlefy connector."""

import logging
import aiohttp

from .objects import Player, Team, Tournament


class Connector:
    """Battlefy connector."""

    def __init__(self):
        self.session = aiohttp.ClientSession()
        logging.debug("Loaded battlefy.connector")

    async def query(self, url):
        """Get a response at url."""
        async with self.session.get("https://dtmwra1jsgyb0.cloudfront.net/" + url) as response:
            if response.status != 200:
                logging.error("Unable to query battlefy api, Status Code: %s", response.status)
                return
            return await response.json()

    async def get_tournament(self, tournament):
        """ Get tournament object from battlefy api.
        :param tournament str: Battlefy Tournament ID
        :return Tournament: A Tournament object
        """
        battlefy_tournament = await self.query(f"tournaments/{tournament}")
        return Tournament(battlefy_tournament)

    async def get_teams(self, tournament):
        """ Get a list of team objects from battlefy api.
        :param tournament str: Battlefy Tournament ID
        :return list[Team]: A list of Team objects
        """
        battlefy_teams = await self.query(f"tournaments/{tournament}/teams")
        return [Team(team) for team in battlefy_teams]


connector = Connector()
