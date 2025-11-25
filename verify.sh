#!/bin/bash
echo "🔍 Pre-Sleep Verification"
echo "=========================="
echo ""

# 1. Check orchestrator running
if launchctl list | grep -q automation-hub; then
    echo "✅ Orchestrator is running (launch agent)"
elif [ -f orchestrator.pid ] && ps -p $(cat orchestrator.pid) > /dev/null 2>&1; then
    echo "✅ Orchestrator is running (background process)"
else
    echo "❌ Orchestrator is NOT running"
    echo "   Run: launchctl load ~/Library/LaunchAgents/com.automation-hub.orchestrator.plist"
fi

# 2. Check .env
if grep -q "GITHUB_TOKEN=ghp_" .env && grep -q "ANTHROPIC_API_KEY=sk-ant-" .env; then
    echo "✅ Environment variables set"
else
    echo "❌ Missing API keys in .env"
fi

# 3. Check autonomous_developer.py
if grep -q "Phase 2.1: Roadmap-Aware" automation/autonomous_developer.py; then
    echo "✅ Autonomous developer updated (Phase 2.1)"
else
    echo "⚠️  Autonomous developer may be old version"
fi

# 4. Check config
if grep -q "enabled: true" orchestration_config.yaml; then
    echo "✅ Autonomous development enabled"
else
    echo "❌ Autonomous development is disabled"
    echo "   Edit orchestration_config.yaml"
fi

# 5. Check for issues
WA_ISSUES=$(gh issue list --repo wittak-dev/WhatsAppAnalyser_v2 --state open --limit 1 2>/dev/null | wc -l)
HO_ISSUES=$(gh issue list --repo wittak-dev/HealthOS-v2_Replit --state open --limit 1 2>/dev/null | wc -l)
echo "📋 Open issues: WhatsApp=$WA_ISSUES, HealthOS=$HO_ISSUES"

echo ""
echo "🌙 Status: Ready for 3 AM run"
echo ""
echo "💡 Remember:"
echo "   - Keep Mac awake (don't shut down)"
echo "   - Sleep mode is fine"
echo "   - Check results at 9 AM"
