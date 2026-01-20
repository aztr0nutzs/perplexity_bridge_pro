"""Tests for configuration module."""
import os
import pytest


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
    assert has_github_copilot() == True


def test_has_github_copilot_without_key():
    """Test GitHub Copilot detection without key."""
    if "GITHUB_COPILOT_API_KEY" in os.environ:
        del os.environ["GITHUB_COPILOT_API_KEY"]
    # Re-import to get fresh function
    import importlib
    import config
    importlib.reload(config)
    from config import has_github_copilot
    assert has_github_copilot() == False
