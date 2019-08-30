import datetime
from typing import Dict

from dateutil.relativedelta import relativedelta

from actioner.clients import github


def get_issue_link(issue_or_pr) -> str:
    return "[#{id}]({url})".format(id=issue_or_pr.number, url=issue_or_pr.html_url)


def get_existing_task(tasks: Dict[int, str], issue_or_pr):
    issue_link = get_issue_link(issue_or_pr)
    for task_id, task_title in tasks.items():
        if issue_link in task_title:
            return task_id
    return None


def get_relevant_issues():
    since = datetime.datetime.now() - relativedelta(weeks=1)
    for repo in github.get_user().get_repos():
        if repo.updated_at < since:
            continue
        for issue in repo.get_issues(since=since, state="all"):
            if issue.pull_request is None:
                yield issue
