import asyncio

from apscheduler.schedulers.blocking import BlockingScheduler


def create_scheduler():
    scheduler = BlockingScheduler()
    return scheduler


def start_scheduler(scheduler):
    scheduler.start()
    asyncio.get_event_loop().run_forever()
