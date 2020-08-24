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
                embed = utils.embed.create(title=f"Current settings for {str(ctx.guild)}:")
                embed.add_field(name="Captain Role:", value=ctx.guild.get_role(int(server.captain_role)).mention, inline=False)
                embed.add_field(name="Bot Channel:", value=ctx.guild.get_channel(int(server.bot_channel)).mention, inline=False)
                embed.add_field(name="Battlefy Field:", value=server.battlefy_field, inline=False)
                embed.add_field(name="Battlefy Tourney:", value=server.battlefy_tourney, inline=False)
                embed.add_field(name="Auto-assign Captain Role:", value=utils.embed.emojibool(server.auto_assign_captain_role), inline=False)
                await ctx.send(embed=embed)
            except NoResultFound:
                await ctx.send(f"There are no settings for your server, initialize your server with `{ctx.prefix}settings init`")

    @settings.command(aliases=["initialize", "new"])
    async def init(self, ctx, captain_role, bot_channel, battlefy_field, battlefy_tourney, auto_assign_captain_role: bool = True):
        """
        Initialize settings for the server.
        
        Example: `!settings init @Captian #bot-commands 5c7..caf 5f2..094 [False]`
        """
        with db.connector.open() as session:
            try:
                server = session.query(SettingsModel).filter(SettingsModel.server == str(ctx.guild.id)).one()
            except NoResultFound:
                server = None
            if not server:
                new = SettingsModel(
                    server=str(ctx.guild.id),
                    captain_role=str(ctx.message.role_mentions[0].id),
                    bot_channel=str(ctx.message.channel_mentions[0].id),
                    battlefy_field=battlefy_field,
                    battlefy_tourney=battlefy_tourney,
                    auto_assign_captain_role=auto_assign_captain_role)
                session.add(new)
                await ctx.send(f"Initialized settings.")
            else:
                await ctx.send(f"Settings have already been initialized for your server, you can view them with `{ctx.prefix}settings`.")


def setup(bot):
    bot.add_cog(Settings(bot))
