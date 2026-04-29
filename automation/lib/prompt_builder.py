"""Build the autonomous-dev prompt from a GitHub issue and a cloned repo."""

from pathlib import Path

from github.Issue import Issue

_SEP = "\n\n---\n\n"


def build(issue: Issue, repo_dir: Path) -> str:
    """Return the full prompt string to send to the Claude Agent SDK."""
    sections = [
        _preamble(),
        _issue_section(issue),
    ]

    backlog = _read_file(repo_dir / "BACKLOG.md")
    if backlog:
        sections.append(f"## Backlog context\n\n{backlog}")

    sections.append(_instructions())
    return _SEP.join(sections)


# ── private helpers ────────────────────────────────────────────────────────────

def _preamble() -> str:
    return (
        "You are an autonomous developer working on a GitHub issue. "
        "Follow the project's CLAUDE.md / AGENTS.md constitutional framework exactly. "
        "Write production-quality code with tests where appropriate."
    )


def _issue_section(issue: Issue) -> str:
    body = issue.body or "(no description provided)"
    return (
        f"## Issue to implement\n\n"
        f"**#{issue.number}: {issue.title}**\n\n"
        f"{body}\n\n"
        f"Issue URL: {issue.html_url}"
    )


def _instructions() -> str:
    return (
        "## Instructions\n\n"
        "1. Implement the issue described above.\n"
        "2. Run existing tests if present; do not break them.\n"
        "3. Add tests for new logic where appropriate.\n"
        "4. Commit your changes with a clear commit message referencing the issue number.\n"
        "5. Do NOT push or create a PR — the orchestrator handles that.\n"
        "6. When done, output a brief summary of the changes you made."
    )


def _read_file(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8").strip()
    except (FileNotFoundError, PermissionError):
        return ""
