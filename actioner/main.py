import logging
from multiprocessing import Process

import click
import sentry_sdk
from apscheduler.util import get_callable_name

from actioner.cli import CLI_ENTRYPOINTS
from actioner.scheduler import create_scheduler
from actioner.settings import LOGGING_LEVEL, SENTRY_DSN
from actioner.web import get_server, run_server

logger = logging.getLogger(__name__)


@click.group()
def cli():
    logging.basicConfig(level=LOGGING_LEVEL)
    sentry_sdk.init(dsn=SENTRY_DSN)


@cli.command()
def start():
    Process(target=run_server, args=(get_server(),)).start()
    Process(target=create_scheduler().start).start()


@cli.command()
def once():
    scheduler = create_scheduler()
    jobs = {job.func for job in scheduler.get_jobs()}
    for job in jobs:
        logger.info("Executing '{}'".format(get_callable_name(job)))
        job()


for entry_point in CLI_ENTRYPOINTS:
    cli.command()(entry_point)


if __name__ == "__main__":
    cli()
