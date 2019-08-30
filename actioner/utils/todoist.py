from todoist.models import Item


def is_task_completed(task: Item):
    """
    `Item` doesn't support `.get`, so re-implement it
    """
    try:
        return task["checked"]
    except KeyError:
        return False


def get_existing_tasks(project_id, todoist):
    return {
        item["id"]: item["content"]
        for item in todoist.state["items"]
        if item["project_id"] == project_id
    }
