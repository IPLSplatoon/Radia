"""Utilities to help with embedding."""

from datetime import datetime
from typing import List

import discord


class Embed(discord.Embed):
    """A custom embed object."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, color=0xe2fe3d, **kwargs)
        self.set_footer(text="Radia", icon_url="https://cdn.vlee.me.uk/LowInk/RadiaMemcakeMin.png")
        self.timestamp = datetime.utcnow()

    @staticmethod
    def list(items: list, *, ordered=False) -> str:
        """ Return a formatted list

        :param list items: List of items to format
        :param bool ordered: Whether the list should be ordered or not
        :return str:
            The list codeblock
        """
        def format(i, item):
            """Format a list item."""
            if ordered:
                return f"> `{i}.` {item}"
            else:
                return f"> `-` {item}"

        return "\n".join([
            *[format(i, item) for i, item in enumerate(items)],
        ])

    @staticmethod
    def file_list(items: list, *, ordered=False) -> str:
        """ Return a formatted list

        :param list items: List of items to format
        :param bool ordered: Whether the list should be ordered or not
        :return str:
            The list codeblock
        """

        def format(i, item):
            """Format a list item."""
            if ordered:
                return f"- {i}. {item}"
            else:
                return f"- {item}"

        return "\n".join([
            *[format(i, item) for i, item in enumerate(items)],
        ])

    @staticmethod
    def emoji_bool(value: bool) -> str:
        """Return an emoji based the Boolean value to display to the user instead of boring text."""
        return {
            True: "\u2705",
            False: "\u274c"
        }[value]
