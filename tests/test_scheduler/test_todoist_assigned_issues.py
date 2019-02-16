from collections import namedtuple

from actioner.clients import github, todoist
from actioner.scheduler.todoist_assigned_issues import (
    REPOS,
    get_existing_task,
    get_issue_link,
    issue_to_task_name,
)
from tests import BaseTestCase

FakeIssue = namedtuple('FakeIssue', ['number', 'html_url', 'title'])


class IssueTaskNameTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.issue = FakeIssue(123, 'https://github.com/repo/thing', 'issue title')

    def test_creates_link(self):
        self.assertEqual(get_issue_link(self.issue), "[#123](https://github.com/repo/thing)")
        self.assertIn(self.issue.html_url, get_issue_link(self.issue))

    def test_task_name_contains_title(self):
        self.assertIn(self.issue.title, issue_to_task_name(self.issue))

    def test_task_name_contains_link(self):
        self.assertIn(get_issue_link(self.issue), issue_to_task_name(self.issue))


class ConfigurationTestCase(BaseTestCase):
    def test_repos_exist(self):
        for repo in REPOS.keys():
            github.get_repo(repo)

    def test_projects_exist(self):
        todoist.projects.sync()
        project_ids = {project['id'] for project in todoist.state['projects']}
        for project_id in REPOS.values():
            self.assertIn(project_id, project_ids)


class ExistingTaskTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.tasks = {
            123: '[#1](url): title',
            456: '[#2](url/2): title 2',
            789: '[#3](url/3): title 3',
        }

    def test_finds_existing_repos(self):
        self.assertEqual(
            get_existing_task(self.tasks, FakeIssue(1, 'url', 'title')),
            123
        )

    def test_not_existing_repo(self):
        self.assertIsNone(
            get_existing_task(self.tasks, FakeIssue(123, 'url', 'title'))
        )
