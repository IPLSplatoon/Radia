"""Battlefy player object."""

import dateutil.parser
from discord.ext import commands


class Player:
    """ Function and utilities for managing players from the battlefy api.

    :param dict battlefy: The raw battlefy api data
    """

    def __init__(self, battlefy):
        self.raw = battlefy
        if self.raw:
            self.created_at = dateutil.parser.isoparse(self.raw.get("createdAt"))
        else:
            self.created_at = None


class Captain(Player):
    """ Added variables for captains specifically.

    :param dict battlefy: Same as Player
    :param str discord_field: The value of the battlefy custom field for their discord
    :param str fc_field: The value of the battlefy custom field for their fc
    """

    def __init__(self, battlefy, discord_field, fc_field):
        super().__init__(battlefy)
        self.member_converter = commands.MemberConverter()
        self.discord = discord_field
        if self.discord:
            self.discord = discord_field.replace('@', '')
            if self.discord.endswith("#0000"):
                self.discord = self.discord[:-5]
            elif self.discord.endswith("#0"):
                self.discord = self.discord[:-2]
        self.fc = fc_field

    async def get_discord(self, ctx):
        """ Return the discord member object using the discord field provided.

        :return Optional[discord.Member]:
            Returns None if the member isn't found in the server.
        """
        if not self.discord:
            return None
        try:
            return await self.member_converter.convert(ctx, self.discord)
        except commands.BadArgument:
            return None
