"""Server cog."""

import discord
from discord.ext import commands

from radia import utils, db


class Server(commands.Cog):
    """Interacts with the server database model."""

    def __init__(self, bot):
        self.bot = bot

    @commands.group(invoke_without_command=True, aliases=["config"])
    async def server(self, ctx):
        """Get the configuration for the server."""
        if not (server := db.utils.query_server(ctx.guild.id)):
            return await ctx.send(f"There is no configuration for your server, initialize your server with `{ctx.prefix}server init`")

        embed = utils.Embed(title=f"Current configuration for {str(ctx.guild)}:")
        embed.add_field(name="Active Tournament:", value=server.active_tournament, inline=False)
        embed.add_field(name="All Tournaments:", value=server.tournaments, inline=False)
        await ctx.send(embed=embed)

    @server.command(aliases=["initialize", "new"])
    async def init(self, ctx):
        """Initialize the server configuration."""
        if db.utils.query_server(ctx.guild.id):
            return await ctx.send(f"Your server has already been initialized, you can view them with `{ctx.prefix}server`.")

        db.utils.add_server({
            "id": ctx.guild.id
        })
        await ctx.send(f"> ✅ **Server Configuration Initialized!**")


def setup(bot):
    bot.add_cog(Server(bot))
