"""Contains Bag class."""

import random


class Bag:
    """ Implemented algorithm to create balanced random picking.
    :param set items: A list of items to be placed in the bag.
    :param int div:
        The fraction of items that are the maximum number of recents at a time.
        A higher number means more balanced but less randomized.
    """

    def __init__(self, items: set, div=3):
        self.items = items
        self.recents = []
        self.max = int(len(items)/div)

    def __iter__(self):
        return iter(self.items - set(self.recents))

    def pick(self, item):
        """Add an item to the recents list."""
        self.recents.append(item)

    def prune(self):
        """Remove the oldest elements from the recents out of the maximum."""
        if len(self.recents) >= self.max:
            self.recents = self.recents[-self.max:]

    def empty(self):
        """Remove all elements from the recents."""
        self.recents = []
