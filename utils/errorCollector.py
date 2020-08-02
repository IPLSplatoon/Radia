import sentry_sdk
from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration
from sentry_sdk.integrations.aiohttp import AioHttpIntegration
from dotenv import load_dotenv
import os
import datetime
import git

repo = git.Repo(search_parent_directories=True)
load_dotenv("files/.env")
SystemEnvironment = os.environ.get("system_environment")

sentry_sdk.init(dsn="https://0070913733224711b3a9a3207b8ef7ab@o83253.ingest.sentry.io/5283135",
                integrations=[SqlalchemyIntegration(), AioHttpIntegration()],
                release="radia@{}".format(repo.head.object.hexsha),
                environment=SystemEnvironment)


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
