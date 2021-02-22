"""Contains the Calendar class."""

import os
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

    def next_tourney(self):
        """Return the upcoming tournament, or None if there isn't one."""
        if self.agenda:
            self.tourney_at(0)

    def prev_tourney(self):
        """Return the previous tournament, or None if there isn't one."""
        prev_event = None
        # Loop over entire timeline
        for event in self.calendar.timeline:
            # Filter events that aren't valid tournaments
            if not event.has_end() or not event.description:
                continue
            # Set prev_event if the event is in the past
            elif event.begin < arrow.now():
                prev_event = event
            # This is next, meaning the prev_event variable stores the previous event
            else:
                return Event(prev_event, **load_yaml(prev_event.description))

    def tourney_at(self, index: int):
        """Return the tournament at the given index."""
        if index == -1:
            return self.prev_tourney()
        try:
            return self.agenda[index]
        except IndexError:
            return None

    async def refresh(self, *args, **kwargs):
        """Refresh the calendar and tournament events by reinitializing them."""
        self.calendar = Calendar(await self.query(*args, **kwargs))
        self.agenda = [
            # Loads the parsed yaml of event desc as __init__ parameters
            Event(event, **load_yaml(event.description))
            # Repeats this for every event that's a valid tournament
            for event in self.filter_cal()
            if event.description
        ]

    async def query(self, url=os.getenv("ICAL")):
        """ Make a get request to the ical link url.

        :param str url: The url to the ical file, defaults to the environment provided one.
        """
        async with self.session.get(url) as response:
            if response.status == 200:
                return await response.text()
            logging.error("Unable to fetch google calendar file, Status Code: %s", response.status)

    def filter_cal(self):
        for event in self.calendar.timeline:
            if event.has_end() and event.end > arrow.now():
                yield event


class Event:
    """Represents a tournament event."""

    def __init__(self, event, battlefy, role="406171863698505739", **kwargs):
        self.event = event
        # Event description params
        self.battlefy = battlefy
        self.role = role

    def get_role(self, ctx):
        return ctx.guild.get_role(int(self.role))
