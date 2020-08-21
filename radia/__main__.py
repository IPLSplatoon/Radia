"""
Initalizes the bot

This includes importing the bot, loading the cogs, setting the prefix, etc.
"""

import os
import logging

from radia import cogs
from radia.bot import Bot

# Create Bot
bot = Bot(command_prefix="!")

# Load Cogs
for cog in cogs.names:
    try:
        bot.load_extension("radia.cogs." + cog)
        logging.info("Loaded cog: %s", cog)
    except Exception as e:
        logging.warn("Failed to load cog: %s", cog)
        logging.error(type(e).__name__, e)

# Run Bot
bot.run(os.getenv("TOKEN"))
