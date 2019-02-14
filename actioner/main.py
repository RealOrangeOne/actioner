import logging
from multiprocessing import Process

from aiohttp.web import run_app as run_web_app

from actioner.scheduler import create_scheduler, start_scheduler
from actioner.settings import LOGGING_LEVEL
from actioner.web import get_server


def main():
    logging.basicConfig(level=LOGGING_LEVEL)

    server = get_server()
    scheduler = create_scheduler()

    Process(target=run_web_app, args=(server,)).start()
    Process(target=start_scheduler, args=(scheduler,)).start()


if __name__ == '__main__':
    main()
