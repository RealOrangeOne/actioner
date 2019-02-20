from actioner.clients import github, todoist
from actioner.utils import (
    GH_ORG_TO_TODOIST,
    GH_REPO_TO_TODOIST,
    get_todoist_project_from_repo,
)
from tests import BaseTestCase


class TodoistProjectToRepoTestCase(BaseTestCase):
    def test_repos_exist(self):
        for repo_name in GH_REPO_TO_TODOIST.keys():
            github.get_repo(repo_name)

    def test_gets_correct_project(self):
        for repo_name, project_id in GH_REPO_TO_TODOIST.items():
            self.assertEqual(get_todoist_project_from_repo(repo_name), project_id)

    def test_gets_correct_project_for_org(self):
        for org_name, project_id in GH_ORG_TO_TODOIST.items():
            self.assertEqual(get_todoist_project_from_repo("{}/test_repo".format(org_name)), project_id)

    def test_organization_exists(self):
        for org in GH_ORG_TO_TODOIST.keys():
            github.get_organization(org)

    def test_project_exists(self):
        project_ids = set(GH_ORG_TO_TODOIST.values()).union(GH_REPO_TO_TODOIST.values())
        todoist.projects.sync()
        todoist_project_ids = {project['id'] for project in todoist.state['projects']}
        for project in project_ids:
            self.assertIn(project, todoist_project_ids)
