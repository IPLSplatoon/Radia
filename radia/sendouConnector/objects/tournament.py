import sendou
from typing import List

from .team import Team


class Tournament:
    """Sendou tournament object."""

    def __init__(self, sendou_data: sendou.Tournament, teams: List[sendou.TournamentTeam]):
        self.raw: sendou.Tournament = sendou_data
        self.id = sendou_data.id
        self.name = sendou_data.name
        self.registered_count = sendou_data.teams.registered_count
        self.teams: List[Team] = [Team(t) for t in teams]

