#!/usr/bin/env python3
"""
Fix the autonomous developer to handle package.json modifications better.
Instead of asking Claude to return the full file, we'll:
1. Tell Claude to return ONLY the changes needed
2. Apply those changes intelligently to the existing package.json
"""
import sys
import os

# Add the automation directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'automation'))

from autonomous_developer import AutonomousDeveloper

# The prompt needs to be smarter about modifications
NEW_PROMPT_SECTION = '''
CRITICAL INSTRUCTIONS FOR FILE MODIFICATIONS:

For "modify" actions on package.json or similar config files:
- Do NOT return the entire file content
- ONLY return the specific sections that need to be added/changed
- Format as: {"scripts": {"test": "vitest", "new-script": "command"}}
- We will merge this into the existing file

For "modify" actions on code files:
- Return the full content only if the file is < 200 lines
- For larger files, return line ranges to replace: {"start_line": 10, "end_line": 20, "new_content": "..."}
'''

print("Fix identified: package.json modifications need smarter prompting")
print("\nThe issue: Claude is trying to return entire file contents which exceed token limits")
print("\nThe solution: Modify the prompt to ask for ONLY the changes, not full files")
print("\nWould you like me to:")
print("1. Update the autonomous_developer.py prompt to be smarter about modifications")
print("2. Add a special handler for package.json that only requests specific changes")
print("3. Increase max_tokens even further (to 12000+)")
print("\nRecommendation: Option 1 + 2 (smarter prompting)")
