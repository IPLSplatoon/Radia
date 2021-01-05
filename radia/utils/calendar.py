"""Contains the Calendar class."""

import logging
import aiohttp
import arrow
from ics import Calendar
from yaml import safe_load as load_yaml


class Agenda:
    """Represents a ical file."""

    def __init__(self):
        self.session = aiohttp.ClientSession()
        self.calendar = None
        self.agenda = []

    def __iter__(self):
        return iter(self.agenda)
    
    async def next_tourney(self):
        """Return the upcoming tournament, or None if there isn't one."""
        if self.agenda:
            return self.agenda[0]

    async def refresh(self, *args, **kwargs):
        """Refresh the calendar and tournament events by reinitializing them."""
        self.calendar = Calendar(self.query(*args, **kwargs))
        self.agenda = [
            Event(**load_yaml(event.description))
            for event in self.filter_cal()
            if event.description
        ]

    async def query(self, url="fi2493cmq5k867spkca48be37o%40group.calendar.google.com/private-81bf777d88e7c877b4aa735a45f676da/basic.ics"):
        """Make a get request to the ical link url."""
        async with self.session.get("https://calendar.google.com/calendar/ical/" + url) as response:
            if response.status == 200:
                return await response.text()
            logging.error("Unable to fetch google calendar file, Status Code: %s", response.status)
    
    def filter_cal(self):
        for event in self.calendar.timeline:
            if event.has_end() and event.end > arrow.now():
                yield event

class Event:
    """Represents a tournament event."""

    def __init__(self, battlefy, role="406171863698505739", *args):
        self.battlefy = battlefy
        self.role = role
