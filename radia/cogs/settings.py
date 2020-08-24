"""Settings cog."""

import logging

import discord
from discord.ext import commands, tasks
from sqlalchemy.orm.exc import NoResultFound

from radia import utils, db
from radia.db.models import Settings as SettingsModel


class Settings(commands.Cog):
    """Deals with Kraken Mare."""

    def __init__(self, bot):
        self.bot = bot

    @commands.group(invoke_without_command=True)
    async def settings(self, ctx):
        """Retrieve the current settings for the server."""
        with db.connector.open() as session:
            try:
                server = session.query(SettingsModel).filter(SettingsModel.server == str(ctx.guild.id)).one()
            except NoResultFound:
                server = None
        if server:
            embed = utils.embed.create(title=f"Current settings for {str(ctx.guild)}:")
            embed.add_field(name="Captain Role:", value=str(ctx.guild.get_role(server.captain_role)), inline=False)
            embed.add_field(name="Bot Channel:", value=str(ctx.guild.get_channel(server.bot_channel)), inline=False)
            embed.add_field(name="Battlefy Field:", value=server.battlefy_field, inline=False)
            embed.add_field(name="Battlefy Tourney:", value=server.battlefy_tourney, inline=False)
            embed.add_field(name="Auto-assign Captain Role:", value=server.auto_assign_captain_role, inline=False)
            await ctx.send(embed=embed)
        else:
            await ctx.send(f"There are no settings for your server, initialize your server with `{ctx.prefix}settings init`")


def setup(bot):
    bot.add_cog(Settings(bot))
