"""
Deals with storing information for reaction based role assignment
"""
import _pickle as pickle
import re

class serverRoleList:
    def __init__(self):
        self.unicode = {}
        self.custom = {}

    def add_unicode_reaction(self, unicodeCode: str, roleID: str):
        self.unicode[unicodeCode] = roleID

    def add_custom_reaction(self, customEmoteID: str, roleID: str):
        self.custom[customEmoteID] = roleID

    def add_reaction(self, emoteID: str, roleID: str):
        unicodeExpression = re.compile("")
