#!/usr/bin/env python3
"""Test the solution format transformation"""

import json
import sys
sys.path.insert(0, 'automation')
from autonomous_developer import AutonomousDeveloper
from pathlib import Path

# Load the actual Claude response
response_file = Path.home() / 'automation-hub' / 'logs' / 'claude_response_1.txt'
raw_solution = json.loads(response_file.read_text())

print("Raw solution keys:", raw_solution.keys())
print("\nChanges count:", len(raw_solution.get('changes', [])))

# Create a dummy instance to test transformation
import os
from dotenv import load_dotenv
load_dotenv()

dev = AutonomousDeveloper(
    github_token=os.getenv('GITHUB_TOKEN'),
    anthropic_api_key=os.getenv('ANTHROPIC_API_KEY')
)

# Test transformation
transformed = dev._transform_solution_format(raw_solution)

print("\n=== TRANSFORMED RESULT ===")
print(f"files_to_create: {len(transformed['files_to_create'])}")
for f in transformed['files_to_create']:
    print(f"  - {f['path']} ({len(f['content'])} chars)")

print(f"\nfiles_to_modify: {len(transformed['files_to_modify'])}")
for f in transformed['files_to_modify']:
    print(f"  - {f['path']} ({len(f['new_content'])} chars)")

print(f"\ntests: {len(transformed['tests'])}")
for f in transformed['tests']:
    print(f"  - {f['path']} ({len(f['content'])} chars)")

print(f"\ncommit_message: {transformed['commit_message'][:80]}...")
print(f"explanation: {transformed['explanation'][:80]}...")

print("\n✅ Transformation successful!")
