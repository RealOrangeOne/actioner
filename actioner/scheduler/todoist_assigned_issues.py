from typing import Dict

from github import Issue

from actioner.clients import github, todoist

REPOS = {
    'srobo/tasks': 2190856871,
    'srobo/core-team-minutes': 2190856871
}


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
        if issue_link in task_title:
            return task_id
    return None


def todoist_assigned_issues():
    me = github.get_user()
    todoist.projects.sync()
    todoist.items.sync()
    for repo_name, project_id in REPOS.items():
        existing_tasks = {item['id']: item['content'] for item in todoist.state['items'] if item['project_id'] == project_id}
        repo = github.get_repo(repo_name)
        for issue in repo.get_issues(assignee=me.login):
            existing_task_id = get_existing_task(existing_tasks, issue)
            if existing_task_id is None:
                existing_task_id = todoist.items.add(
                    issue_to_task_name(issue),
                    project_id
                )['id']
            existing_task = todoist.items.get_by_id(existing_task_id)
            existing_task.update(
                content=issue_to_task_name(issue)
            )
            if issue.milestone and issue.milestone.due_on:
                existing_task.update(date_string=issue.milestone.due_on.strftime("%d/%m/%Y"))

        for issue in repo.get_issues(assignee=me.login, state='closed'):
            existing_task_id = get_existing_task(existing_tasks, issue)
            if existing_task_id is not None:
                todoist.items.complete([existing_task_id])

    todoist.commit()
