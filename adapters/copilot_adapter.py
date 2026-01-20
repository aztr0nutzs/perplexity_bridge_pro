"""
GitHub Copilot API Adapter

Provides integration with GitHub Copilot API for code generation,
chat completions, and agentic workflows.

**Important Notes:**
- This adapter implements a standard OpenAI-compatible interface for GitHub Copilot
- Actual endpoint availability depends on your GitHub Copilot subscription and access level
- For production use, you may need to:
  1. Use the official GitHub Copilot SDK (https://github.com/github/copilot-sdk)
  2. Configure organization-specific endpoints
  3. Use proper authentication methods for your tier
- The default base URL assumes standard API access patterns
- Consult GitHub's official Copilot documentation for your specific setup

This implementation provides a flexible adapter that can be configured via
environment variables to work with different GitHub Copilot deployments.
"""

import httpx
import os
from typing import Dict, List, Optional, Any


class CopilotAdapter:
    """
    Adapter for GitHub Copilot API integration.

    Supports:
    - Code completions
    - Chat conversations
    - Agentic workflows
    - Multi-turn sessions
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None
    ):
        """
        Initialize the Copilot adapter.

        Args:
            api_key: GitHub API token with Copilot access. Falls back to GITHUB_COPILOT_API_KEY env var.
            base_url: Base URL for Copilot API. Falls back to GITHUB_COPILOT_BASE_URL env var.
        """
        self.api_key = api_key or os.getenv("GITHUB_COPILOT_API_KEY", "")
        self.base_url = base_url or os.getenv("GITHUB_COPILOT_BASE_URL", "https://api.github.com/copilot")

        if not self.api_key:
            raise ValueError("GitHub Copilot API key is required")

    async def chat_completion(
        self,
        messages: List[Dict[str, str]],
        model: str = "copilot-gpt-4",
        stream: bool = False,
        max_tokens: int = 1024,
        temperature: float = 0.0
    ) -> Dict[str, Any]:
        """
        Send a chat completion request to GitHub Copilot.

        Note: GitHub Copilot API may require specific endpoints or SDK usage.
        This implementation provides a compatible interface that can be adapted
        when official endpoints are available.

        Args:
            messages: List of message objects with 'role' and 'content'
            model: Model identifier
            stream: Whether to stream the response
            max_tokens: Maximum tokens to generate
            temperature: Sampling temperature

        Returns:
            Response from Copilot API in OpenAI-compatible format
        """
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Editor-Version": "vscode/1.80.0",  # Required by some Copilot endpoints
            "Editor-Plugin-Version": "copilot/1.0.0"
        }

        # GitHub Copilot may use OpenAI-compatible format
        payload = {
            "messages": messages,
            "stream": stream,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "n": 1
        }

        # Try standard completions endpoint
        # Note: Actual endpoint may vary based on GitHub Copilot access level
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                f"{self.base_url}/chat/completions",
                json=payload,
                headers=headers
            )
            response.raise_for_status()
            return response.json()

    async def code_completion(
        self,
        prompt: str,
        language: Optional[str] = None,
        max_tokens: int = 500
    ) -> Dict[str, Any]:
        """
        Request code completion from GitHub Copilot.

        Args:
            prompt: Code context/prompt
            language: Programming language hint
            max_tokens: Maximum tokens to generate

        Returns:
            Code completion response
        """
        messages = [
            {"role": "system", "content": f"You are a coding assistant. Language: {language or 'auto-detect'}"},
            {"role": "user", "content": prompt}
        ]

        return await self.chat_completion(
            messages=messages,
            max_tokens=max_tokens,
            temperature=0.2  # Lower temperature for more deterministic code
        )

    async def agent_workflow(
        self,
        task: str,
        tools: Optional[List[Dict[str, Any]]] = None
    ) -> Dict[str, Any]:
        """
        Execute a multi-step agentic workflow.

        Note: This uses the standard chat completions endpoint with enhanced
        system prompts to simulate agentic behavior. Future GitHub Copilot SDK
        may provide dedicated agent endpoints.

        Args:
            task: Task description
            tools: Optional list of tools the agent can use

        Returns:
            Workflow execution result
        """
        messages = [
            {
                "role": "system",
                "content": ("You are a GitHub Copilot agent capable of multi-step task execution. "
                            "Break down complex tasks, provide detailed solutions, and explain your reasoning. "
                            "When appropriate, suggest commands, code, or configuration changes.")
            },
            {"role": "user", "content": task}
        ]

        # Use the standard chat completion with agent-like prompting
        return await self.chat_completion(
            messages=messages,
            model="copilot-gpt-4",  # Use standard Copilot model
            max_tokens=2048,
            temperature=0.3  # Lower temperature for more focused agent-like responses
        )


# Synchronous wrapper for backwards compatibility
class CopilotAdapterSync:
    """Synchronous wrapper for CopilotAdapter."""

    def __init__(self, api_key: Optional[str] = None, base_url: Optional[str] = None):
        import requests
        self.api_key = api_key or os.getenv("GITHUB_COPILOT_API_KEY", "")
        self.base_url = base_url or os.getenv("GITHUB_COPILOT_BASE_URL", "https://api.github.com/copilot")
        self.session = requests.Session()

        if not self.api_key:
            raise ValueError("GitHub Copilot API key is required")

    def query(self, prompt: str, model: str = "copilot-gpt-4") -> str:
        """Simple synchronous query method."""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "messages": [{"role": "user", "content": prompt}],
            "model": model
        }

        response = self.session.post(
            f"{self.base_url}/chat/completions",
            json=payload,
            headers=headers,
            timeout=60
        )
        response.raise_for_status()

        data = response.json()
        choices = data.get("choices", [])
        if not choices:
            return ""
        return choices[0].get("message", {}).get("content", "")
