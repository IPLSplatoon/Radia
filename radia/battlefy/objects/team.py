"""Battlefy team object."""

from enum import Enum

import discord
from discord.ext import commands
import dateutil.parser

from .player import Player, Captain


class Team:
    """ Function and utilities for managing teams from the battlefy api.

    :param dict battlefy: The raw battlefy data
    :param str discord_field_id: The battlefy field id of the discord field
    :param str fc_field_id: The battlefy field id of the friend-code field
    """

    class Bracket(Enum):
        ALPHA = "a"
        BETA = "b"
        GAMMA = "g"

        def role(self, ctx):
            return discord.utils.get(ctx.guild.roles, name=f"LI {self.name.capitalize()}")

        @classmethod
        def find(cls, string):
            for option in cls:
                if string.lower().startswith(option.value):
                    return option
            else:
                return cls(string)

    def __init__(self, battlefy, discord_field_id, fc_field_id):
        self.raw = battlefy
        self.name = self.raw["name"]
        self.logo = self.raw["persistentTeam"].get("logoUrl", None)
        self.created_at = dateutil.parser.isoparse(self.raw["createdAt"])

        self.captain = Captain(
            battlefy=self.raw.get("captain", None),
            discord_field=self.__get_custom_field_by_id(discord_field_id),
            fc_field=self.__get_custom_field_by_id(fc_field_id))
        self.players = [Player(battlefy=raw) for raw in battlefy["players"]]

    def __get_custom_field_by_id(self, _id: str, default=None):
        """ Return a custom field

        :param _id: The id of the custom field.
        :return:
            The value of the custom field, or default/None if the custom field doesn't exist.
        """
        # Field is a weird word if you look at it for too long
        for field in self.raw.get("customFields", {}):
            if field["_id"] == _id:
                return field["value"]
        return default

    async def assign_bracket(self, ctx, bracket):
        """Assign a bracket to a team by captain roles."""
        captain_discord = await self.captain.get_discord(ctx)
        if captain_discord:
            bracket_role = self.Bracket.find(bracket).role(ctx)
            await captain_discord.add_roles(bracket_role)
        else:
            raise commands.BadArgument

    async def get_bracket(self, ctx):
        """Get the bracket of a team based on captain roles."""
        captain_discord = await self.captain.get_discord(ctx)
        if captain_discord:
            for bracket in self.Bracket:
                bracket_role = self.Bracket.find(bracket).role(ctx)
                if bracket_role in captain_discord.roles:
                    return bracket
