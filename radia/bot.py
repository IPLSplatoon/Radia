"""
Holds the custom Bot subclass
"""

import logging
import random

import asyncio
import discord
from discord.ext import commands, tasks


class Bot(commands.Bot):

    async def on_ready(self):
        logging.info(f"Logged in as: {self.user.name}")

    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"Missing data, you got got to enter something after the command!\nYou can use `{self.command_prefix}help` for help.")
        elif isinstance(error, (commands.CommandNotFound, commands.MissingRole)):
            return
        else:
            logging.error(error)

