
import discord
from discord.ext import commands

from .embed import create as embedder


class HelpCommand(commands.DefaultHelpCommand):
    """Set up help command for the bot."""

