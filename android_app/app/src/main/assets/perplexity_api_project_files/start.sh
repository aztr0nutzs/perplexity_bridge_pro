#!/bin/bash
# Perplexity Bridge - Linux Launcher
# This script starts the Perplexity Bridge server and opens the browser

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    echo "Activating virtual environment..."
    source venv/bin/activate
fi

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "[ERROR] Python 3 is not installed"
    echo "Please run install.sh first"
    exit 1
fi

# Start the server
python3 start.py
