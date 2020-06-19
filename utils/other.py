"""
Deals with random utils wit no home
"""
import datetime


def collect_error(error: Exception, message: str):
    """
    Collects and print errors
    :param message: str
        Message to send
    :param error: Exception
        error object
    :return: None
    """
    print("===================")
    print("Error @ {}".format(datetime.datetime.utcnow()))
    print(message)
    print(error)
    print("===================")
