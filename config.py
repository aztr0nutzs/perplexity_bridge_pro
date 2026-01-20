
import os
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

# Perplexity Configuration
PERPLEXITY_KEY: Optional[str] = os.getenv("PERPLEXITY_API_KEY")
BRIDGE_SECRET: Optional[str] = os.getenv("BRIDGE_SECRET")
BASE_URL: str = os.getenv("PERPLEXITY_BASE_URL", "https://api.perplexity.ai/chat/completions")

# GitHub Copilot Configuration
GITHUB_COPILOT_KEY: Optional[str] = os.getenv("GITHUB_COPILOT_API_KEY")
GITHUB_COPILOT_BASE_URL: str = os.getenv("GITHUB_COPILOT_BASE_URL", "https://api.github.com/copilot")

# Rate Limiting
RATE_LIMIT: str = "10/minute"

# Validate BRIDGE_SECRET on import
if not BRIDGE_SECRET or not BRIDGE_SECRET.strip():
    raise ValueError(
        "BRIDGE_SECRET environment variable is required for security. "
        "Please set it to a strong, unique value in your .env file. "
        "Example: BRIDGE_SECRET=your_secure_random_string_here"
    )


def validate_config() -> None:
    """Validate that all required configuration is present."""
    if not PERPLEXITY_KEY:
        raise ValueError(
            "PERPLEXITY_API_KEY environment variable is required. "
            "Please set it before starting the server."
        )
    if not PERPLEXITY_KEY.strip():
        raise ValueError(
            "PERPLEXITY_API_KEY cannot be empty. "
            "Please provide a valid API key."
        )


def has_github_copilot() -> bool:
    """Check if GitHub Copilot is configured."""
    return bool(GITHUB_COPILOT_KEY and GITHUB_COPILOT_KEY.strip())


# NOTE: Validation is intentionally not run on import so the server can start
# and surface configuration errors at request time.
