#!/usr/bin/env python3
"""Automation Hub v2 — autonomous development orchestrator entry point."""

import argparse
import asyncio
import logging
import os
import sys
import tempfile
from pathlib import Path

# Allow `python automation/autonomous_dev.py` to resolve sibling packages
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import git
from dotenv import load_dotenv
from github import Auth, Github

from automation.lib.issue_selection import get_oldest_issue
from automation.lib.prompt_builder import build as build_prompt
from automation.lib.pr_creator import BRANCH_PREFIX, create as create_pr

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
    p.add_argument("--dry-run", action="store_true",
                   help="Print the constructed prompt without calling the SDK")
    p.add_argument("--issue", type=int, default=None, metavar="N",
                   help="Use a specific issue number instead of selecting automatically")
    p.add_argument("--max-turns", type=int, default=50, metavar="N",
                   help="Maximum agent turns before stopping (default: 50)")
    return p.parse_args()


async def run(args: argparse.Namespace) -> None:
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

    with tempfile.TemporaryDirectory(prefix="autonomous-dev-") as tmpdir:
        repo_dir = Path(tmpdir) / "repo"

        # 2. Shallow-clone the target repo onto a feature branch
        log.info("Cloning %s (shallow) …", args.target_repo)
        clone_url = (
            f"https://x-access-token:{github_token}"
            f"@github.com/{args.target_repo}.git"
        )
        local_repo = git.Repo.clone_from(clone_url, repo_dir, depth=1)
        branch_name = f"{BRANCH_PREFIX}{issue.number}"
        local_repo.git.checkout("-b", branch_name)
        log.info("Working on branch %s", branch_name)

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

        log.info("Invoking Claude Agent SDK (max_turns=%d) …", args.max_turns)
        options = ClaudeAgentOptions(
            cwd=str(repo_dir),
            max_turns=args.max_turns,
            permission_mode="acceptEdits",
            setting_sources=["project"],
        )

        initial_sha = local_repo.head.commit.hexsha
        last_summary = ""

        async for message in query(prompt=prompt, options=options):
            if isinstance(message, AssistantMessage):
                for block in message.content:
                    if isinstance(block, TextBlock):
                        last_summary = block.text
            elif isinstance(message, ResultMessage):
                log.info(
                    "Agent finished. Cost: $%.4f", message.total_cost_usd or 0.0
                )

        # 5. Only open a PR if the agent committed something
        if local_repo.head.commit.hexsha == initial_sha:
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
