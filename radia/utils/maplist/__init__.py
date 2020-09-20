"""Contains Maplist class."""

from .pools import Pools


class Maplist:
    """ Deals with generating a maplist.
    :param dict pools:
        A Pools object, see ./pools.py
    :param list brackets: 
        List of bracket dictionaries, see ./brackets.py
    """

    def __init__(self, pools: Pools, brackets: list):
        self.pools = pools
        self.brackets = brackets
        self.maplist = self.create_empty()
        self.gen_maplist()

    def create_empty(self):
        """Create an empty maplist object.
        :returns: The empty structure of the object looks like this:
            [bracket[round[game{"map": str, "mode": str}]]
        """
        return [
            [
                [
                    {"map": None, "mode": None}
                    for _ in range(bracket["games"])
                ] for _ in range(bracket["rounds"])
            ] for bracket in self.brackets
        ]

    def gen_maplist(self):
        """Generate maplist."""
        for bracket in self.maplist:
            self.gen_bracket(bracket)

    def gen_bracket(self, bracket):
        """Generate maplist for a bracket."""
        # Empty all maps and modes
        self.pools.maps.empty()
        self.pools.modes.empty()
        # Generate rounds
        for _round in bracket:
            self.gen_round(_round)

    def gen_round(self, _round):
        """Generate a round for a bracket."""
        # Prune everything
        self.pools.maps.prune()
        self.pools.modes.prune()
        for pool in self.pools.values():
            pool.prune()
        # Generate games
        for game in _round:
            self.gen_game(game)

    def gen_game(self, game):
        """Generate a game."""
        game["map"], game["mode"] = self.pools.pick()

    def __iter__(self):
        return self.maplist
