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
            "!help to get started",
            # Signup!
            "Signup for Low Ink!",
            "Signup for Swim or Sink!",
            "Signup for Testing Grounds!",
            "Signup for Unnamed Tournament!",
            # funny
            "Powered by High Ink!",
            "Testing Grounds is buying LUTI.",
            "Get your coffee grounds 45% off this weekend at Testing Grounds."
            "According to all known laws of aviation",
            # Round 4
            "Round 4, here we go again!",
            "The real round 4 were the friends we made along the way.",
            # uwu stuff
            "Sprinkles!",
            "Wawa!",
            # Socials
            "Twitter: @IPLSplatoon",
            "Twitch: twitch.tv/IPLSplatoon",
            "Battlefy: battlefy.com/inkling-performance-labs",
            "Patreon: patreon.com/IPLSplatoon",
            "Github: github.com/IPL-Splat",
            "Youtube: youtube.com/channel/UCFRVQSUskcsB5NjjIZKkWTA",
            "Facebook: facebook.com/IPLSplatoon",
            # People-specific
            "Icon by Ozei!",
            "Ban Kraken Mare",
            "I kid you not Hoeen, he turns himself into a pickle.",
            "Go to sleep Lepto.",
            "Skye passed out again."
        ])))
