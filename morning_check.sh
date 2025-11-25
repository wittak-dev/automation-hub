#!/bin/bash
echo "☕ Good Morning! Checking overnight results..."
echo "=============================================="
echo ""

# 1. Check logs
echo "📋 Last 30 lines of orchestrator log:"
tail -30 logs/orchestrator.stdout
echo ""

# 2. Check for new PRs
echo "🔀 New PRs created:"
gh pr list --repo wittak-dev/WhatsAppAnalyser_v2 --search "author:app/github-actions" --limit 3
gh pr list --repo wittak-dev/HealthOS-v2_Replit --search "author:app/github-actions" --limit 3
echo ""

# 3. Check analysis reports
echo "📊 New analysis reports:"
ls -lt analysis/ | head -5
echo ""

# 4. Check weekly report
echo "📈 Weekly report:"
ls -lt reports/ | head -3
echo ""

echo "✅ Morning check complete!"
