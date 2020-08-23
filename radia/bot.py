"""
Holds the custom Bot subclass
"""

import random
import logging

import asyncio
import discord
from discord.ext import commands, tasks


class Bot(commands.Bot):

    async def on_ready(self):
        logging.info(f"Logged in as: {self.user.name}")
        self.update_presence.start()

    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"Missing data, you got got to enter something after the command!\nYou can use `{self.command_prefix}help` for help.")
        elif isinstance(error, (commands.CommandNotFound, commands.MissingRole)):
            return
        else:
            logging.error(error)

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
            "What is Low Ink?",
            "Ban Kraken Mare",
            "Icon by Ozei#3125",
            "Wawa!",
            "Stream @ Twitch.tv/inkfarer",
            "According to all known laws of aviation",
            "I kid you not Hoeen, he turns himself into a pickle.",
            "Go to sleep Lepto.",
            "Skye passed out again."
        ])))
