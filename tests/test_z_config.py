"""Tests for configuration module."""
import os
import pytest


def test_has_github_copilot_with_key():
    """Test GitHub Copilot detection with key."""
    old_key = os.environ.get("GITHUB_COPILOT_API_KEY")
    os.environ["GITHUB_COPILOT_API_KEY"] = "test-key"
    try:
        # Re-import to get fresh function
        from config import has_github_copilot
        # Clear the module cache to force reload
        import importlib
        import config
        importlib.reload(config)
        from config import has_github_copilot
        assert has_github_copilot()
    finally:
        # Restore original state
        if old_key:
            os.environ["GITHUB_COPILOT_API_KEY"] = old_key
        elif "GITHUB_COPILOT_API_KEY" in os.environ:
            del os.environ["GITHUB_COPILOT_API_KEY"]
        # Reload again to restore original state
        import importlib
        import config
        importlib.reload(config)


def test_has_github_copilot_without_key():
    """Test GitHub Copilot detection without key."""
    old_key = os.environ.get("GITHUB_COPILOT_API_KEY")
    if "GITHUB_COPILOT_API_KEY" in os.environ:
        del os.environ["GITHUB_COPILOT_API_KEY"]
    try:
        # Re-import to get fresh function
        import importlib
        import config
        importlib.reload(config)
        from config import has_github_copilot
        assert not has_github_copilot()
    finally:
        # Restore original state
        if old_key:
            os.environ["GITHUB_COPILOT_API_KEY"] = old_key
        # Reload again to restore original state
        import importlib
        import config
        importlib.reload(config)


def test_validate_config_no_key():
    """Test validate_config raises error when no API key is set."""
    old_key = os.environ.get("PERPLEXITY_API_KEY")
    old_secret = os.environ.get("BRIDGE_SECRET")
    try:
        # Need to keep BRIDGE_SECRET for module to load
        os.environ["BRIDGE_SECRET"] = "test-secret"
        if "PERPLEXITY_API_KEY" in os.environ:
            del os.environ["PERPLEXITY_API_KEY"]
        import importlib
        import config
        importlib.reload(config)
        from config import validate_config
        
        with pytest.raises(ValueError, match="PERPLEXITY_API_KEY"):
            validate_config()
    finally:
        # Restore
        if old_key:
            os.environ["PERPLEXITY_API_KEY"] = old_key
        else:
            os.environ["PERPLEXITY_API_KEY"] = "test-api-key"
        if old_secret:
            os.environ["BRIDGE_SECRET"] = old_secret
        # Reload to restore original state
        import importlib
        import config
        importlib.reload(config)


def test_validate_config_empty_key():
    """Test validate_config raises error when API key is empty."""
    old_key = os.environ.get("PERPLEXITY_API_KEY")
    old_secret = os.environ.get("BRIDGE_SECRET")
    try:
        # Need to keep BRIDGE_SECRET for module to load
        os.environ["BRIDGE_SECRET"] = "test-secret"
        os.environ["PERPLEXITY_API_KEY"] = "   "
        import importlib
        import config
        importlib.reload(config)
        from config import validate_config
        
        with pytest.raises(ValueError, match="cannot be empty"):
            validate_config()
    finally:
        # Restore
        if old_key:
            os.environ["PERPLEXITY_API_KEY"] = old_key
        else:
            os.environ["PERPLEXITY_API_KEY"] = "test-api-key"
        if old_secret:
            os.environ["BRIDGE_SECRET"] = old_secret
        # Reload to restore original state
        import importlib
        import config
        importlib.reload(config)
