
import os
from typing import Optional

PERPLEXITY_KEY: Optional[str] = os.getenv("PERPLEXITY_API_KEY")
BRIDGE_SECRET: str = os.getenv("BRIDGE_SECRET", "dev-secret")
BASE_URL: str = "https://api.perplexity.ai/chat/completions"
RATE_LIMIT: str = "10/minute"


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


# Validate configuration on import
validate_config()
