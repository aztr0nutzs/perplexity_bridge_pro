"""Tests for the copilot_adapter module."""
import os
import pytest
from unittest.mock import patch, AsyncMock, MagicMock, Mock
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from adapters.copilot_adapter import CopilotAdapter, CopilotAdapterSync


class TestCopilotAdapterInit:
    """Tests for CopilotAdapter initialization."""
    
    def test_init_with_api_key(self):
        """Test initialization with provided API key."""
        adapter = CopilotAdapter(api_key="test-key")
        assert adapter.api_key == "test-key"
        assert adapter.base_url == "https://api.github.com/copilot"
    
    def test_init_with_env_var(self):
        """Test initialization with environment variable."""
        with patch.dict(os.environ, {"GITHUB_COPILOT_API_KEY": "env-key"}):
            adapter = CopilotAdapter()
            assert adapter.api_key == "env-key"
    
    def test_init_without_api_key(self):
        """Test initialization fails without API key."""
        with patch.dict(os.environ, {}, clear=True):
            with pytest.raises(ValueError, match="GitHub Copilot API key is required"):
                CopilotAdapter()
    
    def test_init_with_custom_base_url(self):
        """Test initialization with custom base URL."""
        adapter = CopilotAdapter(
            api_key="test-key",
            base_url="https://custom.api.com"
        )
        assert adapter.base_url == "https://custom.api.com"
    
    def test_init_with_env_base_url(self):
        """Test initialization with environment variable base URL."""
        with patch.dict(os.environ, {
            "GITHUB_COPILOT_API_KEY": "test-key",
            "GITHUB_COPILOT_BASE_URL": "https://env.api.com"
        }):
            adapter = CopilotAdapter()
            assert adapter.base_url == "https://env.api.com"


class TestCopilotAdapterChatCompletion:
    """Tests for chat_completion method."""
    
    @pytest.mark.asyncio
    async def test_chat_completion_success(self):
        """Test successful chat completion."""
        adapter = CopilotAdapter(api_key="test-key")
        
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "id": "test-id",
            "choices": [{"message": {"content": "Hello!"}}]
        }
        mock_response.raise_for_status = MagicMock()
        
        with patch('httpx.AsyncClient') as mock_client_class:
            mock_client = AsyncMock()
            mock_client.post.return_value = mock_response
            mock_client.__aenter__.return_value = mock_client
            mock_client.__aexit__.return_value = None
            mock_client_class.return_value = mock_client
            
            result = await adapter.chat_completion(
                messages=[{"role": "user", "content": "Hi"}]
            )
            
            assert result["id"] == "test-id"
            mock_client.post.assert_called_once()
            call_args = mock_client.post.call_args
            assert "chat/completions" in call_args[0][0]
    
    @pytest.mark.asyncio
    async def test_chat_completion_with_params(self):
        """Test chat completion with custom parameters."""
        adapter = CopilotAdapter(api_key="test-key")
        
        mock_response = MagicMock()
        mock_response.json.return_value = {"id": "test"}
        mock_response.raise_for_status = MagicMock()
        
        with patch('httpx.AsyncClient') as mock_client_class:
            mock_client = AsyncMock()
            mock_client.post.return_value = mock_response
            mock_client.__aenter__.return_value = mock_client
            mock_client.__aexit__.return_value = None
            mock_client_class.return_value = mock_client
            
            await adapter.chat_completion(
                messages=[{"role": "user", "content": "Test"}],
                model="copilot-gpt-4",
                stream=True,
                max_tokens=500,
                temperature=0.7
            )
            
            call_args = mock_client.post.call_args
            payload = call_args[1]['json']
            assert payload['stream'] is True
            assert payload['max_tokens'] == 500
            assert payload['temperature'] == 0.7
    
    @pytest.mark.asyncio
    async def test_chat_completion_with_headers(self):
        """Test chat completion includes proper headers."""
        adapter = CopilotAdapter(api_key="test-key")
        
        mock_response = MagicMock()
        mock_response.json.return_value = {"id": "test"}
        mock_response.raise_for_status = MagicMock()
        
        with patch('httpx.AsyncClient') as mock_client_class:
            mock_client = AsyncMock()
            mock_client.post.return_value = mock_response
            mock_client.__aenter__.return_value = mock_client
            mock_client.__aexit__.return_value = None
            mock_client_class.return_value = mock_client
            
            await adapter.chat_completion(
                messages=[{"role": "user", "content": "Test"}]
            )
            
            call_args = mock_client.post.call_args
            headers = call_args[1]['headers']
            assert "Bearer test-key" in headers['Authorization']
            assert headers['Content-Type'] == "application/json"
            assert "Editor-Version" in headers


class TestCopilotAdapterCodeCompletion:
    """Tests for code_completion method."""
    
    @pytest.mark.asyncio
    async def test_code_completion_basic(self):
        """Test basic code completion."""
        adapter = CopilotAdapter(api_key="test-key")
        
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "choices": [{"message": {"content": "def hello():\n    print('Hi')"}}]
        }
        mock_response.raise_for_status = MagicMock()
        
        with patch('httpx.AsyncClient') as mock_client_class:
            mock_client = AsyncMock()
            mock_client.post.return_value = mock_response
            mock_client.__aenter__.return_value = mock_client
            mock_client.__aexit__.return_value = None
            mock_client_class.return_value = mock_client
            
            result = await adapter.code_completion(prompt="def hello():")
            
            assert "choices" in result
            mock_client.post.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_code_completion_with_language(self):
        """Test code completion with language hint."""
        adapter = CopilotAdapter(api_key="test-key")
        
        mock_response = MagicMock()
        mock_response.json.return_value = {"choices": []}
        mock_response.raise_for_status = MagicMock()
        
        with patch('httpx.AsyncClient') as mock_client_class:
            mock_client = AsyncMock()
            mock_client.post.return_value = mock_response
            mock_client.__aenter__.return_value = mock_client
            mock_client.__aexit__.return_value = None
            mock_client_class.return_value = mock_client
            
            await adapter.code_completion(
                prompt="print hello",
                language="python",
                max_tokens=100
            )
            
            call_args = mock_client.post.call_args
            payload = call_args[1]['json']
            # Should use lower temperature for code
            assert payload['temperature'] == 0.2
            assert payload['max_tokens'] == 100


class TestCopilotAdapterAgentWorkflow:
    """Tests for agent_workflow method."""
    
    @pytest.mark.asyncio
    async def test_agent_workflow_basic(self):
        """Test basic agent workflow."""
        adapter = CopilotAdapter(api_key="test-key")
        
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "choices": [{"message": {"content": "Task completed"}}]
        }
        mock_response.raise_for_status = MagicMock()
        
        with patch('httpx.AsyncClient') as mock_client_class:
            mock_client = AsyncMock()
            mock_client.post.return_value = mock_response
            mock_client.__aenter__.return_value = mock_client
            mock_client.__aexit__.return_value = None
            mock_client_class.return_value = mock_client
            
            result = await adapter.agent_workflow(task="Write a hello world script")
            
            assert "choices" in result
            mock_client.post.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_agent_workflow_with_tools(self):
        """Test agent workflow with tools."""
        adapter = CopilotAdapter(api_key="test-key")
        
        mock_response = MagicMock()
        mock_response.json.return_value = {"choices": []}
        mock_response.raise_for_status = MagicMock()
        
        with patch('httpx.AsyncClient') as mock_client_class:
            mock_client = AsyncMock()
            mock_client.post.return_value = mock_response
            mock_client.__aenter__.return_value = mock_client
            mock_client.__aexit__.return_value = None
            mock_client_class.return_value = mock_client
            
            tools = [{"name": "file_search", "description": "Search files"}]
            result = await adapter.agent_workflow(
                task="Find config files",
                tools=tools
            )
            
            call_args = mock_client.post.call_args
            payload = call_args[1]['json']
            # Should use agent-appropriate settings
            assert payload['max_tokens'] == 2048
            assert payload['temperature'] == 0.3


class TestCopilotAdapterSync:
    """Tests for CopilotAdapterSync class."""
    
    def test_sync_init_with_api_key(self):
        """Test synchronous adapter initialization with API key."""
        with patch('requests.Session'):
            adapter = CopilotAdapterSync(api_key="test-key")
            assert adapter.api_key == "test-key"
            assert adapter.base_url == "https://api.github.com/copilot"
    
    def test_sync_init_without_api_key(self):
        """Test synchronous adapter initialization fails without API key."""
        with patch.dict(os.environ, {}, clear=True):
            with patch('requests.Session'):
                with pytest.raises(ValueError, match="GitHub Copilot API key is required"):
                    CopilotAdapterSync()
    
    def test_sync_query_success(self):
        """Test synchronous query method."""
        with patch('requests.Session') as mock_session_class:
            mock_session = MagicMock()
            mock_response = MagicMock()
            mock_response.json.return_value = {
                "choices": [{"message": {"content": "Hello response"}}]
            }
            mock_response.raise_for_status = MagicMock()
            mock_session.post.return_value = mock_response
            mock_session_class.return_value = mock_session
            
            adapter = CopilotAdapterSync(api_key="test-key")
            result = adapter.query("Hello")
            
            assert result == "Hello response"
            mock_session.post.assert_called_once()
    
    def test_sync_query_with_model(self):
        """Test synchronous query with custom model."""
        with patch('requests.Session') as mock_session_class:
            mock_session = MagicMock()
            mock_response = MagicMock()
            mock_response.json.return_value = {
                "choices": [{"message": {"content": "Response"}}]
            }
            mock_response.raise_for_status = MagicMock()
            mock_session.post.return_value = mock_response
            mock_session_class.return_value = mock_session
            
            adapter = CopilotAdapterSync(api_key="test-key")
            result = adapter.query("Test", model="custom-model")
            
            call_args = mock_session.post.call_args
            payload = call_args[1]['json']
            assert payload['model'] == "custom-model"
    
    def test_sync_query_empty_response(self):
        """Test synchronous query with empty response."""
        with patch('requests.Session') as mock_session_class:
            mock_session = MagicMock()
            mock_response = MagicMock()
            mock_response.json.return_value = {"choices": [{"message": {}}]}
            mock_response.raise_for_status = MagicMock()
            mock_session.post.return_value = mock_response
            mock_session_class.return_value = mock_session
            
            adapter = CopilotAdapterSync(api_key="test-key")
            result = adapter.query("Test")
            
            # Should return empty string when no content
            assert result == ""
