"""
Holds all the errors that can come up
"""


class MoreThenOneError(AttributeError):
    """
    Raised when then one of an object
    """
    pass


class CheckInBlockedError(AttributeError):
    """
    Raised when team hasn't had checkin enabled for them
    """
    pass
