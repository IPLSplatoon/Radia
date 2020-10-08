"""Holds the custom Bot subclass."""

import random
import logging

import asyncio
import discord
from discord.ext import commands, tasks

from radia import utils


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

    @tasks.loop(seconds=60)
    async def update_presence(self):
        await self.change_presence(activity=discord.Game(random.choice([
            "Powered by High Ink?",
            "Signup for Low Ink!",
            "The Low Ink bot.",
            "!help to get started",
            "Sprinkles!",
            "what is luti?",
            "Round 4, here we go again!",
            "The real round 4 were the friends we made along the way.",
            "What is Low Ink?",
            "Ban Kraken Mare",
            "Icon by Ozei#3125",
            "Wawa!",
            "Twitch: twitch.tv/IPLSplatoon",
            "Battlefy: battlefy.com/inkling-performance-labs",
            "Twitter: @IPLSplatoon",
            "Patreon: patreon.com/IPLSplatoon",
            "Github: github.com/IPL-Splat",
            "Facebook: facebook.com/IPLSplatoon",
            "Youtube: youtube.com/channel/UCFRVQSUskcsB5NjjIZKkWTA",
            "According to all known laws of aviation",
            "I kid you not Hoeen, he turns himself into a pickle.",
            "Go to sleep Lepto.",
            "Skye passed out again."
        ])))
