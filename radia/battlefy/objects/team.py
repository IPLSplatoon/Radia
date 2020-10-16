"""Battlefy team object."""

import dateutil.parser
import re

from .player import Player


class Team:
    """Function and utilities for managing teams from the battlefy api."""

    def __init__(self, battlefy):
        self.raw = battlefy
        self.name = self.raw["name"]
        if "logoUrl" in self.raw["persistentTeam"]:
            self.logo = self.raw["persistentTeam"]["logoUrl"]
        self.created_at = dateutil.parser.isoparse(self.raw["createdAt"])

        self.captain = Player(
            self.raw["captain"],
            self.__get_discord_username(),
            self.__get_friend_code()
        )
        self.players = [Player(raw) for raw in battlefy["players"]]

    def __custom_field(self, _id: str, default=None):
        """ Return a custom field
        :param _id: The id of the custom field.
        :return:
            The value of the custom field, or default/None if the custom field doesn't exist.
        """
        # field is a weird word if you look at it for too long
        for field in self.raw.get("customFields", {}):
            if field["_id"] == _id:
                return field["value"]
        return default

    def __get_discord_username(self, default=None):
        """
        Return the Discord username from the customFields if exists.
        :return:
            The discord username, or default/None if the custom field doesn't exist.
        """
        for field in self.raw.get("customFields", {}):
            if re.match(r"\(?.*#[0-9]{4}\)?", field["_id"]):
                return field["value"]
        return default

    def __get_friend_code(self, default=None):
        """
        Return the Switch friend code from the customFields if exists.
        :return:
            The discord Switch friend code, or default/None if the custom field doesn't exist.
        """
        for field in self.raw.get("customFields", {}):
            if re.match(r"\(?\d{4}(-| )\d{4}(-| )\d{4}\)?", field["_id"]):
                return field["value"]
        return default
