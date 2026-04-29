# Automation Hub v2

Minimal autonomous development orchestrator built on the [Claude Agent SDK](https://github.com/anthropics/claude-agent-sdk-python).

Runs on a schedule in GitHub Actions, picks the oldest open `autonomous-dev` issue from a target repo, invokes Claude Code headlessly to implement it, and opens a PR.

---

## Onboarding a new target repo (6 steps)

### 1. Add the `autonomous-dev` label

In the target repo on GitHub, go to **Issues → Labels → New label** and create a label named exactly `autonomous-dev`.

### 2. Set repository secrets

In the target repo, go to **Settings → Secrets and variables → Actions** and add:

| Secret | Value |
|--------|-------|
| `ANTHROPIC_API_KEY` | Your Claude API key |
| `AUTOMATION_HUB_PAT` | A GitHub Personal Access Token with `repo` and `workflow` scopes |

### 3. Add the workflow file

Copy `templates/workflow.yml` from this repo into the target repo at `.github/workflows/autonomous-dev.yml`. Replace the placeholder on the last line:

```
TARGET_REPO_SLUG  →  owner/repo-name   (e.g. robwhitaker/nuuance)
```

### 4. Add an `AGENTS.md` constitutional framework

Copy `templates/AGENTS.md.template` to the target repo root as `AGENTS.md`. Fill in the project description, tech stack, test commands, and any areas the agent should not touch.

### 5. Create a smoke-test issue

Open an issue in the target repo labelled `autonomous-dev` with a small, self-contained task — for example: *"Add a CONTRIBUTING.md file with basic contribution guidelines"*.

### 6. Trigger and verify

On the target repo, go to **Actions → Autonomous Dev → Run workflow**. After it completes, confirm:
- A PR has been opened referencing the issue.
- A comment has been posted on the issue linking the PR.
- The workflow run shows no errors.

---

## Supported target repos

| Repo | Status |
|------|--------|
| nuuance | pending onboarding |
| dAIg | pending onboarding |
| HealthOS | pending onboarding |
| prodcheck | planned |

---

## Local development

```bash
# Install dependencies
pip install -r requirements.txt

# Run the test suite
pytest

# Dry-run against any repo (no SDK call, no git operations)
export GITHUB_TOKEN=ghp_...
python automation/autonomous_dev.py --target-repo OWNER/REPO --dry-run
```

## Architecture

See `CLAUDE.md` for the full constitutional framework and file-by-file description.

## Legacy

v1 code (November 2025) is preserved at tag `v1-archive` and branch `legacy/v1`.
