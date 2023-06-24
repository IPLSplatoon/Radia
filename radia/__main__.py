"""
Initializes the bot

This includes importing the bot, loading the cogs, setting the prefix, etc.
"""

import os
import logging
import asyncio

from discord import Intents

from radia import cogs, battlefy, google
from radia.bot import Bot

# Create Bot
intents = Intents.default()
intents.members = True
debug = os.getenv("DEBUG", "false").lower() != "false"
bot = Bot(command_prefix="!" if not debug else "^", intents=intents)


# Get token from env variables
if not (token := os.getenv("TOKEN")):
    logging.error(".env - 'TOKEN' key not found. Cannot start bot.")
    raise EnvironmentError


async def run_bot() -> None:
    """
    Loads in cogs and starts bot
    :return: None
    """
    async with bot:
        for cog in cogs.names:
            try:
                await bot.load_extension("radia.cogs." + cog)
                logging.debug("Loaded cogs.%s", cog)
            except Exception as e:
                logging.warning("Failed to load cogs.%s", cog)
                logging.error(type(e).__name__, e)
        await bot.start(token)

asyncio.run(run_bot())
