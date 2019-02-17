import logging
from typing import Dict

from github import Issue

from actioner.clients import github, todoist

REPOS = {
    'srobo/tasks': 2190856871,
    'srobo/core-team-minutes': 2190856871
}

LABEL_TO_STATUS = {
    'must have': 4,
    'critical': 4,
    'should have': 2
}

logger = logging.getLogger(__name__)


def get_status_for_issue(issue: Issue) -> int:
    priorities = {
        LABEL_TO_STATUS.get(label.name.lower(), 1)
        for label in issue.labels
    }
    return max(priorities, default=1)


def get_issue_link(issue: Issue) -> str:
    return "[#{id}]({url})".format(
        id=issue.number,
        url=issue.html_url
    )


def issue_to_task_name(issue: Issue) -> str:
    return get_issue_link(issue) + ": " + issue.title


def get_existing_task(tasks: Dict[int, str], issue: Issue):
    issue_link = get_issue_link(issue)
    for task_id, task_title in tasks.items():
        if task_title.startswith(issue_link):
            return task_id
    return None


def todoist_assigned_issues():
    me = github.get_user()
    todoist.projects.sync()
    todoist.items.sync()
    for repo_name, project_id in REPOS.items():
        existing_tasks = {item['id']: item['content'] for item in todoist.state['items'] if item['project_id'] == project_id}
        repo = github.get_repo(repo_name)
        for issue in repo.get_issues(assignee=me.login, state='all'):
            me_assigned = me.login in {assignee.login for assignee in issue.assignees}
            existing_task_id = get_existing_task(existing_tasks, issue)

            if existing_task_id and not me_assigned:
                logger.info("Deleting task for '{}'".format(issue.title))
                todoist.items.delete([existing_task_id])
                continue

            elif issue.state == 'closed' and existing_task_id is not None:
                logger.info("Completing task for '{}'".format(issue.title))
                todoist.items.complete([existing_task_id])
                continue

            if issue.state == 'open':
                if existing_task_id is None:
                    logger.info("Creating task for '{}'".format(issue.title))
                    existing_task_id = todoist.items.add(
                        issue_to_task_name(issue),
                        project_id
                    )['id']
                existing_task = todoist.items.get_by_id(existing_task_id)
                existing_task.update(
                    content=issue_to_task_name(issue),
                    priority=get_status_for_issue(issue)
                )
                if issue.milestone and issue.milestone.due_on:
                    existing_task.update(date_string=issue.milestone.due_on.strftime("%d/%m/%Y"))

    todoist.commit()
