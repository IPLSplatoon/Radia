"""Battlefy player object."""

import dateutil.parser
from discord.ext import commands


class Player:
    """Function and utilities for managing players from the battlefy api."""

    def __init__(self, battlefy):
        self.raw = battlefy
        self.created_at = dateutil.parser.isoparse(self.raw.get("createdAt"))


class Captain(Player):
    """Added variables for captains specifically."""

    def __init__(self, battlefy, discord_field, fc_field):
        super().__init__(battlefy)
        self.member_converter = commands.MemberConverter()
        self.discord = discord_field
        self.fc = fc_field

    async def get_discord(self, ctx):
        """ Return the discord member object using the discord field provided.
        Can return None if the discord member object is not found in the server.
        """
        if not self.discord:
            return None
        try:
            return await self.member_converter.convert(ctx, self.discord)
        except commands.BadArgument:
            return None
