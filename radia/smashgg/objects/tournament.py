from .event import Event
from .connect import Connect


class Tournament:
    def __init__(self, tournament: dict, gql_connector: Connect):
        self._raw = tournament
        self.name: str = self._raw.get("name", None)
        self.id: int = self._raw.get("id", None)
        self.events = []
        self.session = gql_connector
        for e in self._raw.get("events", []):
            self.events.append(Event(e, self.session))
