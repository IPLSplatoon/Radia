from .player import Player
from typing import  Optional


class Team:
    def __init__(self, smashgg: dict):
        self._raw: dict = smashgg
        self._raw_team: dict = self._raw.get('team', {})
        self.name: str = self._raw.get('name', '')
        self.players = []
        for p in self._raw_team.get("members", []):
            if p:
                self.players.append(Player(p))

    def __str__(self):
        player = ""
        for p in self.players:
            player = f"{player}, {p.name}"
        return f"{self.name} : {player}"

    @property
    def captain(self) -> Optional[Player]:
        """
        Returns captain of team
        :return: Captain of team
        """
        for p in self.players:
            if p.captain:
                return p
        return None
