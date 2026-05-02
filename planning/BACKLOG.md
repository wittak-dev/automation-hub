# Automation Hub v2 — Feature Backlog

**Last Updated**: 2026-05-02 — governance framework added, prodcheck onboarding in progress
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
| Target repos onboarded | 0 (prodcheck next) |

---

## Next Up

Active workstream — start here next session.

- **ONBOARD-001**: Onboard prodcheck as first target repo — CLAUDE.md, BACKLOG.md, planning/, agents, git init, GitHub repo, workflow, first autonomous-dev issue
- **SMOKE-001**: Refresh GITHUB_TOKEN and run dry-run smoke test against prodcheck

---

## Active Priority Order

> Work top to bottom. Do not start a row until the one above it is shipped.

| # | ID | What | Status |
|---|-----|------|--------|
| 1 | **GOV-001** | Create gold-standard governance template | ✅ SHIPPED (2026-05-02) |
| 2 | **ONBOARD-001** | Onboard prodcheck | 🚧 IN PROGRESS |
| 3 | **SMOKE-001** | Dry-run smoke test (requires fresh GITHUB_TOKEN) | 🔴 NOT STARTED |
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
**Status**: 🚧 IN PROGRESS
**Priority**: HIGH

**Tasks:**
- [x] Create governance template
- [ ] Create prodcheck CLAUDE.md
- [ ] Create prodcheck BACKLOG.md from week-1-scaffold-spec
- [ ] Create prodcheck planning/ directory with LESSONS_LEARNED.md and SERVICES.md
- [ ] Install agent definitions
- [ ] Initialise git repo
- [ ] Create GitHub repo
- [ ] Add workflow file
- [ ] Create first autonomous-dev issue

### SMOKE-001: Dry-Run Smoke Test
**Status**: 🔴 NOT STARTED
**Blocked on**: Fresh GITHUB_TOKEN (current one returns 401)

---

## Status Legend

- 🔴 NOT STARTED
- 🚧 IN PROGRESS
- ✅ SHIPPED (YYYY-MM-DD)
- 🟡 BLOCKED (reason in notes)
