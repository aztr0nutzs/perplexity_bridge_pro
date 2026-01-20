
import os
import requests
import logging
from typing import Optional
from requests.exceptions import RequestException, Timeout, ConnectionError

logger = logging.getLogger(__name__)


class RooAdapter:
    """
    Adapter for connecting to the Perplexity Bridge API.
    Supports configurable URL and API key via environment variables.
    """

    def __init__(self, url: Optional[str] = None, api_key: Optional[str] = None, timeout: int = 60):
        """
        Initialize the Roo Adapter.

        Args:
            url: Bridge API URL (defaults to ROO_BRIDGE_URL env var or localhost:7860)
            api_key: API key for authentication (defaults to ROO_BRIDGE_KEY env var or dev-secret)
            timeout: Request timeout in seconds (default: 60)
        """
        self.url = url or os.getenv("ROO_BRIDGE_URL", "http://localhost:7860")
        self.api_key = api_key or os.getenv("ROO_BRIDGE_KEY", "dev-secret")
        self.timeout = timeout
        self.default_model = "mistral-7b-instruct"

        # Ensure URL doesn't end with trailing slash
        self.url = self.url.rstrip('/')

    def query(self, prompt: str, model: Optional[str] = None) -> str:
        """
        Query the bridge API with a prompt.

        Args:
            prompt: The user prompt/question
            model: Model to use (defaults to configured default model)

        Returns:
            Response content from the API

        Raises:
            ValueError: If prompt is empty or invalid
            ConnectionError: If unable to connect to the API
            Timeout: If request times out
            RuntimeError: If API returns an error response
        """
        if not prompt or not prompt.strip():
            raise ValueError("Prompt cannot be empty")

        model = model or self.default_model
        endpoint = f"{self.url}/v1/chat/completions"

        body = {
            "model": model,
            "messages": [{"role": "user", "content": prompt.strip()}]
        }

        headers = {
            "X-API-KEY": self.api_key,
            "Content-Type": "application/json"
        }

        logger.info(f"RooAdapter: Sending request to {endpoint} with model {model}")

        try:
            response = requests.post(
                endpoint,
                headers=headers,
                json=body,
                timeout=self.timeout
            )

            # Check HTTP status
            response.raise_for_status()

            # Parse JSON response
            try:
                data = response.json()
            except ValueError as e:
                logger.error(f"RooAdapter: Invalid JSON response: {e}")
                raise RuntimeError(f"Invalid JSON response from API: {e}")

            # Check for API errors in response
            if "error" in data:
                error_msg = data["error"].get("message", "Unknown API error") if isinstance(data["error"], dict) else str(data["error"])
                logger.error(f"RooAdapter: API error: {error_msg}")
                raise RuntimeError(f"API error: {error_msg}")

            # Validate response structure
            if "choices" not in data or not isinstance(data["choices"], list) or len(data["choices"]) == 0:
                logger.error("RooAdapter: Invalid response format - no choices")
                raise RuntimeError("Invalid response format: no choices returned")

            choice = data["choices"][0]
            if "message" not in choice or "content" not in choice["message"]:
                logger.error("RooAdapter: Invalid response format - missing message content")
                raise RuntimeError("Invalid response format: missing message content")

            content = choice["message"]["content"]
            logger.info("RooAdapter: Successfully received response")
            return content

        except Timeout:
            logger.error(f"RooAdapter: Request timed out after {self.timeout} seconds")
            raise Timeout(f"Request to {endpoint} timed out after {self.timeout} seconds")

        except ConnectionError as e:
            logger.error(f"RooAdapter: Connection error: {e}")
            raise ConnectionError(f"Unable to connect to {endpoint}. Is the server running?") from e

        except requests.exceptions.HTTPError as e:
            logger.error(f"RooAdapter: HTTP error {e.response.status_code}: {e.response.text}")
            error_msg = f"HTTP {e.response.status_code}"
            try:
                error_data = e.response.json()
                if "error" in error_data:
                    error_msg = error_data["error"].get("message", error_msg)
            except Exception:
                pass
            raise RuntimeError(f"API request failed: {error_msg}") from e

        except RequestException as e:
            logger.error(f"RooAdapter: Request error: {e}")
            raise RuntimeError(f"Request failed: {str(e)}") from e

        except Exception as e:
            logger.error(f"RooAdapter: Unexpected error: {e}", exc_info=True)
            raise RuntimeError(f"Unexpected error: {str(e)}") from e
