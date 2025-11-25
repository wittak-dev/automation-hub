#!/usr/bin/env python3
"""
CLI wrapper for running autonomous developer manually
"""
import asyncio
import sys
import os
from pathlib import Path
from dotenv import load_dotenv

# Add automation directory to path
automation_dir = Path(__file__).parent / 'automation'
sys.path.insert(0, str(automation_dir))

from autonomous_developer import AutonomousDeveloper

def main():
    # Load environment variables
    env_path = Path.home() / 'automation-hub' / '.env'
    load_dotenv(env_path)
    
    # Get credentials
    github_token = os.getenv('GITHUB_TOKEN')
    anthropic_api_key = os.getenv('ANTHROPIC_API_KEY')
    
    if not github_token or not anthropic_api_key:
        print("❌ ERROR: Missing credentials in .env file")
        print("   Required: GITHUB_TOKEN and ANTHROPIC_API_KEY")
        sys.exit(1)
    
    # Get project from command line
    if len(sys.argv) < 2:
        print("Usage: python run_autonomous_dev.py <project>")
        print("  project: 'whatsapp' or 'healthos'")
        sys.exit(1)
    
    project = sys.argv[1].lower()
    if project not in ['whatsapp', 'healthos', 'whatsapp-analyser']:
        print(f"❌ ERROR: Unknown project '{project}'")
        print("   Valid options: 'whatsapp' or 'healthos'")
        sys.exit(1)
    
    # Normalize project name
    if project == 'whatsapp-analyser':
        project = 'whatsapp'
    
    print("╔════════════════════════════════════════════════════════════╗")
    print(f"║  🚀 AUTONOMOUS DEVELOPER - {project.upper():30s}         ║")
    print("╚════════════════════════════════════════════════════════════╝")
    print()
    
    # Create developer
    print("📋 Initializing autonomous developer...")
    developer = AutonomousDeveloper(github_token, anthropic_api_key)
    
    # Run development cycle
    print(f"🔨 Starting development cycle for {project}...")
    print()
    
    result = asyncio.run(developer.run_development_cycle(project))
    
    print()
    print("╔════════════════════════════════════════════════════════════╗")
    print("║  ✅ DEVELOPMENT CYCLE COMPLETE                             ║")
    print("╚════════════════════════════════════════════════════════════╝")
    print()
    print(f"📊 Result: {result}")
    
    return 0

if __name__ == '__main__':
    sys.exit(main())
