#!/bin/bash

echo "========================================="
echo "  Photoshop for Codex Environment Check  "
echo "========================================="
echo ""

# 1. Check Node.js
echo -n "[1/4] Checking Node.js & npx... "
if command -v node >/dev/null 2>&1 && command -v npx >/dev/null 2>&1; then
    NODE_VER=$(node -v)
    NPX_VER=$(npx -v)
    echo "OK ($NODE_VER, npx $NPX_VER)"
else
    echo "FAILED"
    echo "    Error: Node.js or npx is not installed. Please install Node.js from https://nodejs.org/"
    exit 1
fi

# 2. Check OS (macOS is preferred)
echo -n "[2/4] Checking Operating System... "
OS_TYPE=$(uname)
if [ "$OS_TYPE" = "Darwin" ]; then
    echo "OK (macOS)"
else
    echo "WARNING"
    echo "    Notice: Currently, this plugin is optimized for macOS. Windows support is coming soon."
fi

# 3. Check Photoshop Process
echo -n "[3/4] Checking if Adobe Photoshop is running... "
if [ "$OS_TYPE" = "Darwin" ]; then
    PS_RUNNING=$(osascript -e 'application "Adobe Photoshop" is running' 2>/dev/null)
    if [ "$PS_RUNNING" = "true" ]; then
        echo "OK (Photoshop is active)"
    else
        echo "FAILED"
        echo "    Error: Adobe Photoshop is not running. Please open Photoshop and try again."
        exit 1
    fi
else
    # Simple check on other platforms (placeholder)
    echo "SKIPPED (Non-macOS)"
fi

# 4. Check AppleScript / Automation Permissions (macOS only)
if [ "$OS_TYPE" = "Darwin" ]; then
    echo -n "[4/4] Checking macOS Automation Permissions... "
    PS_NAME=$(osascript -e 'tell application "Adobe Photoshop" to get name' 2>/dev/null)
    if [ -n "$PS_NAME" ]; then
        echo "OK (Permission granted)"
    else
        echo "FAILED"
        echo "    Error: Codex or Terminal does not have permission to control Photoshop."
        echo "    Please go to: System Settings -> Privacy & Security -> Automation."
        echo "    Ensure 'Terminal' or 'Codex' is checked under 'Adobe Photoshop'."
        exit 1
    fi
fi

echo ""
echo "🎉 Environment check passed successfully! You are ready to use Photoshop for Codex."
exit 0
