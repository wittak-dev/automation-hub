# Automation Hub v2 — Feature Backlog

**Last Updated**: 2026-05-03 — prodcheck onboarded, first autonomous PR opened
**Archive**: No archive yet (project is young)

---

## Current State

| Dimension | Status |
|-----------|--------|
| Core orchestrator | ✅ Complete (257 lines, well under 500 limit) |
| Test suite | ✅ Green (issue_selection + prompt_builder) |
| GitHub repo | wittak-dev/automation-hub |
| Governance template | ✅ Complete (templates/governance/) |
| Agent definitions | ✅ 6 agents defined |
| Target repos onboarded | 1 (prodcheck — active, PR #6 open) |

---

## Next Up

Active workstream — start here next session.

- **Review PR #6** on prodcheck — agent scaffolded pnpm monorepo, needs human review before merge
- **ONBOARD-002**: Onboard nuuance (has mature governance, needs workflow + label)
- **ONBOARD-003**: Onboard dAIg (has mature governance, awaiting Play Store review)

---

## Active Priority Order

> Work top to bottom. Do not start a row until the one above it is shipped.

| # | ID | What | Status |
|---|-----|------|--------|
| 1 | **GOV-001** | Create gold-standard governance template | ✅ SHIPPED (2026-05-02) |
| 2 | **ONBOARD-001** | Onboard prodcheck | ✅ SHIPPED (2026-05-03) |
| 3 | **SMOKE-001** | Live smoke test (prodcheck workflow) | ✅ SHIPPED (2026-05-03) |
| 4 | **ONBOARD-002** | Onboard nuuance | 🔴 NOT STARTED |
| 5 | **ONBOARD-003** | Onboard dAIg | 🔴 NOT STARTED |
| 6 | **ONBOARD-004** | Onboard HealthOS (after housekeeping) | 🔴 NOT STARTED |

---

## Feature Detail

### GOV-001: Gold-Standard Governance Template
**Status**: ✅ SHIPPED (2026-05-02)

Created `templates/governance/` with:
- CLAUDE.md.template (full constitutional framework)
- BACKLOG.md.template, LESSONS_LEARNED.md.template, SERVICES.md.template, CHANGELOG.md.template
- CLAUDE_NFT.md.template (non-functional testing module)
- gitignore.template
- README.md (onboarding guide)
- 6 agent definitions (nft-auditor, session-handoff, pr-reviewer, plan-architect, onboard-project, doc-sync)

### ONBOARD-001: Onboard prodcheck
**Status**: ✅ SHIPPED (2026-05-03)

All tasks completed:
- [x] Create governance template
- [x] Create prodcheck CLAUDE.md, BACKLOG.md, planning/, agents, .gitignore, NFT module
- [x] Initialise git repo, create GitHub repo (wittak-dev/prodcheck)
- [x] Add workflow file, create 5 autonomous-dev issues (#1–#5)
- [x] First workflow run successful — PR #6 opened by autonomous agent

### SMOKE-001: Live Smoke Test
**Status**: ✅ SHIPPED (2026-05-03)

Validated via prodcheck workflow runs. Discovered and fixed:
- Missing Issues: Read permission on PAT (403 on get_issues)
- acceptEdits insufficient for headless CI (switched to bypassPermissions)
- Agent SDK exit code 1 crashing orchestrator (added try/except)
- Issue comment 403 when PAT lacks Issues: Write (made best-effort)

---

## Status Legend

- 🔴 NOT STARTED
- 🚧 IN PROGRESS
- ✅ SHIPPED (YYYY-MM-DD)
- 🟡 BLOCKED (reason in notes)
