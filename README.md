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
| `AUTOMATION_HUB_PAT` | A fine-grained GitHub PAT (see permissions below) |

**Fine-grained PAT permissions required:**

| Resource | Access |
|----------|--------|
| `wittak-dev/automation-hub` | Contents: Read |
| `OWNER/target-repo` | Contents: Read & Write, Pull requests: Read & Write |

> **Omit the `workflow` scope.** A fine-grained PAT without workflow permissions cannot modify `.github/workflows/` files, which is the correct safe default — the agent has no business touching CI configuration. Only add workflow write access if you explicitly want the agent to be able to modify workflow files.

### 3. Add the workflow file

Copy `templates/workflow.yml` from this repo into the target repo at `.github/workflows/autonomous-dev.yml`. Replace the placeholder on the last line:

```
TARGET_REPO_SLUG  →  owner/repo-name   (e.g. robwhitaker/nuuance)
```

### 4. Add a `CLAUDE.md` constitutional framework

Copy `templates/CLAUDE.md.template` to the target repo root as `CLAUDE.md`. Fill in the project description, tech stack, test commands, and any areas the agent should not touch.

### 5. Create a smoke-test issue

Open an issue in the target repo labelled `autonomous-dev` with a small, self-contained task — for example: *"Add a CONTRIBUTING.md file with basic contribution guidelines"*.

> **Before enabling the schedule:** set a monthly Anthropic API budget cap in the [Anthropic console](https://console.anthropic.com). A misconfigured agent running across multiple repos at 03:00 can quietly burn real money before you notice.

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
```

### Smoke testing with --dry-run

```bash
export GITHUB_TOKEN=ghp_...
python automation/autonomous_dev.py --target-repo OWNER/REPO --dry-run
```

When run against a repo with **no open `autonomous-dev` issues** (such as this repo itself), the expected output is:

```
No open autonomous-dev issues in OWNER/REPO — nothing to do.
```

That is the success path, not a failure. The orchestrator exits 0 and does nothing — which is correct behaviour when there is no work to pick up. To exercise the full prompt-construction path, either pass `--issue N` with an existing issue number, or create a labelled issue first.

## Architecture

See `CLAUDE.md` for the full constitutional framework and file-by-file description.

## Legacy

v1 code (November 2025) is preserved at tag `v1-archive` and branch `legacy/v1`.
