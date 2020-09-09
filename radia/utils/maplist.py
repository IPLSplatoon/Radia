"""Contains class for dealing with maplist generation."""


class Maplist:
    """Contains maplist generator."""

    class NotEnoughMaps(Exception):
        """There aren't enough maps in the map pool."""

    def __init__(self, pool, brackets):
        self.pool = pool
        self.brackets = brackets
