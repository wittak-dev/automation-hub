# Automation Hub v2 — Constitutional Framework

## What this repo is

A minimal, app-agnostic autonomous development orchestrator built on the Claude Agent SDK.
It runs in GitHub Actions, picks the oldest open `autonomous-dev` issue from a target repo,
invokes Claude Code headlessly to implement it, and opens a PR.

## Architecture

```
automation/
  autonomous_dev.py       entry point (arg parsing, orchestration loop)
  lib/
    issue_selection.py    fetch oldest open autonomous-dev issue (PyGithub)
    prompt_builder.py     build the Claude prompt (deterministic, no I/O side effects)
    pr_creator.py         push branch, open PR, post comment (GitPython + PyGithub)
templates/
  workflow.yml            GitHub Actions template for target repos
  AGENTS.md.template      starter constitutional framework for onboarding
tests/
  test_issue_selection.py
  test_prompt_builder.py
```

## Development rules for this repo

- **Keep total source under 500 lines** (`automation/**/*.py`, excluding tests and templates).
  If it grows past that, something has gone wrong — refactor rather than add.
- **TDD for deterministic modules.** `issue_selection.py` and `prompt_builder.py` must have
  tests before implementation changes.
- **No scope creep.** This hub is orchestration only — no dashboard, no reports, no Slack,
  no email, no partnership tracking. Those belong elsewhere.
- **Dependency discipline.** Only add a dependency to `requirements.txt` if there is no
  reasonable way to achieve the goal with the existing set.
- **Do not commit secrets.** `GITHUB_TOKEN`, `ANTHROPIC_API_KEY`, and any other credentials
  are environment variables only — never in code or config files.

## Running tests

```bash
pytest                          # full suite
pytest tests/test_issue_selection.py -v
pytest tests/test_prompt_builder.py -v
```

## Local dry-run

```bash
export GITHUB_TOKEN=ghp_...
python automation/autonomous_dev.py \
  --target-repo OWNER/REPO \
  --dry-run
```

## Adding a new target repo

See `README.md` for the 6-step onboarding guide.

## Git workflow

- Feature branches from `main`; PR to merge back
- `legacy/v1` branch and `v1-archive` tag preserve the November 2025 v1 codebase
