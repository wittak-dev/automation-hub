"""Select the oldest open issue with a given label from a GitHub repository."""

from typing import Optional

from github import Github
from github.Issue import Issue


def get_oldest_issue(
    gh: Github,
    repo_name: str,
    label: str = "autonomous-dev",
) -> Optional[Issue]:
    """Return the oldest open issue with *label*, or None if none found."""
    repo = gh.get_repo(repo_name)
    issues = list(repo.get_issues(state="open", labels=[label]))
    if not issues:
        return None
    return min(issues, key=lambda i: i.created_at)
