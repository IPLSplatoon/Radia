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
