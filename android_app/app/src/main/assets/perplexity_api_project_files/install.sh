#!/bin/bash
# Perplexity Bridge - Linux Installation Script
# This script installs dependencies and sets up the application

set -e  # Exit on error

echo "================================================"
echo "Perplexity Bridge - Linux Installation"
echo "================================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "[ERROR] Python 3 is not installed"
    echo "Please install Python 3.8 or higher:"
    echo "  Ubuntu/Debian: sudo apt install python3 python3-pip python3-venv"
    echo "  Fedora: sudo dnf install python3 python3-pip"
    echo "  Arch: sudo pacman -S python python-pip"
    exit 1
fi

echo "[1/4] Checking Python version..."
python3 --version

# Check Python version (must be 3.8+)
PYTHON_VERSION=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d. -f1)
PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d. -f2)

if [ "$PYTHON_MAJOR" -lt 3 ] || ([ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -lt 8 ]); then
    echo "[ERROR] Python 3.8 or higher is required"
    echo "Current version: $PYTHON_VERSION"
    exit 1
fi

echo "[2/4] Creating virtual environment..."
if [ -d "venv" ]; then
    echo "Virtual environment already exists"
else
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo "[WARNING] Failed to create virtual environment, continuing with system Python"
        USE_VENV=0
    else
        echo "Virtual environment created successfully"
        USE_VENV=1
    fi
fi

if [ "$USE_VENV" = "1" ]; then
    echo "[3/4] Activating virtual environment..."
    source venv/bin/activate
fi

echo ""
echo "[4/4] Installing dependencies..."
pip install --upgrade pip > /dev/null 2>&1 || true
pip install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "[ERROR] Failed to install dependencies"
    echo "Please check the error messages above"
    exit 1
fi

echo ""
echo "[5/5] Setting up environment..."
if [ ! -f ".env" ]; then
    cp env.example .env 2>/dev/null || true
    echo "Created .env file - please edit it with your API key"
else
    echo ".env file already exists"
fi

# Make start.sh executable
chmod +x start.sh 2>/dev/null || true

echo ""
echo "================================================"
echo "Installation Complete!"
echo "================================================"
echo ""
echo "Next steps:"
echo "1. Edit .env file and add your PERPLEXITY_API_KEY"
echo "2. Run: ./start.sh"
echo "   Or double-click 'Perplexity Bridge.desktop' launcher"
echo ""
echo "To run manually:"
echo "  source venv/bin/activate  # if using venv"
echo "  python3 start.py"
echo ""
