import logging
from multiprocessing import Process

import sentry_sdk
from aiohttp.web import run_app as run_web_app

from actioner.scheduler import create_scheduler, start_scheduler
from actioner.settings import LOGGING_LEVEL, SENTRY_DSN
from actioner.web import get_server


def main():
    logging.basicConfig(level=LOGGING_LEVEL)

    sentry_sdk.init(
        dsn=SENTRY_DSN,
    )

    server = get_server()
    scheduler = create_scheduler()

    # HACK: APScheduler doesn't like running in an external event loop. https://github.com/agronholm/apscheduler/issues/360
    Process(target=run_web_app, args=(server,)).start()
    Process(target=start_scheduler, args=(scheduler,)).start()


if __name__ == '__main__':
    main()
