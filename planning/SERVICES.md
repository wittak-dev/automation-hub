# Automation Hub — Services Registry

**Last updated**: 2026-05-02 (initial creation)
**Rule**: Update this file whenever a new external service is added or an existing plan/tier changes — same session, before commit.

---

## AI / Machine Learning

### Anthropic (Claude Agent SDK)

| Field | Value |
|-------|-------|
| Plan | Pay-as-you-go |
| Cost | Variable — depends on target repo complexity and issue count |
| Purpose | Powers the autonomous development agent. SDK invoked headlessly in GitHub Actions to implement issues. Model and turn limits controlled by `autonomous_dev.py`. |
| Scale trigger | Monthly spend exceeding budget cap in Anthropic console. Set a cap BEFORE enabling scheduled runs. |
| Env var(s) | `ANTHROPIC_API_KEY` |
| Notes | Budget cap is critical — a misconfigured agent running across multiple repos at 03:00 can burn real money. SDK version pinned to 0.1.71. |

---

## Source Control & CI

### GitHub (API + Actions)

| Field | Value |
|-------|-------|
| Plan | Free tier (public repos) / Pro (private repos) |
| Cost | Actions minutes: 2,000 free/month (GitHub Free), 3,000 (Pro) |
| Purpose | Hosts all repos. GitHub Actions runs the autonomous dev workflow on schedule. PyGithub used for issue selection and PR creation. |
| Scale trigger | Actions minutes approaching limit; or need for concurrent workflow runs across multiple target repos. |
| Env var(s) | `GITHUB_TOKEN` (fine-grained PAT with Contents: Read & Write, Pull requests: Read & Write) |
| Notes | Fine-grained PAT should NOT include workflow scope — prevents agents from modifying CI config. See README.md for exact permission requirements. |

---

## Development Tools

### Python venv

| Field | Value |
|-------|-------|
| Plan | N/A (local tooling) |
| Cost | Free |
| Purpose | Isolated Python 3.11 environment at `venv/`. All dependencies from `requirements.txt`. |
| Scale trigger | N/A |
| Env var(s) | None |
| Notes | Activate with `source venv/bin/activate`. CI uses `pip install -r requirements.txt` directly (no venv in Actions). |
