"""
This file starts and runs the main bot functions
"""
import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import asyncio
import random
import datetime
import gSheetConnector
import utils

load_dotenv("files/.env")
TOKEN = os.environ.get("low_ink_discord_token")

# This is the list of cogs that discord.py loads in as file names without the .py extension
extensions = [
    "cogs.information",
    "cogs.Roles",
    "cogs.other"
]

presence_strings = [
    "Powered by High Ink?",
    "Signup for Low Ink!",
    "The Low Ink bot.",
    "!help to get started",
    "Sprinkles!",
    "what is luti?",
    "Round 3, here we go again!",
    "What is Low Ink?",
    "Ban Kraken Mare",
    "Icon by Ozei#3125",
    "Wawa!"
]

bot = commands.Bot("!")


# Handles incorrect input from user
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Missing data, you got got to enter something after the command!\n"
                       "You can use `<help` for help")
    elif isinstance(error, commands.CommandNotFound):
        return
    else:
        utils.errorCollector.collect_error(error, "on_command_error")


# When the bot is loaded
@bot.event
async def on_ready():
    print('Logged in as:')
    print("Name: {}".format(bot.user.name))
    print("ID: {}".format(bot.user.id))
    print("Booted up at: {}".format(datetime.datetime.utcnow()))
    print("Used in {} servers".format(len(bot.guilds)))
    print('------')
    bot.loop.create_task(presence_update())


# Member join event
@bot.event
async def on_member_join(member: discord.member):
    await assignNewMemberRole(member)


# Give default role to member
async def assignNewMemberRole(member: discord.member):
    settings = gSheetConnector.SheetConnector("files/googleAuth.json", "Low Ink Bot DataSet") \
        .get_settings("Settings")
    if str(member.guild.id) in settings:
        defaultRoleId = settings[str(member.guild.id)]["DefaultRoleID"]
        defaultRole = member.guild.get_role(defaultRoleId)
        if defaultRole is not None:
            await member.add_roles(defaultRole)
    else:
        return


# Updates presence data
async def presence_update():
    while True:
        await bot.change_presence(activity=discord.Game(random.choice(presence_strings)))
        await asyncio.sleep(60)

# Runs the whole show
if __name__ == "__main__":
    for extension in extensions:
        try:
            # Loads in cogs
            bot.load_extension(extension)
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            print('Failed to load extension {}\n{}'.format(extension, exc))

    bot.run(TOKEN)

