# Changelog — Automation Hub

All notable changes to this project are documented here.
The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) conventions.

---

## [Unreleased]

### Added
- **Gold-standard governance template** (GOV-001) — full template set in `templates/governance/` including CLAUDE.md, BACKLOG.md, LESSONS_LEARNED.md, SERVICES.md, CHANGELOG.md, CLAUDE_NFT.md templates, .gitignore template, and onboarding README
- **Six custom agent definitions** (GOV-001) — nft-auditor, session-handoff, pr-reviewer, plan-architect, onboard-project, doc-sync in `templates/governance/agents/`
- **Automation-hub own governance** (GOV-001) — upgraded CLAUDE.md to full constitutional framework with SACRED workflow, decision matrix, session handoff protocol. Added `planning/` directory with BACKLOG.md, LESSONS_LEARNED.md, SERVICES.md

### Changed
- **CLAUDE.md** — upgraded from minimal framework to full constitutional v1.0 with authority ladder, canary verification, Green/Yellow/Red decision matrix, SACRED workflow, session handoff, forbidden zone

---

## [2.0.0] — v2 Launch (2026-04-30)

### Added
- **Complete v2 rewrite** — minimal autonomous dev orchestrator built on Claude Agent SDK
- **autonomous_dev.py** — entry point with --dry-run, --issue, --repo-dir flags
- **issue_selection.py** — fetch oldest open autonomous-dev issue via PyGithub
- **prompt_builder.py** — deterministic prompt construction (no I/O side effects)
- **pr_creator.py** — push branch, open PR, post comment via subprocess + PyGithub
- **workflow.yml** — GitHub Actions template for target repos
- **CLAUDE.md.template** — starter constitutional framework for onboarding

### Removed
- **v1 codebase** — archived at tag `v1-archive` and branch `legacy/v1`

---

<!-- Comparison links:
[Unreleased]: https://github.com/wittak-dev/automation-hub/compare/v2.0.0...HEAD
[2.0.0]: https://github.com/wittak-dev/automation-hub/releases/tag/v2.0.0
-->
