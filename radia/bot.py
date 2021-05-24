"""Holds the custom Bot subclass."""

import logging

import discord
from discord.ext import commands, tasks

from radia import utils


class Bot(commands.Bot):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.help_command = utils.HelpCommand()

    async def on_ready(self):
        logging.info("Logged in as: %s", self.user.name)

    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(embed=utils.Embed(
                title="Error: **Missing Required Argument**",
                description=f"You can use `{ctx.prefix}help` for help."))
        elif isinstance(error, discord.errors.Forbidden):
            await ctx.send(embed=utils.Embed(
                title="Error: **Missing Permissions**",
                description=f"This is probably a mistake, please notify staff about this."))
        elif isinstance(error, (commands.CommandNotFound, commands.MissingRole)):
            return
        else:
            logging.error(error)
            raise error
