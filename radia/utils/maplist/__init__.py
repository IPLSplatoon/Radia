"""Contains Maplist class."""

from .bag import Bag
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
