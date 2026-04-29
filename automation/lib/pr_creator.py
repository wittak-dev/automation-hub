"""Push the agent's branch and open a GitHub PR."""

from pathlib import Path

import git
from github import Github
from github.Issue import Issue

BRANCH_PREFIX = "autonomous/issue-"


def create(gh: Github, repo_name: str, issue: Issue, repo_dir: Path) -> str:
    """Push HEAD to *branch_name* and open a PR. Returns the PR URL."""
    branch_name = f"{BRANCH_PREFIX}{issue.number}"
    local_repo = git.Repo(repo_dir)

    # Push the feature branch to remote
    origin = local_repo.remote("origin")
    origin.push(refspec=f"HEAD:{branch_name}")

    # Open PR via GitHub API
    gh_repo = gh.get_repo(repo_name)
    pr = gh_repo.create_pull(
        title=f"[Auto] {issue.title} (#{issue.number})",
        body=_pr_body(issue),
        head=branch_name,
        base=gh_repo.default_branch,
    )

    # Post a comment on the original issue linking the PR
    issue.create_comment(
        f"Autonomous development complete. PR opened: {pr.html_url}"
    )

    return pr.html_url


def _pr_body(issue: Issue) -> str:
    return (
        f"Closes #{issue.number}\n\n"
        "This PR was opened automatically by the autonomous development orchestrator.\n\n"
        f"**Issue:** [{issue.title}]({issue.html_url})"
    )
