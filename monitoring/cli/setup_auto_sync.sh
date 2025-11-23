#!/bin/bash
# Setup automatic Obsidian sync for all repositories

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
OBSIDIAN_VAULT="${OBSIDIAN_VAULT_PATH:-/Users/ma/Vault}"

echo "🔧 Setting up automatic Obsidian repository sync"

# 1. Install Python dependencies
echo ""
echo "📦 Checking Python dependencies..."
pip install -q --user PyGithub python-dotenv 2>/dev/null || echo "  (Dependencies may already be installed)"

# 2. Create launchd plist for periodic sync (every 6 hours)
PLIST_PATH="$HOME/Library/LaunchAgents/com.user.obsidian-repo-sync.plist"

cat > "$PLIST_PATH" <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.user.obsidian-repo-sync</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/bin/python3</string>
        <string>$SCRIPT_DIR/repo_sync.py</string>
    </array>
    <key>StartInterval</key>
    <integer>21600</integer>
    <key>StandardOutPath</key>
    <string>/tmp/obsidian-repo-sync.log</string>
    <key>StandardErrorPath</key>
    <string>/tmp/obsidian-repo-sync.err</string>
</dict>
</plist>
EOF

# Load the agent
launchctl unload "$PLIST_PATH" 2>/dev/null || true
launchctl load "$PLIST_PATH"

echo "✓ Created launchd agent (runs every 6 hours)"

# 3. Create git hook for post-commit sync
GIT_HOOKS_DIR="$SCRIPT_DIR/../../.git/hooks"
if [ -d "$GIT_HOOKS_DIR" ]; then
    cat > "$GIT_HOOKS_DIR/post-commit" <<'EOF'
#!/bin/bash
# Auto-sync to Obsidian after commit

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && cd ../.. && pwd)"
python3 "$SCRIPT_DIR/monitoring/cli/repo_sync.py" > /dev/null 2>&1 &
EOF

    chmod +x "$GIT_HOOKS_DIR/post-commit"
    echo "✓ Created post-commit hook for this repo"
fi

# 4. Run initial sync
echo ""
echo "🔄 Running initial sync..."
python3 "$SCRIPT_DIR/repo_sync.py"

# 5. Configure Obsidian Git plugin settings (if plugin exists)
OBSIDIAN_GIT_SETTINGS="$OBSIDIAN_VAULT/.obsidian/plugins/obsidian-git/data.json"
if [ -f "$OBSIDIAN_GIT_SETTINGS" ]; then
    echo ""
    echo "📝 Obsidian Git plugin detected!"
    echo ""
    echo "Recommended settings (in Obsidian):"
    echo "  • Auto pull: Every 10 minutes"
    echo "  • Auto commit: Every 30 minutes"
    echo "  • Auto push: Every 60 minutes"
    echo "  • Pull updates on startup: ON"
else
    echo ""
    echo "💡 Install Obsidian Git plugin for automatic vault syncing:"
    echo "   Settings → Community Plugins → Browse → Search 'Obsidian Git'"
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "Your repositories will now sync to: $OBSIDIAN_VAULT/Repositories/"
echo ""
echo "Sync schedule:"
echo "  • Every 6 hours (automatic via launchd)"
echo "  • After every git commit in this repo"
echo "  • Manual: python3 $SCRIPT_DIR/repo_sync.py"
echo ""
echo "View logs: tail -f /tmp/obsidian-repo-sync.log"
