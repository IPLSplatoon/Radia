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
        field_ids = cls.get_field_ids(battlefy_teams)
        return [Team(team, *field_ids) for team in battlefy_teams]

    @classmethod
    def get_field_ids(cls, battlefy_teams):
        """Use regex to identify and return the field ids for battlefy fields."""
        if not battlefy_teams:
            return None, None
        custom_fields = battlefy_teams[0]["customFields"]
        for i, field in enumerate(custom_fields):
            fields = custom_fields.copy()
            # Regex pattern matches valid discord usernames
            if re.match(r'.{1,}#\d{4}$', field["value"]):
                discord_field = fields.pop(i)
                if fields:
                    # Other field must be fc
                    fc_field = fields.pop(0)
                else:
                    # There is no other field
                    fc_field = {"_id": None}

                # Return field ids
                return discord_field["_id"], fc_field["_id"]
        else:
            # Try it with the next team
            return cls.get_field_ids(battlefy_teams[1:])
