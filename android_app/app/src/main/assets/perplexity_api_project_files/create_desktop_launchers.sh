#!/bin/bash
# Create desktop launchers for Linux
# This script creates a proper .desktop launcher file

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
DESKTOP_DIR="$HOME/Desktop"
DESKTOP_LAUNCHER="$DESKTOP_DIR/Perplexity Bridge.desktop"

echo "Creating desktop launcher..."

# Get absolute path
START_SCRIPT="$SCRIPT_DIR/start.sh"
ICON_PATH="$SCRIPT_DIR/icon.png"

# Create desktop entry
cat > "$DESKTOP_LAUNCHER" << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=Perplexity Bridge
Comment=Perplexity AI Bridge with Web UI
Exec=sh -c "cd '$SCRIPT_DIR' && ./start.sh"
Path=$SCRIPT_DIR
Icon=$ICON_PATH
Terminal=true
Categories=Network;Internet;Development;
Keywords=perplexity;ai;bridge;api;web;
StartupNotify=true
EOF

# Make executable
chmod +x "$DESKTOP_LAUNCHER"
chmod +x "$START_SCRIPT"

echo "Desktop launcher created at: $DESKTOP_LAUNCHER"
echo ""
echo "You can now:"
echo "  1. Double-click 'Perplexity Bridge' on your desktop"
echo "  2. Or run: ./start.sh"
echo ""

# Try to refresh desktop (GNOME/KDE)
if command -v gio &> /dev/null; then
    gio set "$DESKTOP_LAUNCHER" metadata::trusted true 2>/dev/null || true
fi

echo "Done!"
