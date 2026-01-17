# Perplexity Bridge - Installation Guide

Simple installation and setup instructions for Windows and Linux.

## Quick Start

### Windows

1. **Double-click `install_windows.bat`**
   - This will check Python, create a virtual environment, and install dependencies

2. **Edit `.env` file**
   - Open `.env` in a text editor
   - Add your `PERPLEXITY_API_KEY=your_key_here`

3. **Launch the application**
   - **Option A**: Double-click `Launch Perplexity Bridge.vbs` (opens silently)
   - **Option B**: Double-click `start.bat` (shows console window)
   - **Option C**: Run `create_desktop_launchers.bat` to create a desktop shortcut

The browser will automatically open to `http://localhost:7860/`

### Linux

1. **Run the installation script**
   ```bash
   chmod +x install.sh
   ./install.sh
   ```

2. **Edit `.env` file**
   ```bash
   nano .env  # or use your preferred editor
   # Add: PERPLEXITY_API_KEY=your_key_here
   ```

3. **Launch the application**
   - **Option A**: Run `./start.sh`
   - **Option B**: Run `./create_desktop_launchers.sh` to create a desktop launcher, then double-click "Perplexity Bridge" on your desktop
   - **Option C**: Right-click `Perplexity Bridge.desktop` and select "Allow Launching"

The browser will automatically open to `http://localhost:7860/`

## Detailed Instructions

### Prerequisites

- **Python 3.8 or higher** - [Download for Windows](https://www.python.org/downloads/) | Install on Linux: `sudo apt install python3 python3-pip python3-venv`
- **Perplexity API Key** - [Get one here](https://www.perplexity.ai/settings/api)

### Installation Steps

#### Windows

1. **Check Python Installation**
   - Open Command Prompt
   - Type `python --version`
   - Should show Python 3.8 or higher
   - If not installed, download from [python.org](https://www.python.org/downloads/)

2. **Run Installation Script**
   - Double-click `install_windows.bat`
   - Follow the prompts
   - Script will:
     - Check Python version
     - Create virtual environment (optional but recommended)
     - Install all dependencies
     - Create `.env` file from template

3. **Configure API Key**
   - Open `.env` file (created in the project folder)
   - Add your API key: `PERPLEXITY_API_KEY=your_key_here`
   - Optionally set `BRIDGE_SECRET=your_secret` (defaults to "dev-secret")

4. **Create Desktop Shortcut** (Optional)
   - Double-click `create_desktop_launchers.bat`
   - A shortcut will be created on your desktop

5. **Launch Application**
   - Double-click `Launch Perplexity Bridge.vbs` (minimal window)
   - Or double-click `start.bat` (shows console)
   - Or use the desktop shortcut if created
   - Browser opens automatically to the UI

#### Linux

1. **Install Python** (if not already installed)
   ```bash
   # Ubuntu/Debian
   sudo apt update
   sudo apt install python3 python3-pip python3-venv
   
   # Fedora
   sudo dnf install python3 python3-pip
   
   # Arch Linux
   sudo pacman -S python python-pip
   ```

2. **Run Installation Script**
   ```bash
   chmod +x install.sh
   ./install.sh
   ```
   The script will:
   - Check Python version
   - Create virtual environment
   - Install all dependencies
   - Create `.env` file from template

3. **Configure API Key**
   ```bash
   nano .env  # or use vim, gedit, etc.
   ```
   Add your API key:
   ```
   PERPLEXITY_API_KEY=your_key_here
   BRIDGE_SECRET=your_secret  # Optional, defaults to "dev-secret"
   ```
   Save and exit (Ctrl+X, then Y, then Enter in nano)

4. **Create Desktop Launcher** (Optional)
   ```bash
   chmod +x create_desktop_launchers.sh
   ./create_desktop_launchers.sh
   ```
   This creates a desktop launcher that can be double-clicked

5. **Launch Application**
   ```bash
   ./start.sh
   ```
   Or double-click the desktop launcher if created.
   
   The browser will automatically open to `http://localhost:7860/`

## Running Without Installation Script

### Windows

```batch
REM Check Python
python --version

REM Install dependencies
pip install -r requirements.txt

REM Create .env file
copy env.example .env
REM Edit .env and add your API key

REM Run
python start.py
```

### Linux

```bash
# Check Python
python3 --version

# Create virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp env.example .env
# Edit .env and add your API key
nano .env

# Run
python3 start.py
```

## Troubleshooting

### "Python is not installed"

**Windows:**
- Download and install from [python.org](https://www.python.org/downloads/)
- Make sure to check "Add Python to PATH" during installation
- Restart your computer after installation

**Linux:**
```bash
sudo apt install python3 python3-pip python3-venv  # Ubuntu/Debian
sudo dnf install python3 python3-pip               # Fedora
```

### "PERPLEXITY_API_KEY environment variable is required"

This warning appears if the API key is not set. The server will still start, but API calls will fail.

**Solution:**
1. Create or edit `.env` file in the project folder
2. Add: `PERPLEXITY_API_KEY=your_key_here`
3. Restart the application

### "Port 7860 is already in use"

Another application is using port 7860.

**Solution:**
- Stop the other application using port 7860
- Or edit `start.py` and change the port number
- Or set environment variable: `PORT=8080` (then update UI connection settings)

### "Module not found" errors

Dependencies are not installed.

**Solution:**
```bash
# Windows
pip install -r requirements.txt

# Linux
pip3 install -r requirements.txt
# Or if using venv:
source venv/bin/activate
pip install -r requirements.txt
```

### Browser doesn't open automatically

The browser opening feature may not work on all systems.

**Solution:**
- Manually open your browser
- Navigate to: `http://localhost:7860/`
- Or click the UI link shown in the console

### Desktop launcher doesn't work (Linux)

Some Linux distributions require trusting desktop files.

**Solution:**
```bash
# Make executable
chmod +x "Perplexity Bridge.desktop"

# Trust the launcher (GNOME)
gio set "Perplexity Bridge.desktop" metadata::trusted true

# Or right-click the .desktop file
# Select "Properties" → "Permissions" → Check "Allow executing file as program"
```

### Virtual environment activation fails

**Windows:**
- Make sure you're running from the project directory
- Try: `venv\Scripts\activate.bat` manually

**Linux:**
- Make sure you're in the project directory
- Try: `source venv/bin/activate` manually

## Configuration

### Environment Variables

Create a `.env` file in the project root with:

```env
# Required: Your Perplexity AI API Key
PERPLEXITY_API_KEY=your_api_key_here

# Optional: Bridge Secret (defaults to "dev-secret")
BRIDGE_SECRET=your_secure_secret_here

# Optional: Roo Adapter Configuration
ROO_BRIDGE_URL=http://localhost:7860
ROO_BRIDGE_KEY=dev-secret
```

### Changing the Port

Edit `start.py` and change:
```python
port = 7860  # Change to your desired port
```

Then update the UI connection settings after launching.

## Uninstalling

Simply delete the project folder. There are no system-wide changes made by the installation scripts.

**To remove dependencies** (if not using virtual environment):
```bash
pip uninstall -r requirements.txt -y
```

**To remove virtual environment:**
```bash
# Windows
rmdir /s venv

# Linux
rm -rf venv
```

## Support

For issues or questions:
- Check the main [README.md](README.md) for more information
- Review the [ROADMAP.md](ROADMAP.md) for known issues
- Check the console output for error messages

## Security Notes

⚠️ **Important:**
- Never commit your `.env` file to version control
- Use a strong `BRIDGE_SECRET` in production
- Keep your `PERPLEXITY_API_KEY` secure and private
- Don't share your API keys publicly
