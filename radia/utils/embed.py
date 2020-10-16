"""Utilities to help with embedding."""

from datetime import datetime

import discord


class Embed(discord.Embed):
    """A custom embed object."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, color=0xFCFF3B, **kwargs)
        self.set_footer(text="Radia", icon_url="https://cdn.vlee.me.uk/LowInk/RadiaMemcakeMin.png")
        self.timestamp = datetime.utcnow()

    @staticmethod
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

    @staticmethod
    def emoji_bool(value: bool) -> str:
        """Return an emoji based the Boolean value to display to the user instead of text."""
        return {
            True: "\u2705",
            False: "\u274c"
        }[value]
