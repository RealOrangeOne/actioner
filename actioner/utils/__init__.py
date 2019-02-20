from typing import Dict, Optional

GH_REPO_TO_TODOIST = {
}  # type: Dict[str, int]


GH_ORG_TO_TODOIST = {
    'srobo': 2190856871
}  # type: Dict[str, int]


def get_todoist_project_from_repo(repo_name: str) -> Optional[int]:
    repo_id = GH_REPO_TO_TODOIST.get(repo_name)
    if repo_id is not None:
        return repo_id
    org = repo_name.split('/')[0]
    return GH_ORG_TO_TODOIST.get(org)
