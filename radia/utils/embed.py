"""Utilities to help with embedding."""

from datetime import datetime
import discord

def create(**kwargs) -> discord.Embed:
    """
    Create a discord embed template
    :return: discord.embed
        discord.py embed object
    """
    embed = discord.Embed(color=0xe0fe3a, **kwargs)
    embed.set_author(
        name="Radia",
        url="https://battlefy.com/low-ink",
        icon_url="https://cdn.vlee.me.uk/LowInk/LowInkIcon.png")
    embed.set_footer(text="The Low Ink Bot", icon_url="https://cdn.vlee.me.uk/LowInk/LowInk.png")
    embed.timestamp = datetime.utcnow()
    return embed

def listblock(items: list) -> str:
    """
    Return a formatted list
    :param list items:
        List of items to format
    :return str:
        The list codeblock
    """
    return "\n".join([
        "```",
        *[f"- {item}" for item in items],
        "```"
    ])
