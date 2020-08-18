"""
Deals with collecting and handling errors.
If a 'sentry_env' field is found in the .env file, this handler will automatically attach to Sentry.
"""
import os
import datetime

from dotenv import load_dotenv
load_dotenv("files/.env")
SENTRY_ENV = os.environ.get("sentry_env")


class ErrorCollector:

    def __init__(self, env):
        self.env = env
        
        if not self.env:
            print("Loaded error collector: Without Sentry")
        else:
            print("Loaded error collector: With Sentry")
            import sentry_sdk
            from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration
            from sentry_sdk.integrations.aiohttp import AioHttpIntegration

            import git
            repo = git.Repo(search_parent_directories=True)

            self.sentry_sdk = sentry_sdk
            self.sentry_sdk.init(
                dsn="https://0070913733224711b3a9a3207b8ef7ab@o83253.ingest.sentry.io/5283135",
                integrations=[SqlalchemyIntegration(), AioHttpIntegration()],
                release="radia@" + repo.head.object.hexsha,
                environment=self.env
            )

    def collector(self, error: Exception, message: str) -> None:
        """
        Collects, print and sends errors to sentry.
        :param message: str
            Message to send
        :param error: Exception
            error object
        :return: None
        """
        print("\n".join([
            "===================",
            f"Error @ {datetime.datetime.utcnow()}",
            message,
            error,
            "==================="
        ]))
        if self.env:
            self.sentry_sdk.capture_exception(error)

error = ErrorCollector(SENTRY_ENV)
