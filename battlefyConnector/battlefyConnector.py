"""
Deals with obtaining data from Battlefy API
"""
import aiohttp
from typing import Optional

# Timeout for requests in seconds
timeout = aiohttp.ClientTimeout(total=20)


class BattlefyAIO:
    async def __requestJson(self, url: str) -> Optional[dict]:
        """
        Private Function
        Requests a data url
        :param url: str
            The URL to request from
        :return: dict
            The dict reply from the website.
        """
        async with aiohttp.ClientSession() as session:
            async with session.get(url=url) as response:
                if response.status != 200:
                    return None
                response = await response.json()
                if response is None:
                    return response
                return response

    async def getOrganiser(self, organiserID: str) -> Optional[dict]:
        """
        Get data on an organiser
        :param organiserID: str
            Organiser's Battlefy ID
        :return: dict
            Dict of the returned data
        """
        URL = "https://dtmwra1jsgyb0.cloudfront.net/organizations/{}".format(organiserID)
        return await self.__requestJson(URL)

    async def getTournament(self, tournamentID: str) -> Optional[dict]:
        """
        Get data on a tournament
        :param tournamentID: str
            Tournament ID
        :return: dict
            Dict of the returned data
        """
        URL = "https://dtmwra1jsgyb0.cloudfront.net/tournaments/{}".format(tournamentID)
        return await self.__requestJson(URL)

    async def getTournamentTeams(self, tournamentID: str) -> Optional[dict]:
        """
        Get the teams taking part in a tournament
        :param tournamentID: str
            Tournament ID
        :return: dict
            Dict of the returned data
        """
        URL = "https://dtmwra1jsgyb0.cloudfront.net/tournaments/{}/teams".format(tournamentID)
        return await self.__requestJson(URL)