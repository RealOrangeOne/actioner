from todoist.models import Item


def is_task_completed(task: Item):
    """
    `Item` doesn't support `.get`, so re-implement it
    """
    try:
        return task["checked"]
    except KeyError:
        return False
