"""Utilities to help with embedding."""

from datetime import datetime

import discord


def create(**kwargs) -> discord.Embed:
    """
    Create a discord embed template
    :return: discord.embed
        discord.py embed object
    """
    embed = discord.Embed(color=0xFCFF3B, **kwargs)
    embed.set_footer(text="Radia", icon_url="https://cdn.vlee.me.uk/LowInk/RadiaMemcakeMin.png")
    embed.timestamp = datetime.utcnow()
    return embed


def list_block(items: list) -> str:
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


def emoji_bool(value: bool) -> str:
    """Return an emoji based the Boolean value to display to the user instead of text."""
    return {
        True: "\u2705",
        False: "\u274c"
    }[value]
