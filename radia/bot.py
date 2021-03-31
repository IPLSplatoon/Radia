"""Holds the custom Bot subclass."""

import logging

import discord
from discord.ext import commands, tasks

from radia import utils
from radia.presence_messages import get_presence_message


class Bot(commands.Bot):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.help_command = utils.HelpCommand()

    async def on_ready(self):
        logging.info("Logged in as: %s", self.user.name)
        self.update_presence.start()

    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(embed=utils.Embed(
                title="Error: **Missing Required Argument**",
                description=f"You can use `{ctx.prefix}help` for help."))
        elif isinstance(error, (commands.CommandNotFound, commands.MissingRole)):
            return
        else:
            logging.error(error)
            raise error

    @tasks.loop(minutes=1)
    async def update_presence(self):
        """Loop to update the bot presence by selecting one of the strings at random."""
        await self.change_presence(activity=discord.Game(get_presence_message()))
