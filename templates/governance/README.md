# Governance Template — Onboarding Guide

A battle-tested governance framework for autonomous and human-led development, extracted from
production projects (nuuance, dAIg) over a year of iterative refinement.

---

## What's in the box

| File | Purpose | Commit to git? |
|------|---------|---------------|
| `CLAUDE.md.template` | Constitutional framework — the supreme governing document | Yes |
| `BACKLOG.md.template` | Product backlog with priority ordering and session handoff | Your choice* |
| `LESSONS_LEARNED.md.template` | Hard-won knowledge base (numbered, Context/Lesson/Prevention) | Yes |
| `SERVICES.md.template` | External services registry (plan, cost, scale triggers) | Yes |
| `CHANGELOG.md.template` | Keep a Changelog format with item IDs and commit hashes | Yes |
| `CLAUDE_NFT.md.template` | Non-functional testing module (security, performance, privacy) | Yes |
| `gitignore.template` | Recommended .gitignore with governance-aware patterns | Yes |
| `agents/` | Six custom agent definitions (see below) | Yes |

\* BACKLOG.md may contain sensitive planning/pricing info. nuuance and dAIg gitignore theirs;
  commit it if your project has no sensitive planning data.

---

## Agents included

| Agent | File | Trigger |
|-------|------|---------|
| **nft-auditor** | `agents/nft-auditor.md` | New dependency, pre-release, monthly, new API route |
| **session-handoff** | `agents/session-handoff.md` | End of session ("wrap up", "handoff", "that's it") |
| **pr-reviewer** | `agents/pr-reviewer.md` | PR opened or ready for review |
| **plan-architect** | `agents/plan-architect.md` | Any task touching 3+ files |
| **onboard-project** | `agents/onboard-project.md` | New project kickoff |
| **doc-sync** | `agents/doc-sync.md` | After a feature merge or commit |

Copy `agents/*.md` to the target repo's `.claude/agents/` directory.

---

## Onboarding a new project (step by step)

### 1. Copy and customise CLAUDE.md

```bash
cp CLAUDE.md.template /path/to/project/CLAUDE.md
```

Replace all `[PLACEHOLDER]` values. At minimum:
- Quick Command Reference (build, test, lint, format, dev commands)
- Core Principles (2-4 project-specific articles with code examples)
- Architecture Overview (tech stack table, directory structure)
- Forbidden Zone (critical files list)

### 2. Create the planning directory

```bash
mkdir -p /path/to/project/planning/plans
cp BACKLOG.md.template /path/to/project/planning/BACKLOG.md
cp LESSONS_LEARNED.md.template /path/to/project/planning/LESSONS_LEARNED.md
cp SERVICES.md.template /path/to/project/planning/SERVICES.md
```

### 3. Create the changelog

```bash
cp CHANGELOG.md.template /path/to/project/CHANGELOG.md
```

### 4. Set up the NFT module

```bash
mkdir -p /path/to/project/docs/constitution
cp CLAUDE_NFT.md.template /path/to/project/docs/constitution/CLAUDE_NFT.md
```

Customise: Lighthouse thresholds, data classification, critical flows.

### 5. Install agents

```bash
mkdir -p /path/to/project/.claude/agents
cp agents/*.md /path/to/project/.claude/agents/
```

### 6. Set up .gitignore

```bash
cp gitignore.template /path/to/project/.gitignore
```

Review and uncomment/add project-specific patterns.

### 7. First commit

```bash
cd /path/to/project
git add CLAUDE.md CHANGELOG.md planning/ docs/constitution/ .claude/agents/ .gitignore
git commit -m "feat: add governance framework (constitution, backlog, agents)"
```

---

## Governance philosophy

The system is built on five pillars:

1. **Constitution** — CLAUDE.md is the supreme document. All rules flow from it.
2. **Workflow discipline** — The SACRED workflow ensures every change is spec-checked,
   tested, verified, and documented before it's committed.
3. **Knowledge capture** — Lessons Learned prevents the same mistake twice.
   Services Registry prevents "what does this env var do?" confusion.
4. **Session continuity** — The handoff protocol and "Next Up" pattern ensure any
   session can resume cold without re-reading the entire codebase.
5. **Autonomous safety** — The decision matrix (Green/Yellow/Red) and bounded-runaway
   mitigations (turn limits, time limits) make autonomous development safe.

---

## Evolving the governance

- **Add constitutional modules** as the project grows. Common additions: DEPLOYMENT,
  DATABASE, PAYMENTS, AI_INTEGRATION, DEBUGGING, TESTING.
- **Promote lessons to rules** — when a lesson recurs 3+ times, add it to CLAUDE.md
  or a constitutional module as a permanent rule.
- **Version the constitution** — bump the version number and add a changelog entry
  at the bottom of CLAUDE.md whenever rules change.
- **Cross-project review** — periodically compare governance across sibling projects
  to propagate improvements.

---

*Template version: 1.0 — May 2026*
*Derived from nuuance (WhatsApp Analyser) and dAIg governance patterns.*
