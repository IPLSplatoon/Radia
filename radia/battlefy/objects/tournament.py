"""Battlefy tournament object."""

import re
import dateutil.parser
from . import Team


class Tournament:
    """Function and utilities for managing tournaments from the battlefy api."""

    def __init__(self, battlefy, battlefy_teams):
        self.raw = battlefy
        self.start_time = dateutil.parser.isoparse(self.raw["startTime"])
        self.teams = self.create_teams(battlefy_teams)

    @classmethod
    def create_teams(cls, battlefy_teams):
        """Create teams using the battlefy_teams data."""
        return [Team(team, *cls.get_field_ids(battlefy_teams)) for team in battlefy_teams]

    @classmethod
    def get_field_ids(cls, battlefy_teams):
        """Use regex to identify and return the field ids for battlefy fields."""
        custom_fields = battlefy_teams[0]["customFields"]
        for i, field in enumerate(custom_fields):
            # Regex pattern matches valid discord usernames
            if re.match(r'.#\d{4}$', field["value"]):
                discord = custom_fields[i]["_id"]
                fc = custom_fields[(i + 1) % 2]["_id"]  # Other field must be fc
                # Return field ids
                return discord, fc
        else:
            # Try it with the next team
            return cls.get_field_ids(battlefy_teams[1:])
