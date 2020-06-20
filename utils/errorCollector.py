import sentry_sdk
import datetime

sentry_sdk.init("https://0070913733224711b3a9a3207b8ef7ab@o83253.ingest.sentry.io/5283135")


def collect_error(error: Exception, message: str):
    """
    Collects, print and sends errors to sentry
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
    sentry_sdk.capture_exception(error)
