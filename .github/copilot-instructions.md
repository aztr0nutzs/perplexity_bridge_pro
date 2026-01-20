# Copilot Agent Onboarding: Perplexity Bridge Pro

## Repo Summary

**Perplexity Bridge Pro** is a FastAPI-based proxy bridge service that connects to the Perplexity AI API. It's a web service application with cross-platform support (Windows/macOS/Linux).

- **Type**: Web service/API proxy + Web UI + VSCode Extension
- **Primary language**: Python 3.8+
- **Framework**: FastAPI with Uvicorn ASGI server
- **Runtime**: Runs locally on port 7860, serves both API endpoints and static web UI
- **Core dependencies**: `fastapi`, `uvicorn`, `httpx`, `pydantic`, `python-dotenv`, `slowapi`, `websockets`

**Mental model**: The app acts as an authenticated, rate-limited proxy layer between clients and Perplexity AI's API. It adds features like WebSocket streaming, a web UI dashboard, rate limiting, and cross-platform tooling (VSCode extension, Python adapter).

**Critical constraint**: Requires `PERPLEXITY_API_KEY` environment variable to make actual API calls (though server starts without it for configuration purposes).

---

## Quickstart (Clean Checkout → Running)

### Prerequisites
- Python 3.8+ (tested with Python 3.12.3)
- Node.js 14+ (only for VSCode extension development, optional)

### Bootstrap & Run (Verified)
```bash
# From repo root
python3 -m pip install -r requirements.txt

# Create .env file (required for API calls)
cp env.example .env
# Edit .env and set: PERPLEXITY_API_KEY=your_key_here

# Verify installation
python3 -c "import fastapi; print('Dependencies OK')"

# Start server
python3 start.py
# Or directly: uvicorn app:app --host 127.0.0.1 --port 7860

# Server starts on http://127.0.0.1:7860
# Web UI served at: http://127.0.0.1:7860/
# API docs at: http://127.0.0.1:7860/docs
```

**Expected behavior**: Server starts, browser auto-opens to UI, logs show startup banner with URL and API key. Server starts even without valid `PERPLEXITY_API_KEY` but API calls will fail.

---

## Verified Build & Validation Commands

### Dependency Installation
**Working directory**: Repo root

```bash
python3 -m pip install -r requirements.txt
```
- **Expected output**: Installs `fastapi`, `uvicorn`, `httpx`, `pydantic`, `python-dotenv`, `slowapi`, `websockets`
- **Time**: ~10-30 seconds on first install
- **Common failure**: Python < 3.8 (requires 3.8+)

### Syntax Check (Python)
**Working directory**: Repo root

```bash
python3 -m py_compile app.py config.py rate_limit.py start.py
echo "Python files compile successfully"
```
- **Expected output**: No output on success, error on syntax issues
- **Time**: < 1 second

### Configuration Validation
**Working directory**: Repo root

```bash
python3 -c "from config import PERPLEXITY_KEY, BRIDGE_SECRET; print('Config loaded')"
```
- **Expected output**: "Config loaded" (or warning about missing API key)
- **Requirement**: `.env` file must exist (create from `env.example`)

### Run Server
**Working directory**: Repo root

```bash
python3 start.py
```
- **Expected output**: Startup banner, "Uvicorn running on http://127.0.0.1:7860"
- **Time**: Starts immediately (< 2 seconds)
- **Note**: Use Ctrl+C to stop

### Test Imports
```bash
python3 -c "import fastapi, uvicorn, httpx, pydantic, slowapi, websockets; print('All imports OK')"
```

### Tests
**Status**: ❌ **No test infrastructure found**
- No `test_*.py` files
- No `tests/` directory
- No test runner configuration (pytest, unittest)
- **Verification**: `find . -name "*test*.py" -o -name "tests" -type d` returns nothing

### Linting/Formatting
**Status**: ⚠️ **Unverified** - No linter config files found
- No `.pylintrc`, `.flake8`, `pyproject.toml` with tool config
- No evidence of `black`, `flake8`, `pylint`, `mypy` usage
- **Note**: Code follows PEP 8 style (per README contribution guidelines) but no automated enforcement

### VSCode Extension Build
**Working directory**: `vscode_extension/`

```bash
# Dependencies already included in node_modules/
# To rebuild (unverified):
# npm install
# vsce package  # requires vsce tool
```
- **Verified**: Pre-built `.vsix` file exists: `perplexity-bridge-1.0.0.vsix`
- **Unverified**: Build process not tested (requires `vsce` tool)

---

## Environment & Tooling

### Required Versions
- **Python**: 3.8+ (tested: 3.12.3)
- **pip**: Included with Python
- **Node.js**: 14+ (only for VSCode extension dev, optional)
- **npm**: 6+ (only for VSCode extension dev, optional)

### Package Manager
- **Python**: `pip` (no `poetry`, `pipenv`, or `conda` config found)
- **Node.js**: `npm` (VSCode extension has `package-lock.json`)

### Version Manager Files
- ❌ No `.python-version`, `.nvmrc`, `.tool-versions`, `Dockerfile`, `docker-compose.yml` found

### Lockfiles
- **Python**: ❌ No `requirements.lock` or `Pipfile.lock` - dependencies use version ranges
- **Node.js**: ✅ `vscode_extension/package-lock.json` exists
- **Rule**: Do not manually edit `package-lock.json`

### Virtual Environment Support
- **Recommended**: Use Python venv (not enforced)
- Installation scripts (`install.sh`, `install_windows.bat`) create venv automatically

### Platform Notes
- **Windows**: Use `install_windows.bat` and `start.bat`
- **Linux/macOS**: Use `install.sh` and `start.sh`
- **Cross-platform**: Python server works on all platforms; desktop launchers are platform-specific

---

## Architecture & Project Layout

### Repo Root Inventory
```
app.py                  # Main FastAPI application (REST + WebSocket endpoints)
config.py               # Environment config loader (PERPLEXITY_API_KEY, etc.)
rate_limit.py           # Rate limiter setup (slowapi)
start.py                # Startup script with health checks, browser launcher
requirements.txt        # Python dependencies
env.example             # Environment variable template

install.sh              # Linux/macOS installer script
install_windows.bat     # Windows installer script
start.sh                # Linux/macOS startup script
start.bat               # Windows startup script (console)
Launch Perplexity Bridge.vbs  # Windows silent launcher

README.md               # Comprehensive documentation
INSTALL.md              # Installation guide
```

### Key Directories
```
ui/                     # Web UI files
  perplex_index2.html   # Main web dashboard (served at /)
  assets/               # Static assets (images, etc.)

adapters/
  roo_adapter.py        # Python client library for bridge API

vscode_extension/       # VSCode extension
  extension.js          # Extension entry point
  package.json          # Extension manifest
  node_modules/         # Dependencies (pre-installed)
  perplexity-bridge-1.0.0.vsix  # Pre-built extension package

assets/                 # Shared assets
  per_api_header.png    # Header image

android_app/            # Android app (separate project, not active)

agent/                  # (Purpose unclear, may be experimental)
```

### Entry Points
- **Web server**: `python3 start.py` or `uvicorn app:app --host 0.0.0.0 --port 7860`
- **API entry**: `app.py` - FastAPI app instance
- **Web UI**: Served at `/` → `ui/perplex_index2.html`

### Configuration Locations
- **Environment**: `.env` (create from `env.example`)
- **API config**: `config.py` (loads from `.env`)
- **Rate limit**: `RATE_LIMIT = "10/minute"` in `config.py`
- **Server host/port**: `start.py` (default: `127.0.0.1:7860`)

### Where to Add New Code
- **New API endpoints**: `app.py` (add routes)
- **New config**: `config.py` + `env.example`
- **New UI features**: `ui/perplex_index2.html`
- **New Python utilities**: Create new `.py` file in root or new subdir
- **Tests**: ❌ No test directory exists - create `tests/` if adding tests

---

## CI / Validation Pipelines

**Status**: ❌ **No CI configured**

- No `.github/workflows/` directory
- No GitHub Actions, Jenkins, CircleCI, or other CI config
- No pre-commit hooks configured
- No automated checks enforced

**Implication**: All validation must be done manually before pushing:
1. Test Python syntax: `python3 -m py_compile *.py`
2. Test imports: `python3 -c "import app, config, rate_limit, start"`
3. Start server to verify runtime: `python3 start.py` (Ctrl+C to stop)
4. Test with actual API key if making API-related changes

**Local validation checklist** (recommended):
- [ ] Python files compile without syntax errors
- [ ] Server starts without crashes
- [ ] Dependencies install cleanly from `requirements.txt`
- [ ] `.env` configuration loads correctly

---

## Known Gotchas & Footguns

### 1. Missing API Key Warning
**Symptom**: Server starts but shows warning: `"PERPLEXITY_API_KEY environment variable is required"`

**Cause**: `.env` file missing or `PERPLEXITY_API_KEY` not set

**Fix**:
```bash
cp env.example .env
# Edit .env and add: PERPLEXITY_API_KEY=your_actual_key
```

**Note**: Server intentionally allows startup without valid key (for UI configuration), but API calls will fail.

### 2. Port 7860 Already in Use
**Symptom**: `"Port 7860 is already in use"`

**Cause**: Another instance running or port occupied

**Fix**:
- Stop existing instance: `pkill -f "uvicorn app:app"`
- Or change port: Set `BRIDGE_PORT=8080` in `.env` or environment
- Or edit `start.py` line 97: `port = int(os.getenv("BRIDGE_PORT", "7860"))`

### 3. Module Import Errors After Fresh Clone
**Symptom**: `ModuleNotFoundError: No module named 'fastapi'`

**Cause**: Dependencies not installed

**Fix**: `python3 -m pip install -r requirements.txt`

### 4. Browser Doesn't Auto-Open
**Symptom**: Server starts but browser doesn't open

**Cause**: `webbrowser` module may not work on headless systems or some environments

**Workaround**: Manually open `http://127.0.0.1:7860` - not a critical failure

### 5. __pycache__ and .env in Git
**Symptom**: `__pycache__/` directories or `.env` committed to repo

**Cause**: No `.gitignore` file in original repo

**Fix**: Add `.gitignore` with:
```
__pycache__/
*.pyc
.env
venv/
node_modules/
```

### 6. VSCode Extension Not Loading
**Symptom**: Extension doesn't work after installation

**Cause**: Bridge server not running or incorrect URL in settings

**Fix**:
- Ensure server is running: `python3 start.py`
- Check VSCode settings: `perplexityBridge.url` = `http://localhost:7860`
- Check API key: `perplexityBridge.apiKey` = value from `.env` `BRIDGE_SECRET`

### 7. CORS Issues in Production
**Symptom**: Browser console errors about CORS when accessing from different domain

**Cause**: `allow_origins=["*"]` in `app.py` is permissive (line 66)

**Note**: For production, change to specific origins: `allow_origins=["https://yourdomain.com"]`

### 8. Rate Limiting Too Strict/Loose
**Symptom**: Too many "429 Too Many Requests" errors or insufficient rate limiting

**Fix**: Edit `config.py` line 11: `RATE_LIMIT = "10/minute"` (change to your needs)

---

## Agent Operating Rules

### Strict Behavior Rules

1. **Trust this document first**. Only search the codebase if information is missing or contradicts this guide.

2. **Inspect before editing**. Before making changes:
   - Identify relevant files (use grep/glob if needed)
   - Understand dependencies and imports
   - Check for related configuration in `config.py` or `.env`

3. **Make minimal changes**. Smallest possible diff to satisfy requirements:
   - Edit only files directly related to the task
   - Don't refactor unrelated code
   - Don't add features not explicitly requested

4. **No breaking existing behavior** unless explicitly required by the change request:
   - Don't remove working endpoints or features
   - Don't change default configurations without reason
   - Test that server still starts after changes

5. **Always run validation** before proposing changes:
   ```bash
   # Syntax check
   python3 -m py_compile <modified_files>.py
   
   # Import check
   python3 -c "import app, config"
   
   # Runtime check (manual stop with Ctrl+C)
   python3 start.py
   ```

6. **If blocked** (missing secrets, external dependencies):
   - **State clearly**: What is missing (e.g., "Real PERPLEXITY_API_KEY needed to test API calls")
   - **State what was validated**: "Server starts, syntax is correct, imports work"
   - **State what cannot be verified**: "Cannot test actual Perplexity API responses without valid key"

7. **Environment files**: Never commit `.env` to repo. Always use `env.example` as template.

8. **No tests to run**: This repo has no test infrastructure. Validate changes by:
   - Running the server
   - Testing manually in the web UI at `http://localhost:7860`
   - Using curl to test API endpoints (if needed)

9. **Documentation updates**: If changing API behavior or configuration:
   - Update relevant sections in `README.md`
   - Update `env.example` if adding new env vars
   - Update `INSTALL.md` if changing installation steps

10. **Commit and push hygiene**:
    - Don't commit `__pycache__/`, `.env`, `venv/`, `node_modules/`
    - Use `.gitignore` to exclude build artifacts
    - Use `report_progress` to commit changes, not direct `git` commands

---

**Document version**: Initial (verified 2026-01-19)
**Verification status**: All commands tested on Python 3.12.3, Ubuntu environment
