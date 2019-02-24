from github import Github
from todoist import TodoistAPI

from actioner.settings import GITHUB_TOKEN, TODOIST_TOKEN

github = Github(GITHUB_TOKEN)


def get_todoist_client():
    """
    The Todoist client isn't thread safe, so we need to create it each time we want to use it
    """
    return TodoistAPI(TODOIST_TOKEN)
