"""Captain cog."""

import discord
from discord.ext import commands

from radia import utils, battlefy
from radia import utils


class Captain(commands.Cog):
    """Manages captain roles."""

    def __init__(self, bot):
        self.bot = bot

    @commands.group(invoke_without_subcommand=True)
    async def captain(self, ctx):
        """
        Show the current status of captains.
        Group of commands handling the captain roles.
        """
        """Group of commands handling the captain roles."""


def setup(bot):
    bot.add_cog(Captain(bot))
