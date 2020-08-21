"""
Initalizes the bot

This includes importing the bot, loading the cogs, setting the prefix, etc.
"""

from radia.bot import Bot
bot = Bot(command_prefix="!")

bot.run(os.getenv("TOKEN"))
