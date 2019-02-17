import asyncio

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from .todoist_assigned_issues import todoist_assigned_issues


def create_scheduler():
    scheduler = AsyncIOScheduler()
    scheduler.add_job(todoist_assigned_issues)
    return scheduler


def start_scheduler(scheduler):
    scheduler.start()
    asyncio.get_event_loop().run_forever()
