# Lessons Learned — Automation Hub

*Update at the end of every session. Format: numbered, titled, with Context / Lesson / Prevention.*
*Cross-reference with CLAUDE.md Key Patterns — any pattern noted there should have a corresponding lesson here.*

---

## Session: v2 Build (2026-04-30)

### 1. PyGithub v2.x uses Auth.Token() not login_or_token
- **Context**: Initial code used deprecated `Github(login_or_token=token)` which triggered warnings.
- **Lesson**: PyGithub 2.x API requires `Github(auth=Auth.Token(token))` syntax.
- **Prevention**: Always check library version and use current API. Pin versions in requirements.txt.

### 2. claude-agent-sdk query() is async — needs asyncio.run()
- **Context**: First attempt called `query()` synchronously, causing runtime errors.
- **Lesson**: The SDK's `query()` returns an async generator. Entry point needs `asyncio.run()`.
- **Prevention**: Check SDK docs for async patterns before writing the orchestration loop.

### 3. No GitPython — subprocess is simpler and has zero dependencies
- **Context**: Evaluated GitPython for git operations but it added a heavy dependency.
- **Lesson**: For simple git ops (checkout, push, rev-parse), subprocess is lighter and sufficient.
- **Prevention**: Prefer subprocess for simple git commands. Only add GitPython if complex graph operations are needed.

### 4. Workflow must checkout target repo to workspace root, automation-hub to subdirectory
- **Context**: Initial workflow design had both repos side by side, causing path confusion.
- **Lesson**: Target repo at `${{ github.workspace }}` (cwd) and automation-hub at `.automation-hub/` is the cleanest layout.
- **Prevention**: Always use this pattern in workflow.yml. The `--repo-dir` flag defaults to cwd for this reason.

### 5. setting_sources=["project"] loads the target repo's CLAUDE.md automatically
- **Context**: Initially planned to pass CLAUDE.md content manually in the prompt.
- **Lesson**: The SDK's `setting_sources` option loads project-level CLAUDE.md from the cwd automatically.
- **Prevention**: Use `setting_sources=["project"]` and ensure the target repo has CLAUDE.md at root.

---

## Session: Governance Framework (2026-05-02)

### 6. Governance patterns are portable across projects with minimal adaptation
- **Context**: Reviewed nuuance (v5.16, 802 lines) and dAIg (v2.3, 1342 lines) constitutions.
- **Lesson**: 20 reusable governance patterns emerged. The core framework (authority ladder, SACRED workflow, session handoff, lessons learned, decision matrix) transfers directly. Only domain-specific articles and forbidden zone lists need customisation.
- **Prevention**: Maintain the governance template in `templates/governance/` as the canonical source. Update it when patterns evolve in any project.

### 7. Agent definitions emerge naturally from governance steps that are most often skipped
- **Context**: Identified 6 agent personas by looking at which governance steps people skip under time pressure.
- **Lesson**: The highest-value agents automate the steps humans are tempted to skip: session handoff, documentation sync, NFT audits, plan creation.
- **Prevention**: When a governance step is consistently skipped, create an agent for it rather than adding more documentation.
