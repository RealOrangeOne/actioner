import argparse
import logging
from multiprocessing import Process

import sentry_sdk
from apscheduler.util import get_callable_name
from sentry_sdk.integrations.aiohttp import AioHttpIntegration

from actioner.scheduler import create_scheduler
from actioner.settings import LOGGING_LEVEL, SENTRY_DSN
from actioner.web import get_server, run_server

logger = logging.getLogger(__name__)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--once", action="store_true")
    return parser.parse_args()


def main():
    logging.basicConfig(level=LOGGING_LEVEL)

    sentry_sdk.init(dsn=SENTRY_DSN, integrations=[AioHttpIntegration()])

    args = parse_args()

    if args.once:
        scheduler = create_scheduler()
        jobs = {job.func for job in scheduler.get_jobs()}
        for job in jobs:
            logger.info("Executing '{}'".format(get_callable_name(job)))
            job()
    else:
        Process(target=run_server, args=(get_server(),)).start()
        Process(target=create_scheduler().start).start()


if __name__ == "__main__":
    main()
