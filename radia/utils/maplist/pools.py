"""Contains Pools class."""


class Pools:
    """Class containing utility methods for handling pools."""

    MIN_MAPS = 8

    class NotEnoughMaps(Exception):
        """There aren't enough maps in the map pool."""

    def __init__(self, *, sz, tc, rm, cb) -> dict:
        """ Create a dictionary representation of map pools.
        :params: A list of :str maps:
        :return dict: A dictionary with modes as keys and a list of :str maps: as values.
            {"Splat Zones": [maps]}
        """
        if any(len(pool) < self.MIN_MAPS for pool in [sz, tc, rm, cb]):
            raise self.NotEnoughMaps(f"Map pool must have {self.MIN_MAPS} or more maps.")

        self.pools = {
            "Splat Zones": sz,
            "Tower Control": tc,
            "Rainmaker": rm,
            "Clam Blitz": cb,
        }

    def total_maps(self):
        """Return the total number of maps in the pool."""
        total = 0
        for maps in self.pools.values():
            total += len(maps)
        return total

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
