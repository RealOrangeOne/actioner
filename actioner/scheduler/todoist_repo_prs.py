import logging

from github import PullRequest

from actioner.clients import get_todoist_client, github
from actioner.utils import get_todoist_project_from_repo
from actioner.utils.github import get_existing_task, get_issue_link
from actioner.utils.todoist import is_task_completed

logger = logging.getLogger(__name__)


REPOS = ["srobo/competition-team-minutes"]


def pr_to_task_name(pr: PullRequest) -> str:
    return "Review " + get_issue_link(pr) + ": " + pr.title


def get_my_review(me, pr: PullRequest):
    for review in pr.get_reviews().reversed:
        if review.user.login == me.login:
            return review


def todoist_repo_prs():
    todoist = get_todoist_client()
    me = github.get_user()
    todoist.projects.sync()
    todoist.items.sync()
    for repo_name in REPOS:
        project_id = get_todoist_project_from_repo(repo_name)
        if not project_id:
            continue
        existing_tasks = {
            item["id"]: item["content"]
            for item in todoist.state["items"]
            if item["project_id"] == project_id
        }
        repo = github.get_repo(repo_name)
        for pr in repo.get_pulls(state="all"):
            existing_task_id = get_existing_task(existing_tasks, pr)

            if pr.state == "closed" and existing_task_id:
                my_review = get_my_review(me, pr)
                if pr.merged and my_review and my_review.state == "APPROVED":
                    if not is_task_completed(todoist.items.get_by_id(existing_task_id)):
                        logger.info("Completing task to review '{}'".format(pr.title))
                        todoist.items.complete([existing_task_id])
                else:
                    logger.info("Deleting task to review '{}'".format(pr.title))
                    todoist.items.delete([existing_task_id])

            elif pr.state == "open":
                my_review = get_my_review(me, pr)

                if existing_task_id:
                    existing_task = todoist.items.get_by_id(existing_task_id)
                    task_completed = is_task_completed(existing_task)
                    if my_review:
                        if my_review.commit_id == pr.head.sha and not task_completed:
                            logger.info(
                                "Completing task to review '{}', because I already did it".format(
                                    pr.title
                                )
                            )
                            todoist.items.complete([existing_task_id])
                        elif task_completed:
                            logger.info(
                                "Re-opening task to review '{}'".format(pr.title)
                            )
                            todoist.items.uncomplete([existing_task_id])
                        continue
                elif my_review and my_review.commit_id != pr.head.sha:
                    logger.info("Creating task to review '{}'".format(pr.title))
                    existing_task_id = todoist.items.add(
                        pr_to_task_name(pr), project_id
                    )["id"]
                if existing_task_id is not None:
                    existing_task = todoist.items.get_by_id(existing_task_id)
                    existing_task.update(content=pr_to_task_name(pr))
                    if pr.milestone and pr.milestone.due_on:
                        existing_task.update(
                            date_string=pr.milestone.due_on.strftime("%d/%m/%Y")
                        )

    todoist.commit()
