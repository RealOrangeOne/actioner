from actioner.scheduler.todoist_assigned_issues import REPOS
from actioner.utils import get_todoist_project_from_repo
from tests import BaseTestCase


class ConfigurationTestCase(BaseTestCase):
    def test_repo_is_known(self):
        for repo in REPOS:
            self.assertIsNotNone(get_todoist_project_from_repo(repo))
