"""Initializes the Battlefy connector."""

import os
import logging

import aiohttp


class Connector:
    """Battlefy connector."""

    def __init__(self):
        self.session = aiohttp.ClientSession()
        logging.debug("Loaded battlefy.connector")

    async def get(self, url):
        """Get a response at url."""
        async with self.session.get(url) as response:
            if response.status != 200:
                return None
            return await response.json()

    async def get_tournament(self, tournament: str):
        """Get tournament from battlefy."""
        request = await self.get(f"https://dtmwra1jsgyb0.cloudfront.net/tournaments/{tournament}")


connector = Connector()
