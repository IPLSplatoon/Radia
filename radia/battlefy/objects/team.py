"""Battlefy team object."""

import dateutil.parser

from .player import Player


class Team:
    """Function and utilities for managing teams from the battlefy api."""

    def __init__(self, battlefy):
        self.raw = battlefy
        self.name = self.raw["name"]
        self.logo = self.raw["persistentTeam"]["logoUrl"]
        self.created_at = dateutil.parser.isoparse(self.raw["createdAt"])

        self.captain = Player(
            self.raw["captain"],
            self.__custom_field("5c71dc2bc61fc30322c85caf"),
            self.__custom_field("32stn45h234t5s_enterursw")
        )
        self.players = [Player(raw) for raw in battlefy["players"]]

    def __custom_field(self, _id: str, default=None):
        """ Return a custom field
        :param field_id: The id of the custom field.
        :return:
            The value of the custom field, or None if the custom field doesn't exist.
        """
        # field is a weird word if you look at it for too long
        for field in self.raw.get("customFields", {}):
            if field["_id"] == _id:
                return field["value"]
        return default
