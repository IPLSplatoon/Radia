"""Battlefy tournament object."""

import dateutil.parser


class Tournament:
    """Function and utilities for managing tournaments from the battlefy api."""

    def __init__(self, battlefy):
        self.raw = battlefy
        self.start_time = dateutil.parser.isoparse(self.raw["startTime"])
