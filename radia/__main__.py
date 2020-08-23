"""
Initalizes the bot

This includes importing the bot, loading the cogs, setting the prefix, etc.
"""

import os
import logging

from radia import cogs
from radia import utils
from radia.bot import Bot

# Create Bot
bot = Bot(command_prefix="!")

# Load Cogs
for cog in cogs.names:
    try:
        bot.load_extension("radia.cogs." + cog)
        logging.debug("Loaded cogs.%s", cog)
    except Exception as e:
        logging.warn("Failed to load cogs.%s", cog)
        logging.error(type(e).__name__, e)

# Run Bot
if not (token := os.getenv("TOKEN")):
    logging.error(".env - 'TOKEN' key not found. Cannot start bot.")
    raise EnvironmentError

bot.run(token)
