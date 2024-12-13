"""Battlefy player object."""
from typing import Optional

import dateutil.parser
from discord.ext import commands
from sendou import TeamMember


class Player:
    """ Function and utilities for managing players from the battlefy api.

    :param dict sendou: The sendou player data
    """

    def __init__(self, sendou: Optional[TeamMember]):
        self.raw: Optional[TeamMember] = sendou
        self.member_converter = commands.MemberConverter()
        if self.raw:
            self.created_at = sendou.joined_at
        else:
            self.created_at = None
    @property
    def discord(self):
        return self.raw.discord_id

    async def get_discord(self, ctx):
        """ Return the discord member object using the discord field provided.

        :return Optional[discord.Member]:
            Returns None if the member isn't found in the server.
        """
        if not self.raw.discord_id:
            return None
        try:
            return await self.member_converter.convert(ctx, self.raw.discord_id)
        except commands.BadArgument:
            return None