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
                embed.add_field(name="Captain Role:", value=ctx.guild.get_role(int(server.captain_role)).mention)
                embed.add_field(name="Bot Channel:", value=ctx.guild.get_channel(int(server.bot_channel)).mention)
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

    @settings.group(aliases=["update"])
    async def edit(self, ctx):
        """Edit a field in the settings."""

    @edit.command(aliases=["captain", "role"])
    async def captain_role(self, ctx, mention):
        """Edit the captain role."""
        with db.connector.open() as session:
            try:
                server = session.query(SettingsModel).filter(SettingsModel.server == str(ctx.guild.id)).one()
            except NoResultFound:
                await ctx.send(f"There are no settings for your server. initialize your server with `{ctx.prefix}`settings init`")
            else:
                if mentions := ctx.message.role_mentions:
                    server.captain_role = mentions[0].id
                    await ctx.send("Successfully changed `captain_role` field.")
                else:
                    await ctx.send("Invalid captain role, did you remember to mention the role?")

    @edit.command(aliases=["bot", "bot_channel"])
    async def channel(self, ctx, mention):
        """Edit the bot channel."""
        with db.connector.open() as session:
            try:
                server = session.query(SettingsModel).filter(SettingsModel.server == str(ctx.guild.id)).one()
            except NoResultFound:
                await ctx.send(f"There are no settings for your server. initialize your server with `{ctx.prefix}`settings init`")
            else:
                if mentions := ctx.message.channel_mentions:
                    server.bot_channel = mentions[0].id
                    await ctx.send("Successfully changed `bot_channel` field.")
                else:
                    await ctx.send("Invalid bot channel, did you remember to mention the channel?")

    @edit.command(aliases=["field"])
    async def battlefy_field(self, ctx, value):
        """Edit battlefy field."""
        with db.connector.open() as session:
            try:
                server = session.query(SettingsModel).filter(SettingsModel.server == str(ctx.guild.id)).one()
            except NoResultFound:
                await ctx.send(f"There are no settings for your server. initialize your server with `{ctx.prefix}`settings init`")
            else:
                server.battlefy_field = value
                await ctx.send("Successfully changed `battlefy_field`... field.")
    
    @edit.command(aliases=["tourney"])
    async def battlefy_tourney(self, ctx, value):
        """Edit battlefy tournament."""
        with db.connector.open() as session:
            try:
                server = session.query(SettingsModel).filter(SettingsModel.server == str(ctx.guild.id)).one()
            except NoResultFound:
                await ctx.send(f"There are no settings for your server. initialize your server with `{ctx.prefix}`settings init`")
            else:
                server.battlefy_tourney = value
                await ctx.send("Successfully changed `battlefy_tourney` field.")
    
    @edit.command(aliases=["auto", "auto-assign", "assign"])
    async def auto_assign_captain_role(self, ctx, value: bool):
        """Edit auto-assign captain role."""
        with db.connector.open() as session:
            try:
                server = session.query(SettingsModel).filter(SettingsModel.server == str(ctx.guild.id)).one()
            except NoResultFound:
                await ctx.send(f"There are no settings for your server. initialize your server with `{ctx.prefix}`settings init`")
            else:
                server.auto_assign_captain_role = value
                await ctx.send("Successfully changed `auto_assign_captain_role` field.")

    @settings.command()
    async def delete(self, ctx):
        """Delete the settings query from the database."""
        with db.connector.open() as session:
            try:
                server = session.query(SettingsModel).filter(SettingsModel.server == str(ctx.guild.id)).one()
            except NoResultFound:
                await ctx.send(f"There are no settings for your server. initialize your server with `{ctx.prefix}`settings init`")
            else:
                session.delete(server)
                await ctx.send("Successfully deleted settings.")

def setup(bot):
    bot.add_cog(Settings(bot))
