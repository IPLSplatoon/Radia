"""
Class for storing map and mode data
"""


class MapSetStorage:
    def __init__(self):
        self.Maps = []
        self.Bracket = []
        self.Set = []
        self.locked = False

    def toggleLock(self):
        if self.locked:
            self.locked = False
        else:
            self.locked = True

    def setMaps(self, maps: list):
        self.Maps = maps

    def setBracket(self, bracket: list):
        self.Bracket = bracket

    def setSet(self, mapSet: list):
        self.Set = mapSet
