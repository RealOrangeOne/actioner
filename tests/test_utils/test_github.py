from collections import namedtuple

from actioner.utils.github import get_existing_task, get_issue_link
from tests import BaseTestCase

FakeIssue = namedtuple("FakeIssue", ["number", "html_url", "title"])


class IssueLinkTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.issue = FakeIssue(123, "https://github.com/repo/thing", "issue title")

    def test_creates_link(self):
        self.assertEqual(
            get_issue_link(self.issue), "[#123](https://github.com/repo/thing)"
        )


class ExistingTaskTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.tasks = {
            123: "[#1](url): title",
            456: "[#2](url/2): title 2",
            789: "[#3](url/3): title 3",
        }

    def test_finds_existing_repos(self):
        self.assertEqual(
            get_existing_task(self.tasks, FakeIssue(1, "url", "title")), 123
        )

    def test_not_existing_repo(self):
        self.assertIsNone(get_existing_task(self.tasks, FakeIssue(123, "url", "title")))
