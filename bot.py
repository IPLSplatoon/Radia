"""
This file starts and runs the main bot functions
"""

import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import asyncio
import random

load_dotenv(".env")
TOKEN = os.environ.get("discord_Token")
# This is the list of cogs that discord.py loads in as file names without the .py extension
extensions = [
    "cogs.information",
    "cogs.Roles"
]

presence_strings = [
    "Powered by High Ink?",
    "Signup for Low Ink!",
    "The Low Ink bot."
]

bot = commands.Bot("!")


# Handles incorrect input from user
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Missing data, you got got to enter something after the command!\n"
                       "You can use `<help` for help")


# When the bot is loaded
@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print("Used in {} servers".format(len(bot.guilds)))
    print('------')
    bot.loop.create_task(presence_update())


# Updates presence data
async def presence_update():
    while True:
        await bot.change_presence(activity=discord.Game(random.choice(presence_strings)))
        await asyncio.sleep(120)

# Runs the whole show
if __name__ == "__main__":
    for extension in extensions:
        try:
            # Loads in cogs
            bot.load_extension(extension)
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            print('Failed to load extension {}\n{}'.format(extension, exc))

    bot.run("")

