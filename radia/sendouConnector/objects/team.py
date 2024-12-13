"""Sendou team object."""
from sendou import TournamentTeam
from typing import List

from .player import Player

class Team:
    def __init__(self, sendou: TournamentTeam):
        self.raw: TournamentTeam = sendou
        self.id = sendou.id
        self.name = sendou.name
        self.logo = sendou.logo_url
        self.players: List[Player] = [Player(p) for p in sendou.members]

    @property
    def captain(self):
        return next(p for p in self.players if p.raw.captain)