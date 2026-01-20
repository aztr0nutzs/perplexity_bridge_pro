"""Tests for configuration module."""
import os
import pytest
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))


def test_has_github_copilot_with_key():
    """Test GitHub Copilot detection with key."""
    os.environ["GITHUB_COPILOT_API_KEY"] = "test-key"
    # Re-import to get fresh function
    from config import has_github_copilot
    # Clear the module cache to force reload
    import importlib
    import config
    importlib.reload(config)
    from config import has_github_copilot
    assert has_github_copilot()


def test_has_github_copilot_without_key():
    """Test GitHub Copilot detection without key."""
    if "GITHUB_COPILOT_API_KEY" in os.environ:
        del os.environ["GITHUB_COPILOT_API_KEY"]
    # Re-import to get fresh function
    import importlib
    import config
    importlib.reload(config)
    from config import has_github_copilot
    assert not has_github_copilot()


def test_has_github_copilot_with_empty_key():
    """Test GitHub Copilot detection with empty key."""
    os.environ["GITHUB_COPILOT_API_KEY"] = "   "
    import importlib
    import config
    importlib.reload(config)
    from config import has_github_copilot
    assert not has_github_copilot()


def test_validate_config_with_valid_key():
    """Test validate_config with valid API key."""
    os.environ["PERPLEXITY_API_KEY"] = "valid-key"
    os.environ["BRIDGE_SECRET"] = "test-secret"
    import importlib
    import config
    importlib.reload(config)
    from config import validate_config
    # Should not raise exception
    validate_config()


def test_validate_config_without_key():
    """Test validate_config without API key."""
    # Save original value
    original_key = os.environ.get("PERPLEXITY_API_KEY")
    try:
        if "PERPLEXITY_API_KEY" in os.environ:
            del os.environ["PERPLEXITY_API_KEY"]
        os.environ["BRIDGE_SECRET"] = "test-secret"
        import importlib
        import config
        importlib.reload(config)
        from config import validate_config
        
        with pytest.raises(ValueError, match="PERPLEXITY_API_KEY environment variable is required"):
            validate_config()
    finally:
        # Restore original value
        if original_key:
            os.environ["PERPLEXITY_API_KEY"] = original_key


def test_validate_config_with_empty_key():
    """Test validate_config with empty API key."""
    os.environ["PERPLEXITY_API_KEY"] = "   "
    os.environ["BRIDGE_SECRET"] = "test-secret"
    import importlib
    import config
    importlib.reload(config)
    from config import validate_config
    
    with pytest.raises(ValueError, match="PERPLEXITY_API_KEY cannot be empty"):
        validate_config()


def test_config_constants():
    """Test that configuration constants are set."""
    os.environ["BRIDGE_SECRET"] = "test-secret"
    os.environ["PERPLEXITY_API_KEY"] = "test-key"
    import importlib
    import config
    importlib.reload(config)
    
    assert config.BASE_URL == "https://api.perplexity.ai/chat/completions"
    assert config.GITHUB_COPILOT_BASE_URL == "https://api.github.com/copilot"
    assert config.RATE_LIMIT == "10/minute"


def test_config_custom_base_url():
    """Test configuration with custom base URL."""
    os.environ["BRIDGE_SECRET"] = "test-secret"
    os.environ["PERPLEXITY_BASE_URL"] = "https://custom.api.com/chat"
    import importlib
    import config
    importlib.reload(config)
    
    assert config.BASE_URL == "https://custom.api.com/chat"
