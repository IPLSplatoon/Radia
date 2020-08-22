"""
Initalizes the early stuff for the entire application

This includes:
 - Setting up logging
 - Optionally setting up sentry
 - Opening a database connection
 - etc.
"""

import os
import logging

# Initialize logging
logging.basicConfig(
    level=(
        logging.DEBUG if os.getenv("DEBUG") else logging.INFO
    ),
    format='\033[31m%(levelname)s\033[0m \033[90min\033[0m \033[33m%(filename)s\033[0m \033[90mat\033[0m %(asctime)s\033[90m:\033[0m %(message)s',
    datefmt='\033[32m%m/%d/%Y\033[0m \033[90mon\033[0m \033[32m%H:%M:%S\033[0m'
)
logging.getLogger("discord").setLevel(logging.ERROR)
logging.getLogger("websockets").setLevel(logging.WARNING)
logging.getLogger("asyncio").setLevel(logging.WARNING)

logging.getLogger(__name__)

# Optionally initialize sentry
def initialize_sentry(sentry_env):
    import sentry_sdk
    from sentry_sdk.integrations.aiohttp import AioHttpIntegration
    from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration

    sentry_sdk.init(
        dsn="https://0070913733224711b3a9a3207b8ef7ab@o83253.ingest.sentry.io/5283135",
        integrations=[
            SqlalchemyIntegration(),
            AioHttpIntegration()
        ],
        environment=sentry_env
    )

if sentry_env := os.getenv("SENTRY"):
    initialize_sentry(sentry_env)
# TODO: Initialize database connection
