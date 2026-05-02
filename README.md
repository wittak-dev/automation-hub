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

Copy `templates/workflow.yml` from this repo into the target repo at `.github/workflows/autonomous-dev.yml`. No substitution is required — `${{ github.repository }}` resolves automatically to the host repo's slug at runtime.

### 4. Apply the governance framework

The full governance template is at `templates/governance/` with its own [onboarding guide](templates/governance/README.md). At minimum:

```bash
# From the automation-hub repo root:
cp templates/governance/CLAUDE.md.template /path/to/target/CLAUDE.md
mkdir -p /path/to/target/{planning/plans,docs/constitution,.claude/agents}
cp templates/governance/BACKLOG.md.template /path/to/target/planning/BACKLOG.md
cp templates/governance/LESSONS_LEARNED.md.template /path/to/target/planning/LESSONS_LEARNED.md
cp templates/governance/SERVICES.md.template /path/to/target/planning/SERVICES.md
cp templates/governance/CHANGELOG.md.template /path/to/target/CHANGELOG.md
cp templates/governance/CLAUDE_NFT.md.template /path/to/target/docs/constitution/CLAUDE_NFT.md
cp templates/governance/agents/*.md /path/to/target/.claude/agents/
```

Then customise `CLAUDE.md` — fill in the project description, tech stack, test commands, core principles, decision matrix, and forbidden zone. See the [governance README](templates/governance/README.md) for the full guide.

The governance framework includes 6 custom agent definitions (NFT auditor, session handoff, PR reviewer, plan architect, onboard project, doc sync) that automate the governance steps most often skipped under time pressure.

### 5. Create a smoke-test issue

Open an issue in the target repo labelled `autonomous-dev` with a small, self-contained task — for example: *"Add a `.editorconfig` file with two-space indentation, LF line endings, and final newline enforced."*

> **Before enabling the schedule:** set a monthly Anthropic API budget cap in the [Anthropic console](https://console.anthropic.com). A misconfigured agent running across multiple repos at 03:00 can quietly burn real money before you notice.

### 6. Trigger and verify

On the target repo, go to **Actions → Autonomous Dev → Run workflow**. After it completes, confirm:
- A PR has been opened referencing the issue.
- A comment has been posted on the issue linking the PR.
- The workflow run shows no errors.

### Troubleshooting

| Symptom | Likely cause and fix |
|---------|----------------------|
| **Workflow doesn't trigger** | Workflow file may be on a non-default branch, or `workflow_dispatch` is not enabled in the repo's Actions settings. Check **Actions → Autonomous Dev** exists and is not disabled. |
| **"Checkout automation-hub" step fails** | `AUTOMATION_HUB_PAT` is expired, missing, or lacks `Contents: Read` on `wittak-dev/automation-hub`. Regenerate the PAT and update the secret. |
| **"Run autonomous dev" 401s from Anthropic** | `ANTHROPIC_API_KEY` is missing or expired in the target repo's secrets. |
| **Workflow completes but no PR appears** | The agent ran but made no commits. The orchestrator deliberately skips PR creation when nothing has changed (see the `initial_sha` short-circuit in `autonomous_dev.py`). This is not a failure — it means the agent judged there was nothing actionable. |
| **`git push` fails** | The PAT lacks `Contents: Read & Write` on the target repo. Update the PAT's permissions or create a new one. |
| **Agent ignores `CLAUDE.md`** | The `CLAUDE.md` file is missing from the target repo root, or it was not committed to the default branch that the workflow checks out. |

---

## Pausing a target repo

When a project hits MVP, goes into maintenance mode, or otherwise needs to be parked, pause autonomous development without removing the integration:

**Recommended — disable the workflow:**
On the target repo, go to **Actions → Autonomous Dev → ⋯ → Disable workflow**. The schedule stops immediately. Re-enable from the same menu when development resumes. The workflow file, secrets, and labelled issues remain untouched.

**For finer-grained control:**
Remove the `autonomous-dev` label from any open issues you don't want picked up. The orchestrator only selects labelled issues, so unlabelled ones are ignored. Useful when you want most autonomous activity paused but still want a specific issue addressed.

**To remove a target repo entirely:**
Delete the `.github/workflows/autonomous-dev.yml` file from the target repo and remove the `ANTHROPIC_API_KEY` and `AUTOMATION_HUB_PAT` secrets from its settings. Update the "Supported target repos" table in this README to reflect the change.

---

## Supported target repos

| Repo | Status | Notes |
|------|--------|-------|
| prodcheck | governance applied, pending git init + workflow | First target. Week 1 scaffold spec ready. |
| nuuance | pending onboarding | Has mature governance already; needs workflow + label. |
| dAIg | pending onboarding | Has mature governance already; awaiting Play Store review. |
| HealthOS | pending onboarding | Needs housekeeping first (strategy review, backlog creation). |

**Status legend:** `active` — scheduled runs enabled and verified; `paused` — workflow disabled, integration intact; `pending onboarding` — not yet set up.

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
export GITHUB_TOKEN=ghp_...   # fine-grained PAT or classic PAT with repo read + PR write
python automation/autonomous_dev.py --target-repo OWNER/REPO --dry-run
```

The `GITHUB_TOKEN` used here should be either the same fine-grained PAT configured in Actions, or a separate classic PAT scoped to read issues and create PRs on the target repo.

When run against a repo with **no open `autonomous-dev` issues** (such as this repo itself), the expected output is:

```
No open autonomous-dev issues in OWNER/REPO — nothing to do.
```

That is the success path, not a failure. The orchestrator exits 0 and does nothing — which is correct behaviour when there is no work to pick up.

To exercise the full prompt-construction path against a specific issue without relying on date ordering, use the `--issue N` flag:

```bash
python automation/autonomous_dev.py --target-repo OWNER/REPO --issue 42 --dry-run
```

This selects issue #42 directly and prints the constructed prompt, regardless of its label or creation date.

## Architecture

See `CLAUDE.md` for the full constitutional framework and file-by-file description.

## Legacy

v1 code (November 2025) is preserved at tag `v1-archive` and branch `legacy/v1`.
