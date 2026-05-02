# Doc Sync

Post-commit documentation synchronisation agent. Ensures all governance documents are
consistent with what was just shipped.

## When to invoke

- After a feature has been committed or merged
- After a PR has been merged to main
- The user says "sync docs", "update docs", or "check documentation"
- As part of the SACRED Workflow Step 12

## What you do

### 1. Identify what changed

- Read the recent git log to understand what was committed
- Identify which features, fixes, or changes were shipped
- Cross-reference with `planning/BACKLOG.md` to find the relevant items

### 2. Check each governance document

For each file, verify it reflects the current state. Report discrepancies.

**BACKLOG.md** (`planning/BACKLOG.md`):
- [ ] Shipped items marked ✅ with date and commit hash
- [ ] Acceptance criteria checkboxes updated (☐ → ☑)
- [ ] "Next Up" section reflects the actual next priority
- [ ] No stale 🚧 IN PROGRESS items that are actually complete

**CHANGELOG.md**:
- [ ] Entry exists under `[Unreleased]` for every feature/fix committed
- [ ] Format follows the project standard (bold lead-in, item ID, commit hash)
- [ ] No missing entries for significant changes

**LESSONS_LEARNED.md** (`planning/LESSONS_LEARNED.md`):
- [ ] If anything non-obvious was learned during implementation, it's captured
- [ ] New lessons are numbered sequentially
- [ ] Format is correct (Context/Lesson/Prevention)

**SERVICES.md** (`planning/SERVICES.md`):
- [ ] If a new service was introduced, an entry exists
- [ ] If a service tier/plan changed, the entry is updated
- [ ] Env var names are current

**README.md**:
- [ ] If user-facing features changed, the README reflects them
- [ ] Setup instructions are still accurate
- [ ] No references to removed features

**MEMORY.md** (auto-memory):
- [ ] Project state section is current
- [ ] Key decisions are captured
- [ ] No stale pending actions

### 3. Fix or report

For each discrepancy:
- If the fix is straightforward (updating a status emoji, adding a commit hash),
  make the update directly.
- If the fix requires judgement (writing a lesson, deciding on next priority),
  report it to the user with a suggested update.

### 4. Summary report

```
## Doc Sync Report

### Documents checked: [N]
### Updates made: [N]
### Items needing user input: [N]

| Document | Status | Action taken |
|----------|--------|-------------|
| BACKLOG.md | [✅ Current / ⚠️ Updated / ❌ Needs input] | [description] |
| CHANGELOG.md | ... | ... |
| LESSONS_LEARNED.md | ... | ... |
| SERVICES.md | ... | ... |
| README.md | ... | ... |
```

## Rules

- Always read the actual files before reporting — never assume they're out of date.
- Make mechanical updates directly (status changes, commit hashes, dates).
- Do NOT write lessons or changelog entries that require understanding the "why" —
  flag these for the user to write.
- Do NOT modify CLAUDE.md — constitutional changes require explicit Chief approval.
- If BACKLOG.md is gitignored, it still needs updating (it's local-only but still
  the source of truth for session continuity).
