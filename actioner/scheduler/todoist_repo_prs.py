import logging

from github import PullRequest

from actioner.clients import github, todoist
from actioner.utils import get_todoist_project_from_repo
from actioner.utils.github import get_existing_task, get_issue_link

logger = logging.getLogger(__name__)


REPOS = ["srobo/core-team-minutes"]


def pr_to_task_name(pr: PullRequest) -> str:
    return "Review " + get_issue_link(pr) + ": " + pr.title


def get_my_review(me, pr: PullRequest):
    for review in pr.get_reviews():
        if review.user.login == me.login:
            return review


def todoist_repo_prs():
    me = github.get_user()
    todoist.projects.sync()
    todoist.items.sync()
    for repo_name in REPOS:
        project_id = get_todoist_project_from_repo(repo_name)
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
                    logger.info("Completing task to review '{}'".format(pr.title))
                    todoist.items.complete([existing_task_id])
                else:
                    logger.info("Deleting task to review '{}'".format(pr.title))
                    todoist.items.delete([existing_task_id])

            elif pr.state == "open":
                if existing_task_id is None:
                    logger.info("Creating task to review '{}'".format(pr.title))
                    existing_task_id = todoist.items.add(
                        pr_to_task_name(pr), project_id
                    )["id"]

                existing_task = todoist.items.get_by_id(existing_task_id)
                my_review = get_my_review(me, pr)
                if existing_task_id and my_review:
                    if (
                        my_review.commit_id == pr.head.sha
                        and not existing_task["checked"]
                    ):
                        logger.info("Completing task to review '{}'".format(pr.title))
                        todoist.items.complete([existing_task_id])
                    elif existing_task["checked"] and existing_task["checked"]:
                        logger.info("Re-opening task to review '{}'".format(pr.title))
                        todoist.items.uncomplete([existing_task_id])
                existing_task.update(content=pr_to_task_name(pr))
                if pr.milestone and pr.milestone.due_on:
                    existing_task.update(
                        date_string=pr.milestone.due_on.strftime("%d/%m/%Y")
                    )

    todoist.commit()
