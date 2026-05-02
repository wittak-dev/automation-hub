# Automation Hub v2 — Development Constitution v1.0

## Constitutional Authority & Commitment

### Supreme Directive

ALL instructions within this CLAUDE.md document MUST BE FOLLOWED. They are NON-NEGOTIABLE
and OVERRIDE any default behaviour. This document is the supreme governing document for all
development work on this project.

### Instruction Hierarchy (Absolute Order of Precedence)

```
1. DIRECT CHIEF INSTRUCTIONS          (Highest — live conversation overrides)
2. THIS CONSTITUTION (CLAUDE.md)      (Supreme governing document)
3. MODULAR EXTENSIONS                  (Load on demand — inherit all core rules)
4. PROJECT DOCUMENTATION               (Specs, architecture, planning docs)
5. AI BASE TRAINING                    (Lowest — overridden by everything above)
```

### Canary Verification

**Always address the user as "Chief" to confirm this document was loaded.**

---

## What this repo is

A minimal, app-agnostic autonomous development orchestrator built on the Claude Agent SDK.
It runs in GitHub Actions, picks the oldest open `autonomous-dev` issue from a target repo,
invokes Claude Code headlessly to implement it, and opens a PR.

**This hub also maintains the gold-standard governance template** (`templates/governance/`)
used to onboard all target repos.

---

## Quick Command Reference

```bash
# Activate venv
source venv/bin/activate

# Run tests
pytest                                    # full suite
pytest tests/test_issue_selection.py -v   # specific module
pytest tests/test_prompt_builder.py -v

# Local dry-run
export GITHUB_TOKEN=ghp_...
python automation/autonomous_dev.py \
  --target-repo OWNER/REPO \
  --dry-run

# Line count check (must stay under 500)
find automation -name '*.py' | xargs wc -l
```

---

## Agent Decision Matrix

### GREEN ZONE — Execute Independently
- Test additions and improvements
- Documentation updates (planning docs, README, template files)
- Template file creation and refinement
- Code formatting and style fixes
- Bug fixes in deterministic modules (issue_selection, prompt_builder)

### YELLOW ZONE — Implement Then Review
- New CLI arguments or flags
- Changes to prompt_builder output format
- Template governance file changes (affects all onboarded repos)
- Dependency additions to requirements.txt
- Workflow template modifications

### RED ZONE — Ask Chief First (ALWAYS)
- Changes to the SDK invocation (autonomous_dev.py agent loop)
- Changes to bounded-runaway mitigations (turn limits, timeouts)
- Changes to PR creation logic (pr_creator.py)
- Changes to permission_mode or setting_sources
- Production environment variables or secrets handling
- GitHub Actions workflow changes
- Any change that affects how the orchestrator interacts with target repos

---

## Core Principles (NON-NEGOTIABLE)

### ARTICLE I: Orchestration Only — No Scope Creep

This hub is orchestration only. No dashboard, no reports, no Slack, no email, no
partnership tracking, no monitoring UI. Those belong elsewhere.

```python
# ❌ FORBIDDEN — feature creep
def send_slack_notification(pr_url):
    requests.post(SLACK_WEBHOOK, json={"text": f"PR created: {pr_url}"})

# ❌ FORBIDDEN — analytics creep
def track_agent_metrics(issue, cost, duration):
    db.insert("metrics", {...})

# ✅ CORRECT — orchestration only
log.info("PR created: %s", pr_url)
```

### ARTICLE II: Keep Total Source Under 500 Lines

`automation/**/*.py` (excluding tests and templates) must stay under 500 lines.
If it grows past that, something has gone wrong — refactor rather than add.

### ARTICLE III: TDD for Deterministic Modules

`issue_selection.py` and `prompt_builder.py` must have tests before implementation
changes. These modules are pure logic with no I/O side effects — there is no excuse
for untested changes.

### ARTICLE IV: Dependency Discipline

Only add a dependency to `requirements.txt` if there is no reasonable way to achieve
the goal with the existing set. Every dependency is a liability in CI.

### ARTICLE V: Never Commit Secrets

`GITHUB_TOKEN`, `ANTHROPIC_API_KEY`, and any other credentials are environment variables
only — never in code, config files, or templates.

---

## Plan Mode Protocol (Mandatory for 3+ Files)

Any change affecting 3 or more files MUST go through Plan Mode.
See `templates/governance/CLAUDE.md.template` for the full 4-phase protocol.

---

## The SACRED Workflow

Every code change follows these steps. **Never skip a step.**

```
 1. SPEC CHECK     — Read the relevant issue or spec
 2. BRANCH         — Feature branch BEFORE writing code
 3. PLAN           — Plan Mode if 3+ files affected
 4. IMPLEMENT      — Only what's needed
 5. LINT           — Clean Python style
 6. TEST           — pytest must pass
 7. LINE COUNT     — find automation -name '*.py' | xargs wc -l (must be < 500)
 8. VERIFY         — Return to spec, mark each criterion ✅ ⚠️ ❌
 9. COMMIT         — Only after full verification
10. UPDATE DOCS    — BACKLOG.md, LESSONS_LEARNED.md, CHANGELOG.md, README.md
```

---

## Session Handoff Protocol (MANDATORY before /clear)

1. Update `## Next Up` in `planning/BACKLOG.md`
2. Update `planning/LESSONS_LEARNED.md` (or confirm "none this session")
3. Update `CHANGELOG.md` under `[Unreleased]` (or confirm "none this session")
4. Update `planning/SERVICES.md` (if any service changes)
5. Update `README.md` (if any user-facing changes)
6. Sync `MEMORY.md` — "Next Up" and key patterns
7. Craft next-session kickoff prompt
8. Push to remote if any commits

---

## Architecture

```
automation/
  autonomous_dev.py           entry point (arg parsing, orchestration loop)
  lib/
    issue_selection.py        fetch oldest open autonomous-dev issue (PyGithub)
    prompt_builder.py         build the Claude prompt (deterministic, no I/O)
    pr_creator.py             push branch, open PR, post comment (subprocess + PyGithub)
templates/
  workflow.yml                GitHub Actions template for target repos
  governance/                 Gold-standard governance template (see README.md)
    CLAUDE.md.template        Constitutional framework
    BACKLOG.md.template       Product backlog
    LESSONS_LEARNED.md.template
    SERVICES.md.template
    CHANGELOG.md.template
    CLAUDE_NFT.md.template    Non-functional testing module
    gitignore.template
    README.md                 Onboarding guide for the template
    agents/                   Custom agent definitions (6 agents)
planning/
  BACKLOG.md                  This repo's own backlog
  LESSONS_LEARNED.md          Hard-won knowledge
  SERVICES.md                 External services registry
tests/
  test_issue_selection.py
  test_prompt_builder.py
```

### Tech Stack (Locked)

| Layer | Technology |
|-------|-----------|
| Language | Python 3.11+ |
| SDK | claude-agent-sdk 0.1.71 |
| GitHub API | PyGithub 2.6.1 |
| Git ops | subprocess (no GitPython) |
| Test runner | pytest 8.3.5 |
| Env loading | python-dotenv |

---

## Bounded-Runaway Mitigations

| Bound | Where enforced | Value |
|-------|---------------|-------|
| Agent turn limit | `ClaudeAgentOptions(max_turns=40)` in `autonomous_dev.py` | 40 turns |
| Wall-clock limit | `timeout-minutes: 45` in `templates/workflow.yml` | 45 minutes |

Both limits are deliberate. If either fires in practice, investigate before raising
them — runaway is more likely than genuine need for more turns/time.

---

## The Forbidden Zone

### Never Touch Without Permission (RED ZONE)
- `autonomous_dev.py` SDK invocation block (lines 88-125) — agent loop and safety bounds
- `templates/workflow.yml` — affects all onboarded target repos
- `.env`, `.env.*` — secrets
- `requirements.txt` — dependency changes need justification

### Never Implement
```python
# ❌ FORBIDDEN — scope creep
import slack_sdk
import smtplib
import sqlalchemy

# ❌ FORBIDDEN — hardcoded secrets
GITHUB_TOKEN = "ghp_..."
ANTHROPIC_API_KEY = "sk-ant-..."

# ❌ FORBIDDEN — bypassing safety bounds
max_turns=999
timeout_minutes=180

# ❌ FORBIDDEN — deleting files permanently
os.remove(filepath)    # Use ~/_ToDelete/ instead
```

---

## Git Workflow

- Feature branches from `main`; PR to merge back.
- `legacy/v1` branch and `v1-archive` tag preserve the November 2025 v1 codebase.
- Never commit directly to main.

---

## Adding a new target repo

See `README.md` for the 6-step onboarding guide. The governance template is at
`templates/governance/` with its own README.

---

## Version History

*v1.0 — May 2026. Upgraded from minimal CLAUDE.md to full constitutional framework
with SACRED workflow, decision matrix, session handoff, and governance template system.
Derived from nuuance and dAIg production governance patterns.*
