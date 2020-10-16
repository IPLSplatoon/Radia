"""Battlefy player object."""

import dateutil.parser


class Player:
    """Function and utilities for managing players from the battlefy api."""

    def __init__(self, battlefy, discord=None, sw=None):
        self.raw = battlefy
        self.slug = self.raw.get("userSlug")  # More persistent than their "persistent" player ids
        self.ign = self.raw.get("inGameName")
        self.created_at = dateutil.parser.isoparse(self.raw.get("createdAt"))
        self.discord = discord
        self.sw = sw
