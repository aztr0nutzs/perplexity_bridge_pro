"""
GitHub Copilot API Adapter

Provides integration with GitHub Copilot API for code generation,
chat completions, and agentic workflows.
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
            "Accept": "application/json"
        }
        
        payload = {
            "messages": messages,
            "model": model,
            "stream": stream,
            "max_tokens": max_tokens,
            "temperature": temperature
        }
        
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
        
        Args:
            task: Task description
            tools: Optional list of tools the agent can use
            
        Returns:
            Workflow execution result
        """
        messages = [
            {
                "role": "system",
                "content": "You are a GitHub Copilot agent capable of multi-step task execution. "
                          "Break down complex tasks, use available tools, and provide detailed solutions."
            },
            {"role": "user", "content": task}
        ]
        
        payload = {
            "messages": messages,
            "model": "copilot-agent",
            "max_tokens": 2048
        }
        
        if tools:
            payload["tools"] = tools
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        async with httpx.AsyncClient(timeout=120.0) as client:
            response = await client.post(
                f"{self.base_url}/agent/execute",
                json=payload,
                headers=headers
            )
            response.raise_for_status()
            return response.json()


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
        return data.get("choices", [{}])[0].get("message", {}).get("content", "")
