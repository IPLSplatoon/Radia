"""Info cog."""

import discord
from discord.ext import commands, tasks

from radia import utils, google

class Info(commands.Cog):
    """All of the commands that send the user info."""

    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    def refresh(self, ctx):
        """Reload all the data on the worksheets."""
        await google.connector.rules.refresh()
        await google.connector.canned.refresh()


def setup(bot):
    bot.add_cog(Info(bot))
