"""
Contains the Classes that define how data is stored
"""


class Replies:
    def __init__(self, reply: str, imageLink: str = ""):
        self.reply = reply
        self.image = imageLink


class Responses:
    """
    Object for holding responses list
    """

    def __init__(self, options: list, variantList: dict, replies: list):
        """
        Constructor
        :param options: dict
            List of options and their reply number
        :param replies: list
            List of replies available
        """
        self.options = options
        self.variantList = variantList
        self.replies = replies
