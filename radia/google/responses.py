"""
This file holds the the responses for the information responses
"""


class Reply:
    """
    This holds the reply that would will be given to
    the user.
    """
    def __init__(self, reply: str, image_link: str = ""):
        self.reply = reply
        self.image = image_link


class Responses:
    """
    Object for holding responses list
     """
    def __init__(self, options: list, replies: dict):
        self.options = options  # This should hold all the options available under prefix0
        self.replies = replies  # This holds the each prefix and the accompanying Reply object
