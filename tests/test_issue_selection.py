from datetime import datetime, timezone
from unittest.mock import MagicMock

import pytest

from automation.lib.issue_selection import get_oldest_issue


def _make_issue(number, title, created_at, labels=None):
    issue = MagicMock()
    issue.number = number
    issue.title = title
    issue.body = f"Body of issue {number}"
    issue.created_at = created_at
    issue.html_url = f"https://github.com/owner/repo/issues/{number}"
    label_mocks = [MagicMock(name=n) for n in (labels or [])]
    issue.labels = label_mocks
    return issue


def _make_gh(issues):
    gh = MagicMock()
    repo = MagicMock()
    repo.get_issues.return_value = issues
    gh.get_repo.return_value = repo
    return gh


def test_returns_oldest_labelled_issue():
    older = _make_issue(1, "Old issue", datetime(2024, 1, 1, tzinfo=timezone.utc))
    newer = _make_issue(2, "Newer issue", datetime(2024, 6, 1, tzinfo=timezone.utc))
    gh = _make_gh([newer, older])

    result = get_oldest_issue(gh, "owner/repo")

    assert result is not None
    assert result.number == 1


def test_returns_none_when_no_issues():
    gh = _make_gh([])
    assert get_oldest_issue(gh, "owner/repo") is None


def test_calls_get_issues_with_label():
    gh = _make_gh([])
    get_oldest_issue(gh, "owner/repo", label="autonomous-dev")
    gh.get_repo.return_value.get_issues.assert_called_once_with(
        state="open", labels=["autonomous-dev"]
    )


def test_single_issue_returned_directly():
    only = _make_issue(7, "Only issue", datetime(2025, 3, 15, tzinfo=timezone.utc))
    gh = _make_gh([only])
    assert get_oldest_issue(gh, "owner/repo").number == 7
