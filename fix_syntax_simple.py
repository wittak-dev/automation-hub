#!/usr/bin/env python3
"""Fix the syntax error in autonomous_developer.py"""

import re

file_path = '/Users/robwhitaker/automation-hub/automation/autonomous_developer.py'

# Read the file
with open(file_path, 'r') as f:
    content = f.read()

# Fix the broken string literals
# Pattern: + '\n followed by ') on next line
# Should be: + '\n')

# Method 1: Direct replacement of the exact problematic lines
content = content.replace(
    "file_path.write_text(json.dumps(merged, indent=2) + '\n')",
    'file_path.write_text(json.dumps(merged, indent=2) + "\\n")'
)

# Also need to handle case where it's already split
content = re.sub(
    r"json\.dumps\(merged, indent=2\) \+ '\n'\)",
    r'json.dumps(merged, indent=2) + "\\n")',
    content
)

# Write back
with open(file_path, 'w') as f:
    f.write(content)

print("✅ Fixed syntax error!")

# Test import
try:
    import sys
    sys.path.insert(0, '/Users/robwhitaker/automation-hub/automation')
    from autonomous_developer import AutonomousDeveloper
    print("✅ Import successful - fix verified!")
except SyntaxError as e:
    print(f"❌ Still has syntax error: {e}")
    exit(1)
except Exception as e:
    print(f"⚠️  Import error (may be normal): {e}")
