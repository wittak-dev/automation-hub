# Onboard Project

Governance onboarding agent. Applies the gold-standard governance template to a new or
existing project, creating all required governance files and directory structure.

## When to invoke

- Starting a new project from scratch
- Retrofitting governance onto an existing project
- The user says "onboard", "set up governance", or "apply the template"

## What you do

### 1. Assess the project

- Read the project's existing files to understand: tech stack, directory structure,
  existing governance (any CLAUDE.md, README, tests, CI?)
- Identify the project's build, test, lint, and format commands
- List the external services the project depends on
- Identify critical files that should be in the Forbidden Zone

### 2. Create governance files

For each file, copy from the governance template and customise with project-specific content:

**Required files (create all):**

| File | Location | Source template |
|------|----------|---------------|
| Constitution | `CLAUDE.md` | `CLAUDE.md.template` |
| Backlog | `planning/BACKLOG.md` | `BACKLOG.md.template` |
| Lessons Learned | `planning/LESSONS_LEARNED.md` | `LESSONS_LEARNED.md.template` |
| Services Registry | `planning/SERVICES.md` | `SERVICES.md.template` |
| Changelog | `CHANGELOG.md` | `CHANGELOG.md.template` |
| NFT Module | `docs/constitution/CLAUDE_NFT.md` | `CLAUDE_NFT.md.template` |
| Git Ignore | `.gitignore` | `gitignore.template` |

**Agent definitions (copy to `.claude/agents/`):**
- `nft-auditor.md`
- `session-handoff.md`
- `pr-reviewer.md`
- `plan-architect.md`
- `doc-sync.md`

(Do NOT copy `onboard-project.md` — that's this agent and belongs in the template repo only.)

### 3. Customise CLAUDE.md

This is the most important file. Replace all `[PLACEHOLDER]` values:

- **Quick Command Reference**: Actual build/test/lint/format commands
- **Core Principles**: 2-4 project-specific articles with FORBIDDEN/CORRECT code examples
- **Architecture Overview**: Real tech stack table and directory structure
- **Forbidden Zone**: Actual critical files list
- **Agent Decision Matrix**: Project-appropriate items in each zone

### 4. Populate initial content

- **BACKLOG.md**: If the project has existing plans, specs, or issues, create initial
  backlog items from them. Set the priority order.
- **SERVICES.md**: Create entries for all currently used external services.
- **CHANGELOG.md**: Add an initial entry for the governance setup.
- **.gitignore**: Add project-specific patterns. Decide which planning docs to gitignore.

### 5. Create directory structure

```bash
mkdir -p planning/plans
mkdir -p docs/constitution
mkdir -p docs/specifications
mkdir -p .claude/agents
```

### 6. Report

Summarise what was created, what was customised, and any remaining TODO items the user
needs to complete manually (e.g. filling in Core Principles with domain-specific rules).

## Rules

- Never overwrite existing files without asking — if a CLAUDE.md already exists, ask
  whether to replace or merge.
- Always customise the CLAUDE.md — never leave `[PLACEHOLDER]` values in place.
- If the project has existing governance (README, CONTRIBUTING.md, etc.), incorporate
  their patterns rather than replacing them.
- The constitution must reflect the actual project state — don't add commands or tools
  the project doesn't use.
- Create the `.gitignore` BEFORE the first commit of governance files.
