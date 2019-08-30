import logging
from multiprocessing import Process

import sentry_sdk
from sentry_sdk.integrations.aiohttp import AioHttpIntegration

from actioner.scheduler import create_scheduler
from actioner.settings import LOGGING_LEVEL, SENTRY_DSN
from actioner.web import get_server, run_server


def main():
    logging.basicConfig(level=LOGGING_LEVEL)

    sentry_sdk.init(dsn=SENTRY_DSN, integrations=[AioHttpIntegration()])

    server = get_server()
    scheduler = create_scheduler()

    # HACK: APScheduler doesn't like running in an external event loop. https://github.com/agronholm/apscheduler/issues/360
    Process(target=run_server, args=(server,)).start()
    Process(target=scheduler.start).start()


if __name__ == "__main__":
    main()
