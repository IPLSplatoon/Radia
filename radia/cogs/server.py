"""Server cog."""
import sys

from discord.ext import commands

from radia import utils


class Server(commands.Cog, command_attrs={"hidden": True}):
    """Utility commands for handling server (guild) commands."""

    def __init__(self, bot):
        self.bot = bot

    @commands.has_role("Staff")
    @commands.command(aliases=["clean_checkin", "purge_checkin"])
    async def clear_checkin(self, ctx):
        """Clear the current check-in channel of messages."""
        if 'check-in' in ctx.channel.name:
            await ctx.channel.purge(limit=sys.maxsize)
        else:
            await ctx.channel.send(
                embed=utils.Embed(title="You'd better be careful where you're throwing that clean command around.")
            )


def setup(bot):
    bot.add_cog(Server(bot))
