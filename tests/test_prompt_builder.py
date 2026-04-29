from pathlib import Path
from unittest.mock import MagicMock

from automation.lib.prompt_builder import build


def _make_issue(number=42, title="Fix the bug", body="It crashes on startup"):
    issue = MagicMock()
    issue.number = number
    issue.title = title
    issue.body = body
    issue.html_url = f"https://github.com/owner/repo/issues/{number}"
    return issue


def test_prompt_contains_issue_number_and_title(tmp_path):
    result = build(_make_issue(), tmp_path)
    assert "#42" in result
    assert "Fix the bug" in result


def test_prompt_contains_issue_body(tmp_path):
    result = build(_make_issue(), tmp_path)
    assert "It crashes on startup" in result


def test_prompt_contains_autonomous_developer_preamble(tmp_path):
    result = build(_make_issue(), tmp_path)
    assert "autonomous developer" in result.lower()


def test_prompt_includes_backlog_when_present(tmp_path):
    (tmp_path / "BACKLOG.md").write_text("## Priority 1\n- Do the thing", encoding="utf-8")
    result = build(_make_issue(), tmp_path)
    assert "Do the thing" in result


def test_prompt_skips_backlog_section_when_absent(tmp_path):
    result = build(_make_issue(), tmp_path)
    assert "Backlog context" not in result


def test_prompt_handles_issue_with_no_body(tmp_path):
    result = build(_make_issue(body=None), tmp_path)
    assert "no description" in result


def test_prompt_contains_do_not_push_instruction(tmp_path):
    result = build(_make_issue(), tmp_path)
    assert "Do NOT push" in result or "do not push" in result.lower()
