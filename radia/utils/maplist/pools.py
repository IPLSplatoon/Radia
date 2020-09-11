"""Contains Pools class."""

from .bag import Bag


class Pools:
    """Class containing utility methods for handling pools."""

    MIN_MAPS = 8

    class NotEnoughMaps(Exception):
        """ There aren't enough maps in the map pool.
        
        Contains 5 different bags:
        - 1 bag for each pool
        - 1 bag for all maps
        - 1 bag for modes

        Bags:
            Pool[mode]: Gets the bag for the pool
            Pool.maps: Gets the bag for all maps
            Pool.modes: Gets the bag for modes
        
        Methods:
            Pool.pick(): Returns a new tuple(map, mode) pick
        """

    def __init__(self, *, sz, tc, rm, cb) -> dict:
        """ Create a class to represent map pools.
        :params set: A :set: of :str maps:
        :return dict: A dictionary with modes as keys and a Bag of :maps: as values.
            {"Splat Zones": [maps]}
        """
        # Check if any map pool has less than the minimum allowed maps
        if any(len(pool) < self.MIN_MAPS for pool in [sz, tc, rm, cb]):
            raise self.NotEnoughMaps(f"Map pool must have {self.MIN_MAPS} or more maps.")
        
        # Create bags
        self.pools = {
            "Splat Zones": Bag(sz),
            "Tower Control": Bag(tc),
            "Rainmaker": Bag(rm),
            "Clam Blitz": Bag(cb),
        }
        self.maps: Bag = Bag(self.__total_maps())
        self.modes: Bag = Bag(set(self.pools.keys()))

    def pick(self):
        """Pick a map and mode."""
        mode = self.pick_mode()
        _map = self.pick_map(mode)
        return _map, mode

    def pick_mode(self):
        """Pick a mode."""
        mode = next(iter(self.modes))
        self.modes.pick(mode)
        return mode
    
    def pick_map(self, mode):
        """Pick a map."""
        # Pick a new map from the bag
        try:
            _map = next(iter(set(self[mode]) - self.maps.recents))
        except StopIteration:
            # Start removing maps from recents until a map can be picked
            if self.maps.recents:
                self.maps.recents.pop()
            else:
                self[mode].recents.pop()
            _map = self.pick_map(mode)

        # Add map to recents
        self.maps.pick(_map)
        self[mode].pick(_map)
        return _map

    def keys(self):
        self.pools.keys()

    def values(self):
        self.pools.values()

    def items(self):
        self.pools.items()

    def __getitem__(self, key):
        return self.pools[key]

    def __total_maps(self) -> set:
        """Return all of the maps in all pools."""
        total = set()
        for maps in self.pools.values():
            total += set(maps)
        return total
