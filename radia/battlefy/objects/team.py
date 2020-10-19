"""Battlefy team object."""

import dateutil.parser

from .player import Player


class Team:
    """Function and utilities for managing teams from the battlefy api."""

    def __init__(self, battlefy, discord_field_id, fc_field_id):
        self.raw = battlefy
        self.name = self.raw["name"]
        if "logoUrl" in self.raw["persistentTeam"]:
            self.logo = self.raw["persistentTeam"]["logoUrl"]
        self.created_at = dateutil.parser.isoparse(self.raw["createdAt"])

        self.captain = Player(
            self.raw["captain"],
            self.__custom_field(discord_field_id),
            self.__custom_field(fc_field_id))
        self.players = [Player(raw) for raw in battlefy["players"]]

    def __custom_field(self, _id: str, default=None):
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
