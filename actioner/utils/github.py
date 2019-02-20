from typing import Dict


def get_issue_link(issue_or_pr) -> str:
    return "[#{id}]({url})".format(
        id=issue_or_pr.number,
        url=issue_or_pr.html_url
    )


def get_existing_task(tasks: Dict[int, str], issue_or_pr):
    issue_link = get_issue_link(issue_or_pr)
    for task_id, task_title in tasks.items():
        if issue_link in task_title:
            return task_id
    return None
