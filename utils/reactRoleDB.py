"""
Deals with storing information for reaction based role assignment
"""
import _pickle as pickle
import re
from typing import Optional
import os

unicodeExpression = re.compile("U\+([0-9]*[A-Z]*){5}")


class MessageRoleList:
    """
    This class stores the role and emotes that a message can have for reaction role assignments
    """
    def __init__(self):
        self.unicode = {}
        self.custom = {}

    def add_reaction(self, emoteID: str, roleID: str) -> bool:
        """
        Add a reaction and role to the message
        :param emoteID: str
            the emoteID or Unicode code of the emote to use
        :param roleID: str
            the ID of the role you want to add
        :return:
            if is was possible to add the reaction in or not
        """
        if unicodeExpression.match(emoteID):
            self.unicode[emoteID] = roleID
            return True
        if emoteID.isdigit():
            self.custom[emoteID] = roleID
            return True
        return False

    def get_role_id(self, emoteID: str) -> Optional[str]:
        """
        Get the role ID that's tied to a role
        :param emoteID: str
            the emoteID or Unicode code of the role you want to get
        :return: Optional[str]
            The ID of the role you want to find or the None if it doesn't exist
        """
        if unicodeExpression.match(emoteID):
            if emoteID in self.unicode:
                return self.unicode[emoteID]
        if emoteID.isdigit():
            if emoteID in self.custom:
                return self.custom[emoteID]
        return None

    def remove_role_id(self, emoteID: str) -> bool:
        """
        Remove a role from the list
        :param emoteID: str
            the emoteID or Unicode code of the role you want to remove
        :return: bool
            If it was remove successfully or not
        """
        if unicodeExpression.match(emoteID):
            if emoteID in self.unicode:
                del self.unicode[emoteID]
                return True
        if emoteID.isdigit():
            if emoteID in self.custom:
                del self.custom[emoteID]
                return True
        return False


class RoleReactList:
    def __init__(self, fileName: str):
        self.fileName = fileName
        self.messageList = {}
        if os.path.isfile(self.fileName):
            self.messageList = pickle.load(open(self.fileName, 'rb'))

    def add_message_reaction(self, messageID: str, emoteID: str, roleID: str) -> bool:
        if not messageID.isdigit():
            return False
        if messageID not in self.messageList:
            self.messageList[messageID] = MessageRoleList()
        messageRoleList = self.messageList[messageID]
        if messageRoleList.add_reaction(emoteID, roleID):
            pickle.dump(self.messageList, open(self.fileName, "wb"))
            return True
        return False

    def remove_message_reaction(self, messageID: str, emoteID: str, roleID: str) -> bool:
        if not messageID.isdigit():
            return False
        if messageID not in self.messageList:
            return False
        messageRoleList = self.messageList[messageID]
        if messageRoleList.add_reaction(emoteID, roleID):
            pickle.dump(self.messageList, open(self.fileName, "wb"))
            return True
        return False

    def get_reaction_role(self, messageID: str, emoteID: str) -> Optional[str]:
        if not messageID.isdigit():
            return None
        if messageID not in self.messageList:
            return None
        messageRoleList = self.messageList[messageID]
        return messageRoleList.get_role_id(emoteID)


