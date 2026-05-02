#!/usr/bin/env python3
"""Automation Hub v2 — autonomous development orchestrator entry point."""

import argparse
import asyncio
import logging
import os
import subprocess
import sys
from pathlib import Path

# Allow `python automation/autonomous_dev.py` to resolve sibling packages
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from dotenv import load_dotenv
from github import Auth, Github

from automation.lib.issue_selection import get_oldest_issue
from automation.lib.prompt_builder import build as build_prompt
from automation.lib.pr_creator import BRANCH_PREFIX, create as create_pr

if Path(".env").exists():
    load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%dT%H:%M:%S",
)
log = logging.getLogger(__name__)


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Autonomous development orchestrator v2")
    p.add_argument("--target-repo", required=True, metavar="OWNER/REPO",
                   help="GitHub repository slug, e.g. robwhitaker/nuuance")
    p.add_argument("--repo-dir", type=Path, default=None, metavar="PATH",
                   help="Path to the pre-cloned target repo (default: current directory)")
    p.add_argument("--dry-run", action="store_true",
                   help="Print the constructed prompt without calling the SDK")
    p.add_argument("--issue", type=int, default=None, metavar="N",
                   help="Use a specific issue number instead of selecting automatically")
    return p.parse_args()


def _git(args: list[str], cwd: Path) -> str:
    """Run a git command and return stdout. Raises on non-zero exit."""
    return subprocess.run(
        ["git", *args], cwd=cwd, check=True, capture_output=True, text=True
    ).stdout.strip()


async def run(args: argparse.Namespace) -> None:
    repo_dir = args.repo_dir or Path.cwd()
    github_token = os.environ["GITHUB_TOKEN"]
    gh = Github(auth=Auth.Token(github_token))

    # 1. Select issue
    if args.issue:
        issue = gh.get_repo(args.target_repo).get_issue(args.issue)
        log.info("Using specified issue #%d: %s", issue.number, issue.title)
    else:
        issue = get_oldest_issue(gh, args.target_repo)
        if issue is None:
            log.info("No open autonomous-dev issues in %s — nothing to do.", args.target_repo)
            return
        log.info("Selected issue #%d: %s", issue.number, issue.title)

    # 2. Create feature branch in the pre-checked-out repo
    branch_name = f"{BRANCH_PREFIX}{issue.number}"
    _git(["checkout", "-b", branch_name], repo_dir)
    log.info("Working on branch %s in %s", branch_name, repo_dir)

    # 3. Build prompt
    prompt = build_prompt(issue, repo_dir)

    if args.dry_run:
        print("\n" + "=" * 60)
        print("DRY RUN — prompt that would be sent to the Claude Agent SDK:")
        print("=" * 60)
        print()
        print(prompt)
        print()
        print("=" * 60)
        log.info("Dry run complete — no SDK call made.")
        return

    # 4. Invoke Claude Agent SDK
    from claude_agent_sdk import (  # noqa: PLC0415
        AssistantMessage,
        ClaudeAgentOptions,
        ResultMessage,
        TextBlock,
        query,
    )

    log.info("Invoking Claude Agent SDK (max_turns=40) …")
    options = ClaudeAgentOptions(
        cwd=str(repo_dir),
        max_turns=40,
        permission_mode="acceptEdits",
        setting_sources=["project"],
    )

    initial_sha = _git(["rev-parse", "HEAD"], repo_dir)
    last_summary = ""

    try:
        async for message in query(prompt=prompt, options=options):
            if isinstance(message, AssistantMessage):
                for block in message.content:
                    if isinstance(block, TextBlock):
                        last_summary = block.text
            elif isinstance(message, ResultMessage):
                log.info("Agent finished. Cost: $%.4f", message.total_cost_usd or 0.0)
    except Exception as exc:
        log.warning("Agent exited with error: %s", exc)
        log.info("Checking for commits despite error …")

    # 5. Only open a PR if the agent committed something
    if _git(["rev-parse", "HEAD"], repo_dir) == initial_sha:
        log.warning("Agent made no commits on %s — skipping PR.", branch_name)
        return

    # 6. Push and create PR
    log.info("Creating PR …")
    pr_url = create_pr(gh, args.target_repo, issue, repo_dir)
    log.info("PR created: %s", pr_url)
    if last_summary:
        log.info("Agent summary: %.200s", last_summary)


def main() -> None:
    asyncio.run(run(parse_args()))


if __name__ == "__main__":
    main()
