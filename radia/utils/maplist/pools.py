"""Contains Pools class."""


class Pools:
    """Class containing utility methods for handling pools."""

    MIN_MAPS = 8

    class NotEnoughMaps(Exception):
        """There aren't enough maps in the map pool."""

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

    def modes(self):
        """Return all the modes of the pools."""
        return list(self.pools.keys())

    def sz(self):
        return self.pools["Splat Zones"]

    def tc(self):
        return self.pools["Tower Control"]

    def rm(self):
        return self.pools["Rainmaker"]

    def cb(self):
        return self.pools["Clam Blitz"]
