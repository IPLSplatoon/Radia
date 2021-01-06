"""Misc cog."""

import discord
from discord.ext import commands, tasks

from radia import utils, google


class Refresh(commands.Cog):
    """All the miscellaneous commands."""

    def __init__(self, bot):
        self.bot = bot
        self.refresh_loop.start()

    @staticmethod
    async def run_refresh():
        """Reload all the data on the worksheets and agenda."""
        await utils.agenda.refresh()
        await google.connector.rules.refresh()
        await google.connector.whatis.refresh()

    @commands.command()
    async def refresh(self, ctx):
        """Refetch all of the code."""
        with ctx.typing():
            await self.run_refresh()
        await ctx.send("♻ **Refreshed!**")
    
    @tasks.loop(hours=1)
    async def refresh_loop(self):
        """Loop that refreshes worksheets and agenda."""
        self.run_refresh()


def setup(bot):
    bot.add_cog(Refresh(bot))
