#!/bin/bash
# minimal_setup.sh - Just what's missing

set -e

echo "🔧 Completing automation hub setup..."

# 1. Add missing dependencies to requirements.txt
echo "📦 Adding missing dependencies..."
cat >> requirements.txt << 'EOF'

# Additional dependencies for orchestrator
python-dateutil==2.8.2
python-dotenv==1.0.0
EOF

# 2. Install updated requirements
echo "📥 Installing all dependencies..."
pip install -r requirements.txt

# 3. Verify installation
echo "🔍 Verifying imports..."
python -c "
import yaml
import schedule
import requests
import slack_sdk
import jinja2
from dateutil import parser
from dotenv import load_dotenv
print('✅ All dependencies verified')
"

# 4. Create stub modules (automation/ directory)
echo "🔨 Creating stub modules..."
mkdir -p automation

cat > automation/autonomous_developer.py << 'EOF'
"""Autonomous Developer - Stub Implementation"""

class AutonomousDeveloper:
    def __init__(self, github_token, anthropic_api_key):
        self.github_token = github_token
        self.api_key = anthropic_api_key
        print("✅ AutonomousDeveloper initialized (stub)")
    
    async def run_development_cycle(self, project):
        print(f"🔨 Would run development cycle for {project} (stub)")
        return {"status": "simulated", "tasks_completed": 0}
EOF

cat > automation/weekly_progress_generator.py << 'EOF'
"""Weekly Progress Generator - Stub Implementation"""

class ProgressReportGenerator:
    def __init__(self, github_token):
        self.github_token = github_token
        print("✅ ProgressReportGenerator initialized (stub)")
    
    def generate_weekly_report(self):
        print("📊 Would generate weekly report (stub)")
        return {"report": "stub", "status": "simulated"}
EOF

cat > automation/partnership_tracker.py << 'EOF'
"""Partnership Tracker - Stub Implementation"""

class PartnershipTracker:
    def __init__(self):
        print("✅ PartnershipTracker initialized (stub)")
    
    def check_partnerships(self):
        print("🤝 Would check partnerships (stub)")
        return {"status": "simulated", "active": 0}
EOF

cat > automation/legal_doc_generator.py << 'EOF'
"""Legal Document Generator - Stub Implementation"""

class LegalDocumentGenerator:
    def __init__(self):
        print("✅ LegalDocumentGenerator initialized (stub)")
    
    def generate_document(self, template):
        print(f"📄 Would generate {template} document (stub)")
        return {"status": "simulated", "document": "stub"}
EOF

# 5. Create minimal config
echo "⚙️  Creating orchestration_config.yaml..."
cat > orchestration_config.yaml << 'EOF'
# Master Orchestration Configuration

project_paths:
  whatsapp_analyser: /Users/robwhitaker/projects/whatsapp-analyzer
  healthos: /Users/robwhitaker/projects/healthos

automation_schedule:
  autonomous_development:
    enabled: false
    time: "03:00"
    days: [monday, tuesday, wednesday, thursday, friday]
  
  health_monitoring:
    enabled: true
    interval_minutes: 30

notification_preferences:
  daily_summary: false
  critical_alerts: false
  weekly_reports: false
  partnership_updates: false
  deployment_notifications: false

monitoring_thresholds:
  test_coverage_min: 80
  accessibility_score_min: 100
  build_time_max: 300
  error_rate_max: 0.05
  response_time_max: 1000
EOF

# 6. Create .env if doesn't exist
echo "🔐 Creating .env file..."
if [ ! -f .env ]; then
  cat > .env << 'EOF'
# API Keys
GITHUB_TOKEN=your_github_token_here
ANTHROPIC_API_KEY=your_anthropic_key_here

# Slack (optional)
SLACK_WEBHOOK_URL=
SLACK_BOT_TOKEN=

# Email (optional)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
EMAIL_USERNAME=
EMAIL_PASSWORD=
FROM_EMAIL=
TO_EMAILS=

# Environment
ENVIRONMENT=development
EOF
  echo "⚠️  Please edit .env with your actual credentials"
else
  echo "ℹ️  .env already exists, skipping"
fi

# 7. Update .gitignore
echo "📝 Updating .gitignore..."
if [ ! -f .gitignore ]; then
  touch .gitignore
fi

# Add entries if they don't exist
grep -qxF '.env' .gitignore || echo '.env' >> .gitignore
grep -qxF '*.log' .gitignore || echo '*.log' >> .gitignore
grep -qxF 'logs/' .gitignore || echo 'logs/' >> .gitignore
grep -qxF 'dashboard.html' .gitignore || echo 'dashboard.html' >> .gitignore
grep -qxF '__pycache__/' .gitignore || echo '__pycache__/' >> .gitignore
grep -qxF '*.pyc' .gitignore || echo '*.pyc' >> .gitignore
grep -qxF '.pytest_cache/' .gitignore || echo '.pytest_cache/' >> .gitignore

echo ""
echo "✅ Setup complete!"
echo ""
echo "📋 Summary of what was added:"
echo "  • python-dateutil (date handling)"
echo "  • python-dotenv (.env file loading)"
echo "  • Stub modules (autonomous_developer, etc.)"
echo "  • orchestration_config.yaml"
echo "  • .env template"
echo "  • .gitignore entries"
echo ""
echo "🎯 Next steps:"
echo "  1. Edit .env with your API credentials"
echo "  2. Update project paths in orchestration_config.yaml"
echo "  3. Run: python automation/master_orchestrator.py --test-mode"