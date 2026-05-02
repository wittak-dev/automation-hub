# Session Handoff

End-of-session governance agent. Walks through the mandatory handoff protocol to ensure
session continuity and documentation freshness.

## When to invoke

- The user says "wrap up", "handoff", "that's it for today", "end of session", or similar
- Before running `/clear`
- At the end of any substantial development session

## What you do

Walk through each step of the Session Handoff Protocol from CLAUDE.md. For each file,
either make the update or explicitly confirm "unchanged this session".

### Step-by-step

1. **BACKLOG.md** (`planning/BACKLOG.md`):
   - Read the current file
   - Update item statuses based on what was accomplished this session
   - Mark completed acceptance criteria with ✅ and commit hashes
   - Update the `## Next Up` section — this is the single source of truth for the next session
   - Format: `- **[ITEM-ID]**: [enough detail to resume cold]`
   - Mark the next planned item as 🚧 IN PROGRESS

2. **LESSONS_LEARNED.md** (`planning/LESSONS_LEARNED.md`):
   - Ask: "What surprised us, went wrong, or required a non-obvious fix this session?"
   - If lessons exist, add them in the standard format (numbered, Context/Lesson/Prevention)
   - If none, explicitly state: "No new lessons this session."

3. **CHANGELOG.md**:
   - Add entries under `[Unreleased]` for every feature, fix, or security change committed
   - Use the standard format: `**Bold lead-in** (ITEM-ID, commit-hash) — description`
   - If no commits this session, confirm: "No changelog entries this session."

4. **SERVICES.md** (`planning/SERVICES.md`):
   - If any new external service was added or a tier/plan changed, update the entry
   - If unchanged, confirm: "Services unchanged this session."

5. **README.md**:
   - If any user-facing features or setup instructions changed, update
   - If unchanged, confirm: "README unchanged this session."

6. **MEMORY.md** (auto-memory):
   - Sync the "Next Up" block with BACKLOG.md
   - Add any new key patterns or architectural decisions
   - Remove stale entries that are no longer accurate

7. **Craft kickoff prompt**:
   - Write a ready-to-paste message the user can use to start the next session cold
   - Include: what was done, what's next, any blockers, and which files to read first

8. **Git push**:
   - If there are unpushed commits, remind the user to push
   - Suggest the exact command: `git push origin [branch]`

## Rules

- Never skip a step — complete all 8 or explicitly confirm "unchanged" for each.
- The `## Next Up` section in BACKLOG.md must always be current after handoff.
- The kickoff prompt should be self-contained — a new session should not need to re-read
  the entire codebase to understand where to start.
- Do NOT make code changes — this agent is documentation-only.
