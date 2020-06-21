"""
This cog configures, loads and runs Reaction based role requests
"""
import utils
from discord.ext import commands, tasks
import discord
import gSheetConnector
import datetime
import os
from dotenv import load_dotenv
import emoji
import re

load_dotenv("files/.env")
GOOGLE_SHEET_NAME = os.environ.get("google_sheet_name")


def emoji_check(emojiChar: str):
    """
    Check if the emoji provided is custom, or unicode
    :param emojiChar: str
    :return: int, str
        int: 0 = Invalid, 1 = Unicode, 2 = Custom
        str: ID, Unicode Codestring, None
    """
    # Check if it's an Unicode emoji
    if emojiChar in emoji.UNICODE_EMOJI:
        return 1, 'U+{}'.format(ord(emojiChar))  # Last section gets the unicode code
    # This is a regular expression to check the format for a Discord custom Emoji
    customEmojiExpression = re.compile("<:([A-Z]+[a-z]+[0-9]+):([0-9]+)>")
    # Check if the emoji is a custom emoji
    if customEmojiExpression.match(emojiChar):
        emojiChar = emojiChar[2:][:-1]  # Remove first 2 and last char from string
        emojiID = emojiChar.split(":")  # Split string with the : in the middle
        return 2, emojiID[1]  # Return
    return 0, None  # Return 0 and None is provided string isn't an emoji


class RoleReact(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.sheets = gSheetConnector.SheetConnector("files/googleAuth.json", GOOGLE_SHEET_NAME)

    @commands.command(name='test', help="testing shit")
    async def testing(self, ctx, emote):
        print(emote)
        emojiType, ID = emoji_check(emote)
        print("Type {} | ID:{}".format(emojiType, ID))




def setup(bot):
    bot.add_cog(RoleReact(bot))
