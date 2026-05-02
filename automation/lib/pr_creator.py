"""Push the agent's branch and open a GitHub PR."""

import logging
import subprocess
from pathlib import Path

from github import Github
from github.Issue import Issue

log = logging.getLogger(__name__)

BRANCH_PREFIX = "autonomous/issue-"


def create(gh: Github, repo_name: str, issue: Issue, repo_dir: Path) -> str:
    """Push HEAD to the feature branch and open a PR. Returns the PR URL."""
    branch_name = f"{BRANCH_PREFIX}{issue.number}"

    # Push feature branch (git auth is pre-configured by actions/checkout in CI,
    # or by GITHUB_TOKEN embedded in the remote URL for local runs)
    subprocess.run(
        ["git", "push", "origin", f"HEAD:{branch_name}"],
        cwd=repo_dir,
        check=True,
    )

    # Open PR via GitHub API
    gh_repo = gh.get_repo(repo_name)
    pr = gh_repo.create_pull(
        title=f"[Auto] {issue.title} (#{issue.number})",
        body=_pr_body(issue),
        head=branch_name,
        base=gh_repo.default_branch,
    )

    # Post a comment on the original issue linking the PR (best-effort —
    # the PAT may lack Issues: Write permission)
    try:
        issue.create_comment(f"Autonomous development complete. PR opened: {pr.html_url}")
    except Exception as exc:
        log.warning("Could not comment on issue #%d: %s", issue.number, exc)

    return pr.html_url


def _pr_body(issue: Issue) -> str:
    return (
        f"Closes #{issue.number}\n\n"
        "This PR was opened automatically by the autonomous development orchestrator.\n\n"
        f"**Issue:** [{issue.title}]({issue.html_url})"
    )
