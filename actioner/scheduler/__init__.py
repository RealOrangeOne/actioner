import asyncio

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.interval import IntervalTrigger

from .todoist_assigned_issues import todoist_assigned_issues
from .todoist_repo_prs import todoist_repo_prs


def create_scheduler():
    scheduler = BlockingScheduler()
    scheduler.add_job(todoist_assigned_issues, "interval", minutes=15)
    scheduler.add_job(todoist_repo_prs, "interval", minutes=15)

    for job in scheduler.get_jobs():
        if isinstance(job.trigger, IntervalTrigger):
            scheduler.add_job(job.func)

    return scheduler
