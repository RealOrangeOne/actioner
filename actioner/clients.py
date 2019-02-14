import os
import tempfile

from github import Github
from todoist import TodoistAPI

from actioner.settings import GITHUB_TOKEN, TODOIST_TOKEN

github = Github(GITHUB_TOKEN)
todoist = TodoistAPI(TODOIST_TOKEN, cache=os.path.join(tempfile.gettempdir(), 'todoist-api'))
