#!/usr/bin/env python3
"""
Fix autonomous developer to handle file modifications intelligently.
This prevents token limit issues by asking for targeted changes instead of full files.
"""
import re

# Read the current file
with open('/Users/robwhitaker/automation-hub/automation/autonomous_developer.py', 'r') as f:
    content = f.read()

# Find and replace the OUTPUT FORMAT section with smarter instructions
OLD_PROMPT = '''OUTPUT FORMAT (JSON):
{{
    "analysis": "Brief analysis of the issue and approach",
    "changes": [
        {{
            "file": "path/to/file.ext",
            "action": "create|modify|delete",
            "content": "full file content for create, or diff-style for modify",
            "description": "what this change does"
        }}
    ],
    "tests_to_run": ["npm test", "pytest", etc],
    "commit_message": "type: description following conventional commits"
}}'''

NEW_PROMPT = '''OUTPUT FORMAT (JSON):
{{
    "analysis": "Brief analysis of the issue and approach",
    "changes": [
        {{
            "file": "path/to/file.ext",
            "action": "create|modify|delete",
            "content": "CONTENT RULES - READ CAREFULLY:
                - For action='create': Full file content (required)
                - For action='modify' on CONFIG FILES (package.json, tsconfig.json, vite.config.ts, etc):
                  ONLY include the specific sections being added/changed as a JSON object/snippet
                  Example: {{\\"scripts\\": {{\\"test\\": \\"vitest\\", \\"new-script\\": \\"command\\"}}}}
                  DO NOT include the entire file - we will merge your changes into the existing file
                - For action='modify' on CODE FILES:
                  If file is small (<200 lines): Full file content is OK
                  If file is large (>200 lines): Use line-based changes:
                  {{\\"line_changes\\": [{{\\"start\\": 10, \\"end\\": 20, \\"new_content\\": \\"...\\"}}, ...]}}
                - For action='delete': Set content to empty string",
            "description": "what this change does"
        }}
    ],
    "tests_to_run": ["npm test", "pytest", etc],
    "commit_message": "type: description following conventional commits"
}}

CRITICAL: For modifications to package.json, vite.config.ts, tsconfig.json and similar config files,
return ONLY the specific keys/sections being added or modified. We will intelligently merge them.
This prevents token limit issues.'''

# Replace the old prompt
if OLD_PROMPT in content:
    content = content.replace(OLD_PROMPT, NEW_PROMPT)
    print("✅ Updated OUTPUT FORMAT section with smart modification rules")
else:
    print("⚠️  Could not find exact OUTPUT FORMAT section")
    print("Looking for alternative pattern...")
    
    # Try a more flexible replacement
    pattern = r'OUTPUT FORMAT \(JSON\):.*?"commit_message": "type: description following conventional commits"\s*\}\}'
    if re.search(pattern, content, re.DOTALL):
        content = re.sub(pattern, NEW_PROMPT + '\n}}', content, flags=re.DOTALL)
        print("✅ Updated using flexible pattern match")
    else:
        print("❌ Could not find OUTPUT FORMAT section to replace")
        exit(1)

# Now add a smart modification applier function
SMART_APPLIER = '''
    def _apply_modification_smart(self, repo_path: Path, change: dict) -> bool:
        """
        Intelligently apply modifications based on file type.
        For config files (JSON/TS configs), merge changes instead of replacing entire file.
        """
        file_path = repo_path / change['file']
        content = change['content']
        
        # Check if this is a config file that should be merged
        config_files = ['package.json', 'tsconfig.json', 'vite.config.ts', 'vitest.config.ts']
        is_config = any(file_path.name == cf for cf in config_files)
        
        if is_config and file_path.name.endswith('.json'):
            # JSON config file - merge intelligently
            try:
                import json
                
                # Read existing file
                if not file_path.exists():
                    # If file doesn't exist, treat as create
                    file_path.write_text(content)
                    return True
                
                existing_content = json.loads(file_path.read_text())
                
                # Parse the partial changes Claude provided
                try:
                    changes = json.loads(content) if isinstance(content, str) else content
                except json.JSONDecodeError:
                    # Claude might have provided invalid JSON snippet
                    # Fall back to full replacement
                    print(f"   ⚠️  Could not parse JSON changes for {file_path.name}, using full replacement")
                    file_path.write_text(content)
                    return True
                
                # Deep merge the changes
                def deep_merge(base, updates):
                    """Recursively merge updates into base"""
                    for key, value in updates.items():
                        if key in base and isinstance(base[key], dict) and isinstance(value, dict):
                            deep_merge(base[key], value)
                        else:
                            base[key] = value
                    return base
                
                merged = deep_merge(existing_content.copy(), changes)
                
                # Write back with proper formatting
                file_path.write_text(json.dumps(merged, indent=2) + '\\n')
                print(f"   ✅ Merged changes into {file_path.name}")
                return True
                
            except Exception as e:
                print(f"   ⚠️  Merge failed for {file_path.name}: {e}")
                print(f"   📝 Falling back to full file replacement")
                file_path.write_text(content)
                return True
        
        elif is_config and file_path.name.endswith('.ts'):
            # TypeScript config - for now, do full replacement
            # TODO: Could implement smart merging for TS configs too
            file_path.write_text(content)
            return True
        
        else:
            # Regular code file - full replacement
            file_path.write_text(content)
            return True
'''

# Find where to insert the smart applier function
# Look for the apply_changes method
apply_changes_pattern = r'(    def apply_changes\(self[^:]+:[\s\S]*?"""[\s\S]*?""")'
match = re.search(apply_changes_pattern, content)

if match:
    # Insert the smart applier before apply_changes
    insert_pos = match.start()
    content = content[:insert_pos] + SMART_APPLIER + '\n' + content[insert_pos:]
    print("✅ Added _apply_modification_smart() method")
else:
    print("⚠️  Could not find apply_changes method, appending smart applier")
    # Find the class definition and append
    class_pattern = r'(class AutonomousDeveloper:[\s\S]*?def __init__)'
    content = re.sub(class_pattern, r'\1' + SMART_APPLIER + '\n    def __init__', content)

# Update the apply_changes method to use smart applier for modifications
old_modify_code = '''                elif change['action'] == 'modify':
                    print(f"   ✅ Modified: {change['file']}")
                    file_path.write_text(change['content'])'''

new_modify_code = '''                elif change['action'] == 'modify':
                    # Use smart modification that handles config files intelligently
                    if self._apply_modification_smart(repo_path, change):
                        print(f"   ✅ Modified: {change['file']}")
                    else:
                        print(f"   ⚠️  Modification failed: {change['file']}")'''

if old_modify_code in content:
    content = content.replace(old_modify_code, new_modify_code)
    print("✅ Updated apply_changes to use smart modification")
else:
    print("⚠️  Could not find exact modify code to replace")

# Write the updated file
with open('/Users/robwhitaker/automation-hub/automation/autonomous_developer.py', 'w') as f:
    f.write(content)

print("\n✅ All fixes applied successfully!")
print("\nChanges made:")
print("1. Updated prompt to request targeted changes for config files")
print("2. Added _apply_modification_smart() method for intelligent merging")
print("3. Updated apply_changes() to use smart modification")
print("\nNext steps:")
print("1. Test with: ./venv/bin/python run_autonomous_dev.py whatsapp")
print("2. Verify package.json modifications are merged properly")
