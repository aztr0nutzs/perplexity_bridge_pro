#!/usr/bin/env python3
"""
Startup script for Perplexity Bridge.
Handles graceful startup, browser opening, and error handling.
"""

import sys
import os
import time
import logging
import webbrowser
import threading
import subprocess
from pathlib import Path

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)


def check_dependencies():
    """Check if required dependencies are installed."""
    try:
        import fastapi
        import uvicorn
        import httpx
        import pydantic
        import slowapi
        logger.info("✓ All dependencies found")
        return True
    except ImportError as e:
        logger.error(f"✗ Missing dependency: {e.name}")
        logger.error("\nPlease install dependencies:")
        logger.error("  pip install -r requirements.txt")
        return False


def check_config():
    """Check if configuration is valid."""
    try:
        from config import PERPLEXITY_KEY, validate_config
        validate_config()
        logger.info("✓ Configuration valid")
        return True
    except ValueError as e:
        logger.error(f"✗ Configuration error: {e}")
        logger.error("\nPlease set your PERPLEXITY_API_KEY environment variable:")
        logger.error("  Windows: set PERPLEXITY_API_KEY=your_key")
        logger.error("  Linux/Mac: export PERPLEXITY_API_KEY=your_key")
        logger.error("\nOr create a .env file with your API key")
        return False
    except Exception as e:
        logger.error(f"✗ Configuration error: {e}")
        return False


def open_browser(url, delay=2):
    """Open browser after a delay."""
    def _open():
        time.sleep(delay)
        try:
            webbrowser.open(url)
            logger.info(f"✓ Browser opened: {url}")
        except Exception as e:
            logger.warning(f"Could not open browser automatically: {e}")
            logger.info(f"Please open manually: {url}")
    
    thread = threading.Thread(target=_open, daemon=True)
    thread.start()


def start_server():
    """Start the FastAPI server."""
    try:
        import uvicorn
        from config import BRIDGE_SECRET
        
        host = "127.0.0.1"
        port = 7860
        url = f"http://{host}:{port}"
        
        logger.info("=" * 60)
        logger.info("Perplexity Bridge - Starting Server")
        logger.info("=" * 60)
        logger.info(f"Server URL: {url}")
        logger.info(f"UI URL: {url}/")
        logger.info(f"API Key: {BRIDGE_SECRET}")
        logger.info("=" * 60)
        logger.info("\nPress Ctrl+C to stop the server\n")
        
        # Open browser after delay
        open_browser(url)
        
        # Start server
        uvicorn.run(
            "app:app",
            host=host,
            port=port,
            log_level="info",
            access_log=True
        )
        
    except KeyboardInterrupt:
        logger.info("\n\nServer stopped by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"\n✗ Failed to start server: {e}")
        logger.error("\nTroubleshooting:")
        logger.error("  1. Check if port 7860 is available")
        logger.error("  2. Verify all dependencies are installed")
        logger.error("  3. Check the logs above for errors")
        sys.exit(1)


def main():
    """Main entry point."""
    logger.info("Perplexity Bridge - Startup Check")
    logger.info("-" * 60)
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Check configuration
    if not check_config():
        logger.warning("\n⚠ Continuing without API key validation...")
        logger.warning("The server will start but API calls will fail until API key is set.")
        logger.warning("You can set it in the UI settings.\n")
        time.sleep(3)
    
    # Start server
    start_server()


if __name__ == "__main__":
    main()
