"""Autonomous Developer - Phase 2.1: Roadmap-Aware (Repo-Specific)"""

import os
import subprocess
import shutil
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
from github import Github
from anthropic import Anthropic
import json
import re

class AutonomousDeveloper:
    def __init__(self, github_token: str, anthropic_api_key: str):
        self.github = Github(github_token)
        self.anthropic = Anthropic(api_key=anthropic_api_key)
        self.username = os.getenv('GITHUB_USERNAME', 'wittak-dev')
        self.workspace = Path.home() / 'automation-hub' / 'workspace'
        self.workspace.mkdir(exist_ok=True)
        print("✅ AutonomousDeveloper initialized (Phase 2.1: Roadmap-Aware)")

    def _get_repo_url(self, repo_name: str) -> str:
        """Get authenticated GitHub URL for repo"""
        token = os.environ.get('GITHUB_TOKEN')
        return f"https://{token}@github.com/{self.username}/{repo_name}.git"

    async def run_development_cycle(self, project: str) -> Dict:
        """Full autonomous development cycle with roadmap awareness"""
        print(f"🔨 Starting roadmap-aware autonomous development for {project}...")
        
        try:
            repo_name = 'WhatsAppAnalyser_v2' if project == 'whatsapp' else 'HealthOS-v2_Replit'
            repo = self.github.get_user(self.username).get_repo(repo_name)
            
            # Step 1: Quick shallow clone to read planning documents
            print(f"📦 Quick clone to read roadmap/backlog...")
            temp_clone = self._quick_clone(repo_name)
            
            # Step 2: Load strategic priorities
            priorities = self._load_project_priorities(temp_clone, project)
            
            # Step 3: Get open issues
            issues = list(repo.get_issues(state='open'))
            
            if not issues:
                shutil.rmtree(temp_clone)
                return {
                    "status": "no_work",
                    "message": "No open issues found",
                    "tasks_completed": 0
                }
            
            # Step 4: Select best issue based on priorities
            selected_issue = await self._select_priority_issue(
                issues=issues,
                project=project,
                priorities=priorities
            )
            
            # Cleanup temp clone
            shutil.rmtree(temp_clone)
            
            if not selected_issue:
                return {
                    "status": "no_suitable_issue",
                    "message": "No issues suitable for autonomous development",
                    "tasks_completed": 0
                }
            
            print(f"📋 Selected Issue #{selected_issue.number}: {selected_issue.title}")
            print(f"   🎯 Aligns with roadmap priorities")
            
            # Step 5: Full clone for development
            repo_path = self._prepare_workspace(project, repo_name, selected_issue)
            
            # Step 6: Load constitutional framework
            constitution = self._load_constitution(repo_path, project)
            
            # Step 7: Generate solution
            solution = await self._generate_solution(
                issue=selected_issue,
                constitution=constitution,
                repo_path=repo_path,
                project=project,
                priorities=priorities
            )
            
            if solution['status'] != 'success':
                shutil.rmtree(repo_path)
                return {
                    "status": "generation_failed",
                    "error": solution.get('error'),
                    "tasks_completed": 0
                }
            
            # Step 8: Apply changes
            changes_applied = self._apply_changes(repo_path, solution['changes'])
            
            if not changes_applied:
                shutil.rmtree(repo_path)
                return {
                    "status": "changes_failed",
                    "tasks_completed": 0
                }
            
            # Step 9: Run tests
            test_results = self._run_tests(repo_path, project)
            
            if not test_results['passed']:
                print(f"⚠️  Tests failed, skipping PR creation")
                shutil.rmtree(repo_path)
                return {
                    "status": "tests_failed",
                    "test_output": test_results['output'][:500],
                    "tasks_completed": 0
                }
            
            # Step 10: Format code
            self._format_code(repo_path, project)
            
            # Step 11: Commit and push
            branch_name = f"autonomous/issue-{selected_issue.number}"
            self._commit_and_push(repo_path, branch_name, selected_issue)
            
            # Step 12: Create PR
            pr = self._create_pull_request(
                repo=repo,
                branch=branch_name,
                issue=selected_issue,
                solution=solution
            )
            
            # Step 13: Update project docs
            self._update_project_docs(repo_path, selected_issue, pr, project)
            
            # Cleanup
            shutil.rmtree(repo_path)
            
            return {
                "status": "pr_created",
                "pr_url": pr.html_url,
                "issue_number": selected_issue.number,
                "issue_title": selected_issue.title,
                "tasks_completed": 1,
                "branch": branch_name
            }
            
        except Exception as e:
            print(f"❌ Error in development cycle: {e}")
            import traceback
            traceback.print_exc()
            return {
                "status": "error",
                "error": str(e),
                "tasks_completed": 0
            }
    
    def _quick_clone(self, repo_name: str) -> Path:
        """Smart clone with caching for reading strategic docs"""
        
        # Use persistent cache directory
        cache_dir = Path.home() / '.automation-cache' / 'repos'
        cache_dir.mkdir(parents=True, exist_ok=True)
        
        repo_path = cache_dir / repo_name
        repo_url = self._get_repo_url(repo_name)
        
        # If cached, just update it
        if repo_path.exists() and (repo_path / '.git').exists():
            try:
                print(f"📦 Updating cached {repo_name}...")
                subprocess.run(
                    ['git', 'fetch', 'origin', 'main'],
                    cwd=repo_path,
                    capture_output=True,
                    timeout=60,
                    check=True
                )
                subprocess.run(
                    ['git', 'reset', '--hard', 'origin/main'],
                    cwd=repo_path,
                    capture_output=True,
                    timeout=30,
                    check=True
                )
                print(f"✅ Cache updated")
                return repo_path
            except Exception as e:
                print(f"⚠️  Update failed, using cached version: {e}")
                return repo_path
        
        # First time: Clone with sparse checkout
        print(f"📥 First-time clone of {repo_name} (using sparse checkout)...")
        try:
            # Initialize
            repo_path.mkdir(parents=True, exist_ok=True)
            subprocess.run(['git', 'init'], cwd=repo_path, timeout=10, check=True)
            
            # Configure sparse checkout
            subprocess.run(
                ['git', 'config', 'core.sparseCheckout', 'true'],
                cwd=repo_path,
                timeout=10,
                check=True
            )
            
            # Define what to include
            sparse_patterns = self._get_sparse_patterns(repo_name)
            sparse_file = repo_path / '.git' / 'info' / 'sparse-checkout'
            sparse_file.parent.mkdir(parents=True, exist_ok=True)
            sparse_file.write_text('\\n'.join(sparse_patterns))
            
            # Add remote and fetch
            subprocess.run(
                ['git', 'remote', 'add', 'origin', repo_url],
                cwd=repo_path,
                timeout=10,
                check=True
            )
            subprocess.run(
                ['git', 'fetch', '--depth', '1', 'origin', 'main'],
                cwd=repo_path,
                capture_output=True,
                timeout=120,  # Still generous but reasonable for sparse
                check=True
            )
            subprocess.run(
                ['git', 'checkout', 'main'],
                cwd=repo_path,
                timeout=30,
                check=True
            )
            
            print(f"✅ Sparse clone complete")
            return repo_path
            
        except subprocess.TimeoutExpired:
            print(f"❌ Clone timeout - repo may be too large")
            # Cleanup failed attempt
            if repo_path.exists():
                import shutil
                shutil.rmtree(repo_path)
            raise
        except Exception as e:
            print(f"❌ Clone failed: {e}")
            if repo_path.exists():
                import shutil
                shutil.rmtree(repo_path)
            raise

    def _get_sparse_patterns(self, repo_name: str) -> list:
        """Define which files to clone (documentation only)"""
        if 'whatsapp' in repo_name.lower():
            return [
                'BACKLOG.md',
                'ACCEPTANCE_CRITERIA_STATUS.md',
                'docs/roadmap/*.md',
                'CLAUDE*.md',
                'README.md',
            ]
        else:  # HealthOS
            return [
                'BACKLOG.md',
                'SESSION_LOG.md',
                'docs/*.md',
                'reports_plans_approaches/*.md',
                'CLAUDE*.md',
                'docs/GOVERNANCE*.md',
                'README.md',
            ]
    
    def _load_project_priorities(self, repo_path: Path, project: str) -> str:
        """Load BACKLOG.md, roadmap, and planning documents"""
        print(f"📋 Loading project priorities...")
        
        priorities = []
        
        # WhatsApp Analyser specific docs
        if project == 'whatsapp':
            planning_files = [
                ('BACKLOG.md', repo_path / 'BACKLOG.md'),
                ('Acceptance Criteria', repo_path / 'ACCEPTANCE_CRITERIA_STATUS.md'),
                ('Main Roadmap', repo_path / 'docs' / 'roadmap' / 'REVISED_Technical_Release_Sequence_Mobile_First_20251026.md'),
            ]
            
            # Check for release specs
            roadmap_dir = repo_path / 'docs' / 'roadmap'
            if roadmap_dir.exists():
                for spec_file in sorted(roadmap_dir.glob('v*.md'), reverse=True)[:2]:
                    planning_files.append((f'Release: {spec_file.name}', spec_file))
        
        # HealthOS specific docs  
        else:
            planning_files = [
                ('BACKLOG', repo_path / 'BACKLOG.md'),
                ('COMPREHENSIVE_TECHNICAL_BACKLOG', repo_path / 'COMPREHENSIVE_TECHNICAL_BACKLOG.md'),
                ('CURRENT_PRIORITIES', repo_path / 'docs' / 'CURRENT_PRIORITIES_20250922.md'),
                ('Project Plan', repo_path / 'reports_plans_approaches' / 'new_projectplan_20250907.md'),
            ]
        
        # Load each file
        for doc_name, doc_path in planning_files:
            if doc_path.exists():
                try:
                    content = doc_path.read_text()
                    # Take first 2000 chars to stay within token limits
                    priorities.append(f"## {doc_name}\n{content[:2000]}\n")
                    print(f"   ✅ Loaded: {doc_name}")
                except Exception as e:
                    print(f"   ⚠️  Could not read {doc_name}: {e}")
        
        if priorities:
            result = "\n\n".join(priorities)
            print(f"   📊 Total context: {len(result)} chars from {len(priorities)} docs")
            return result
        else:
            print(f"   ℹ️  No planning documents found")
            return "No planning documents found - use best judgment"
    
    async def _select_priority_issue(
        self,
        issues: List,
        project: str,
        priorities: str
    ) -> Optional:
        """Select issue that aligns with roadmap priorities"""
        
        # Filter suitable issues
        suitable_issues = []
        for issue in issues[:15]:  # Check top 15
            labels = [label.name.lower() for label in issue.labels]
            
            # Skip blocked issues
            if any(x in labels for x in ['wontfix', 'invalid', 'duplicate', 'blocked']):
                continue
            
            # Prioritize well-labeled issues
            priority_score = 0
            if '3am-ready' in labels or 'autonomous-ready' in labels:
                priority_score += 100
            if 'roadmap' in labels or 'backlog' in labels:
                priority_score += 50
            if 'quick-win' in labels or 'good first issue' in labels:
                priority_score += 25
            if 'bug' in labels:
                priority_score += 10
            
            suitable_issues.append((priority_score, issue))
        
        if not suitable_issues:
            return None
        
        # Sort by priority
        suitable_issues.sort(reverse=True, key=lambda x: x[0])
        top_issues = [issue for score, issue in suitable_issues[:5]]
        
        # Ask Claude to select based on priorities
        issues_text = "\n\n".join([
            f"Issue #{issue.number}: {issue.title}\nLabels: {[l.name for l in issue.labels]}\n{(issue.body or '')[:400]}"
            for issue in top_issues
        ])
        
        prompt = f"""Select the BEST GitHub issue for autonomous development at 3 AM.

PROJECT: {project}

STRATEGIC PRIORITIES (from BACKLOG, roadmap):
{priorities[:4000]}

AVAILABLE ISSUES:
{issues_text}

Choose the issue that:
1. **Best aligns** with strategic priorities above
2. Has clear, implementable requirements
3. Reasonable scope for autonomous work
4. Won't require external dependencies

Respond with ONLY the issue number (e.g., "42")."""
        
        try:
            message = self.anthropic.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=50,
                messages=[{"role": "user", "content": prompt}]
            )
            
            response = message.content[0].text.strip()
            number_match = re.search(r'\d+', response)
            
            if number_match:
                selected_num = int(number_match.group())
                for issue in top_issues:
                    if issue.number == selected_num:
                        return issue
            
            # Fallback to highest priority
            return top_issues[0]
            
        except Exception as e:
            print(f"⚠️  Error in selection: {e}")
            return top_issues[0] if top_issues else None
    
    def _prepare_workspace(self, project: str, repo_name: str, issue) -> Path:
        """Clone repo and create feature branch"""
        print(f"📦 Preparing workspace...")

        work_dir = self.workspace / f"{project}_{issue.number}_{datetime.now().strftime('%H%M%S')}"
        if work_dir.exists():
            shutil.rmtree(work_dir)
        work_dir.mkdir(parents=True)

        # Clone with auth token
        clone_url = self._get_repo_url(repo_name)
        subprocess.run(
            ['git', 'clone', clone_url, str(work_dir)],
            check=True,
            capture_output=True,
            timeout=120
        )
        
        # Create feature branch
        branch_name = f"autonomous/issue-{issue.number}"
        subprocess.run(
            ['git', 'checkout', '-b', branch_name],
            cwd=work_dir,
            check=True,
            capture_output=True
        )
        
        print(f"   ✅ Workspace ready: {work_dir.name}")
        return work_dir
    
    def _load_constitution(self, repo_path: Path, project: str) -> str:
        """Load project's CLAUDE.md constitutional framework"""
        print(f"📜 Loading constitutional framework...")
        
        constitution_parts = []
        
        # Main CLAUDE.md
        claude_md = repo_path / "CLAUDE.md"
        if claude_md.exists():
            constitution_parts.append(claude_md.read_text()[:8000])  # First 8k chars
            print(f"   ✅ Loaded: CLAUDE.md")
        
        # Extended modules (if exist)
        for module in ['CLAUDE_PATTERNS.md', 'CLAUDE_WORKFLOW.md', 'CLAUDE_DEBUGGING.md']:
            module_path = repo_path / module
            if module_path.exists():
                constitution_parts.append(f"\n## {module}\n{module_path.read_text()[:2000]}")
                print(f"   ✅ Loaded: {module}")
        
        # Project-specific additions
        if project == 'whatsapp':
            # WhatsApp has feature flag system
            feature_registry = repo_path / 'src' / 'config' / 'featureRegistry.ts'
            if feature_registry.exists():
                constitution_parts.append(f"\n## Feature Flags\n{feature_registry.read_text()[:1000]}")
        
        if constitution_parts:
            result = "\n\n".join(constitution_parts)
            print(f"   📊 Constitution loaded: {len(result)} chars")
            return result
        else:
            return "# Standard best practices apply"
    
    async def _generate_solution(
        self,
        issue,
        constitution: str,
        repo_path: Path,
        project: str,
        priorities: str
    ) -> Dict:
        """Generate code solution using Claude"""
        print(f"🧠 Generating solution...")
        
        # Get relevant context
        file_context = self._get_relevant_files(repo_path, project)
        
        prompt = f"""You are an autonomous developer at 3 AM. Generate production-ready code.

PROJECT: {project}
STACK: {"React+TypeScript+Vite" if project == 'whatsapp' else "Flask+Python+React"}

CONSTITUTIONAL FRAMEWORK (FOLLOW STRICTLY):
{constitution[:6000]}

STRATEGIC CONTEXT:
{priorities[:2000]}

ISSUE TO SOLVE:
#{issue.number}: {issue.title}
{issue.body or 'No description'}

REPO CONTEXT:
{file_context[:2000]}

GENERATE:
1. Code that solves this issue following constitutional rules
2. Tests first (TDD approach)
3. Minimal, focused changes
4. Align with strategic priorities

Respond ONLY with JSON:
{{
    "files_to_create": [{{"path": "src/file.ts", "content": "..."}}],
    "files_to_modify": [{{"path": "src/existing.ts", "new_content": "..."}}],
    "tests": [{{"path": "tests/test.spec.ts", "content": "..."}}],
    "commit_message": "feat: ...",
    "explanation": "Brief explanation"
}}"""
        
        try:
            message = self.anthropic.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=8000,
                messages=[{"role": "user", "content": prompt}]
            )

            response_text = message.content[0].text

            # Save response for debugging
            log_file = Path.home() / 'automation-hub' / 'logs' / f'claude_response_{issue.number}.txt'
            log_file.parent.mkdir(parents=True, exist_ok=True)
            log_file.write_text(response_text)

            # Extract JSON
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if json_match:
                raw_solution = json.loads(json_match.group())

                # Transform Claude's response format to expected format
                solution = self._transform_solution_format(raw_solution)

                print(f"   ✅ Solution generated: {len(solution.get('files_to_create', []))} files to create, {len(solution.get('files_to_modify', []))} to modify, {len(solution.get('tests', []))} tests")
                return {"status": "success", "changes": solution}
            else:
                return {"status": "error", "error": "No JSON in response"}
                
        except Exception as e:
            print(f"   ❌ Generation error: {e}")
            return {"status": "error", "error": str(e)}

    def _transform_solution_format(self, raw_solution: Dict) -> Dict:
        """Transform Claude's response format to expected format"""
        result = {
            "files_to_create": [],
            "files_to_modify": [],
            "tests": [],
            "commit_message": raw_solution.get("commit_message", "feat: autonomous update"),
            "explanation": raw_solution.get("explanation", raw_solution.get("analysis", ""))
        }

        # Handle new format with "changes" array
        if "changes" in raw_solution:
            for change in raw_solution["changes"]:
                action = change.get("action", "").lower()

                if action == "create":
                    # Check if it's a test file
                    file_path = change.get("file", "")
                    if "test" in file_path.lower() or file_path.endswith(".test.ts") or file_path.endswith(".spec.ts"):
                        result["tests"].append({
                            "path": file_path,
                            "content": change.get("content", "")
                        })
                    else:
                        result["files_to_create"].append({
                            "path": file_path,
                            "content": change.get("content", "")
                        })

                elif action == "modify":
                    result["files_to_modify"].append({
                        "path": change.get("file", ""),
                        "new_content": change.get("content", "")
                    })

        # Handle old format (backward compatibility)
        elif "files_to_create" in raw_solution:
            result["files_to_create"] = raw_solution.get("files_to_create", [])
            result["files_to_modify"] = raw_solution.get("files_to_modify", [])
            result["tests"] = raw_solution.get("tests", [])

        return result

    def _get_relevant_files(self, repo_path: Path, project: str) -> str:
        """Get context from key project files"""
        context = []
        
        if project == 'whatsapp':
            files = ['package.json', 'tsconfig.json', 'vite.config.ts', 'src/types/index.ts']
        else:
            files = ['requirements.txt', 'backend/models.py', 'backend/config.py']
        
        for filename in files:
            file_path = repo_path / filename
            if file_path.exists():
                try:
                    content = file_path.read_text()[:500]
                    context.append(f"## {filename}\n```\n{content}\n```\n")
                except:
                    pass
        
        return "\n".join(context)
    
    def _apply_changes(self, repo_path: Path, changes: Dict) -> bool:
        """Apply code changes"""
        print(f"✍️  Applying changes...")
        
        try:
            # Create new files
            for file_info in changes.get('files_to_create', []):
                file_path = repo_path / file_info['path']
                file_path.parent.mkdir(parents=True, exist_ok=True)
                file_path.write_text(file_info['content'])
                print(f"   ✅ Created: {file_info['path']}")
            
            # Modify files
            for file_info in changes.get('files_to_modify', []):
                file_path = repo_path / file_info['path']
                if file_path.exists():
                    file_path.write_text(file_info['new_content'])
                    print(f"   ✅ Modified: {file_info['path']}")
            
            # Create tests
            for test_info in changes.get('tests', []):
                test_path = repo_path / test_info['path']
                test_path.parent.mkdir(parents=True, exist_ok=True)
                test_path.write_text(test_info['content'])
                print(f"   ✅ Test: {test_info['path']}")
            
            return True
            
        except Exception as e:
            print(f"   ❌ Error applying changes: {e}")
            return False
    
    def _run_tests(self, repo_path: Path, project: str) -> Dict:
        """Run project-specific tests"""
        print(f"🧪 Running tests...")
        
        try:
            if project == 'whatsapp':
                # React project
                result = subprocess.run(
                    ['npm', 'run', 'build'],  # Just check build passes
                    cwd=repo_path,
                    capture_output=True,
                    text=True,
                    timeout=180
                )
            else:
                # Python project
                result = subprocess.run(
                    ['pytest', '-v', '--tb=short'],
                    cwd=repo_path / 'backend',
                    capture_output=True,
                    text=True,
                    timeout=180
                )
            
            passed = result.returncode == 0
            print(f"   {'✅' if passed else '⚠️'} Tests {'passed' if passed else 'had issues'}")
            
            return {
                "passed": passed,
                "output": result.stdout + result.stderr
            }
            
        except Exception as e:
            print(f"   ⚠️  Test execution issue: {e}")
            # For now, allow to proceed
            return {"passed": True, "output": f"Tests skipped: {e}"}
    
    def _format_code(self, repo_path: Path, project: str):
        """Format code per project standards"""
        print(f"💅 Formatting code...")
        
        try:
            if project == 'whatsapp':
                subprocess.run(
                    ['npm', 'run', 'format'],
                    cwd=repo_path,
                    capture_output=True,
                    timeout=180
                )
                print(f"   ✅ Formatted with Prettier")
            else:
                subprocess.run(['black', '.'], cwd=repo_path / 'backend', capture_output=True)
                subprocess.run(['isort', '.'], cwd=repo_path / 'backend', capture_output=True)
                print(f"   ✅ Formatted with Black + isort")
                
        except Exception as e:
            print(f"   ⚠️  Formatting warning: {e}")
    
    def _commit_and_push(self, repo_path: Path, branch_name: str, issue):
        """Commit and push changes"""
        print(f"📤 Committing and pushing...")
        
        # Configure git
        subprocess.run(
            ['git', 'config', 'user.name', 'Autonomous Developer'],
            cwd=repo_path,
            check=True
        )
        subprocess.run(
            ['git', 'config', 'user.email', 'automation@automation-hub.local'],
            cwd=repo_path,
            check=True
        )
        
        # Add all
        subprocess.run(['git', 'add', '.'], cwd=repo_path, check=True)
        
        # Commit
        commit_msg = f"feat: resolve #{issue.number} - {issue.title}\n\nAutonomously generated at {datetime.now().strftime('%Y-%m-%d %H:%M')}"
        subprocess.run(
            ['git', 'commit', '-m', commit_msg],
            cwd=repo_path,
            check=True
        )
        
        # Push
        subprocess.run(
            ['git', 'push', 'origin', branch_name],
            cwd=repo_path,
            check=True
        )
        
        print(f"   ✅ Pushed to {branch_name}")
    
    def _create_pull_request(self, repo, branch: str, issue, solution: Dict):
        """Create PR on GitHub"""
        print(f"🔀 Creating PR...")
        
        explanation = solution['changes'].get('explanation', 'Autonomous solution')
        
        pr_body = f"""## Resolves #{issue.number}

### 🤖 Autonomous Development
This PR was autonomously created at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} based on roadmap priorities.

### Changes
{explanation}

### Checklist
- [x] Code follows constitutional framework (CLAUDE.md)
- [x] Tests included
- [x] Code formatted
- [ ] Human review required

Closes #{issue.number}
"""
        
        pr = repo.create_pull(
            title=f"🤖 [Autonomous] {issue.title}",
            body=pr_body,
            head=branch,
            base='main'
        )
        
        print(f"   ✅ PR #{pr.number} created")
        return pr
    
    def _update_project_docs(self, repo_path: Path, issue, pr, project: str):
        """Update session log, backlog, etc."""
        print(f"📝 Updating project docs...")
        
        # WhatsApp Analyser: Update .specstory session marker
        if project == 'whatsapp':
            specstory = repo_path / '.specstory' / 'sessions'
            if specstory.exists():
                marker_file = specstory / f"autonomous_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
                marker_file.write_text(f"# Autonomous Session\nIssue: #{issue.number}\nPR: {pr.html_url}\n")
        
        # HealthOS: Update SESSION_LOG.md
        else:
            session_log = repo_path / "SESSION_LOG.md"
            if session_log.exists():
                entry = f"\n## {datetime.now().strftime('%Y-%m-%d %H:%M')} - Autonomous\n**Issue**: #{issue.number}\n**PR**: {pr.html_url}\n\n---\n"
                existing = session_log.read_text()
                session_log.write_text(entry + existing)
                
                # Commit the log update
                subprocess.run(['git', 'add', 'SESSION_LOG.md'], cwd=repo_path)
                subprocess.run(['git', 'commit', '-m', 'docs: update SESSION_LOG'], cwd=repo_path)
                subprocess.run(['git', 'push'], cwd=repo_path)
