"""Tests for the start.py module."""
import os
import sys
import socket
import pytest
from unittest.mock import patch, MagicMock, Mock
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Set test environment before importing
os.environ["BRIDGE_SECRET"] = "test-secret-key"
os.environ["PERPLEXITY_API_KEY"] = "test-api-key"

import start


class TestCheckDependencies:
    """Tests for check_dependencies function."""
    
    def test_all_dependencies_available(self):
        """Test when all dependencies are available."""
        result = start.check_dependencies()
        assert result is True
    
    def test_missing_dependency(self):
        """Test when a dependency is missing."""
        with patch('builtins.__import__', side_effect=ImportError("fastapi")):
            result = start.check_dependencies()
            assert result is False


class TestCheckConfig:
    """Tests for check_config function."""
    
    def test_valid_config(self):
        """Test with valid configuration."""
        with patch.dict(os.environ, {
            "BRIDGE_SECRET": "test-secret",
            "PERPLEXITY_API_KEY": "test-key"
        }):
            # Reload config to pick up new env vars
            import importlib
            import config
            importlib.reload(config)
            result = start.check_config()
            assert result is True
    
    def test_missing_api_key(self):
        """Test with missing API key."""
        with patch.dict(os.environ, {"PERPLEXITY_API_KEY": ""}, clear=False):
            # Mock the validate_config to raise ValueError
            with patch('config.validate_config', side_effect=ValueError("API key required")):
                result = start.check_config()
                assert result is False
    
    def test_config_exception(self):
        """Test with configuration exception."""
        with patch('config.validate_config', side_effect=Exception("Config error")):
            result = start.check_config()
            assert result is False


class TestOpenBrowser:
    """Tests for open_browser function."""
    
    def test_browser_opens_successfully(self):
        """Test that browser opens successfully."""
        with patch('webbrowser.open') as mock_open:
            with patch('time.sleep'):  # Skip the delay
                start.open_browser("http://localhost:7860", delay=0)
                # Give thread time to execute
                import time
                time.sleep(0.1)
    
    def test_browser_open_fails(self):
        """Test browser open failure is handled gracefully."""
        with patch('webbrowser.open', side_effect=Exception("Browser error")):
            with patch('time.sleep'):
                # Should not raise exception
                start.open_browser("http://localhost:7860", delay=0)
                import time
                time.sleep(0.1)


class TestCheckPortAvailable:
    """Tests for check_port_available function."""
    
    def test_port_available(self):
        """Test when port is available."""
        # Find an available port
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('127.0.0.1', 0))
            port = s.getsockname()[1]
        
        result = start.check_port_available('127.0.0.1', port)
        assert result is True
    
    def test_port_in_use(self):
        """Test when port is already in use."""
        # Create a socket and bind it to a port
        test_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        test_socket.bind(('127.0.0.1', 0))
        test_socket.listen(1)
        port = test_socket.getsockname()[1]
        
        try:
            result = start.check_port_available('127.0.0.1', port)
            assert result is False
        finally:
            test_socket.close()


class TestStartServer:
    """Tests for start_server function."""
    
    def test_server_start_with_port_in_use(self):
        """Test server fails when port is in use."""
        with patch('start.check_port_available', return_value=False):
            with pytest.raises(SystemExit) as exc_info:
                start.start_server()
            assert exc_info.value.code == 1
    
    def test_server_keyboard_interrupt(self):
        """Test server handles keyboard interrupt."""
        with patch('start.check_port_available', return_value=True):
            with patch('start.open_browser'):
                with patch('uvicorn.run', side_effect=KeyboardInterrupt()):
                    with pytest.raises(SystemExit) as exc_info:
                        start.start_server()
                    assert exc_info.value.code == 0
    
    def test_server_start_exception(self):
        """Test server handles start exception."""
        with patch('start.check_port_available', return_value=True):
            with patch('start.open_browser'):
                with patch('uvicorn.run', side_effect=Exception("Server error")):
                    with pytest.raises(SystemExit) as exc_info:
                        start.start_server()
                    assert exc_info.value.code == 1
    
    def test_server_respects_env_vars(self):
        """Test server uses environment variables."""
        with patch('start.check_port_available', return_value=True):
            with patch('start.open_browser'):
                with patch('uvicorn.run', side_effect=KeyboardInterrupt()) as mock_run:
                    with patch.dict(os.environ, {
                        "BRIDGE_HOST": "0.0.0.0",
                        "BRIDGE_PORT": "8080"
                    }):
                        with pytest.raises(SystemExit):
                            start.start_server()
                        
                        # Verify uvicorn was called with correct params
                        mock_run.assert_called_once()
                        call_args = mock_run.call_args[1]
                        assert call_args['host'] == '0.0.0.0'
                        assert call_args['port'] == 8080


class TestMain:
    """Tests for main function."""
    
    def test_main_missing_dependencies(self):
        """Test main exits when dependencies are missing."""
        with patch('start.check_dependencies', return_value=False):
            with pytest.raises(SystemExit) as exc_info:
                start.main()
            assert exc_info.value.code == 1
    
    def test_main_missing_config(self):
        """Test main continues with warning when config is invalid."""
        with patch('start.check_dependencies', return_value=True):
            with patch('start.check_config', return_value=False):
                with patch('time.sleep') as mock_sleep:  # Skip the warning delay
                    with patch('start.start_server'):
                        start.main()
                        # Verify sleep was called for the warning delay
                        mock_sleep.assert_called()
    
    def test_main_success(self):
        """Test main with successful startup."""
        with patch('start.check_dependencies', return_value=True):
            with patch('start.check_config', return_value=True):
                with patch('start.start_server'):
                    start.main()
