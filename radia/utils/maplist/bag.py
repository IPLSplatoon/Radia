"""Contains Bag class."""

import random


class Bag:
    """ Implemented algorithm to create balanced random picking.
    :param list items: A list of items to be placed in the bag.
    :param int maximum:
        The maximum number of recents in the bag at a time.
        A higher number means more balanced but less randomized.
    """
    def __init__(self, items: list, maximum: int):
        self.items = items
        self.max = maximum
        self.recents = []
    
    def pick(self, prune=True):
        pick = random.choice(self.items - self.recents)
        self.recents.append(pick)
        if prune:
            self.prune()
        return pick

    def prune(self):
        """Remove the oldest elements from the bag out of the maximum."""
        if len(self.recents) >= self.max:
            self.recents = self.recents[-self.max:]
