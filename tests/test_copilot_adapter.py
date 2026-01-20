"""Tests for GitHub Copilot adapter."""
import os
import pytest
from unittest.mock import patch, MagicMock, AsyncMock
import httpx


@pytest.fixture
def mock_api_key():
    """Set up mock API key."""
    old_key = os.environ.get("GITHUB_COPILOT_API_KEY")
    os.environ["GITHUB_COPILOT_API_KEY"] = "test-copilot-key"
    yield "test-copilot-key"
    if old_key:
        os.environ["GITHUB_COPILOT_API_KEY"] = old_key
    else:
        if "GITHUB_COPILOT_API_KEY" in os.environ:
            del os.environ["GITHUB_COPILOT_API_KEY"]


def test_copilot_adapter_init_with_key(mock_api_key):
    """Test CopilotAdapter initialization with API key."""
    from adapters.copilot_adapter import CopilotAdapter
    
    adapter = CopilotAdapter(api_key="explicit-key")
    assert adapter.api_key == "explicit-key"


def test_copilot_adapter_init_from_env(mock_api_key):
    """Test CopilotAdapter initialization from environment."""
    from adapters.copilot_adapter import CopilotAdapter
    
    adapter = CopilotAdapter()
    assert adapter.api_key == "test-copilot-key"


def test_copilot_adapter_init_no_key():
    """Test CopilotAdapter raises error without API key."""
    from adapters.copilot_adapter import CopilotAdapter
    
    # Clear env var
    old_key = os.environ.get("GITHUB_COPILOT_API_KEY")
    if "GITHUB_COPILOT_API_KEY" in os.environ:
        del os.environ["GITHUB_COPILOT_API_KEY"]
    
    with pytest.raises(ValueError, match="GitHub Copilot API key is required"):
        CopilotAdapter()
    
    # Restore
    if old_key:
        os.environ["GITHUB_COPILOT_API_KEY"] = old_key


def test_copilot_adapter_custom_base_url(mock_api_key):
    """Test CopilotAdapter with custom base URL."""
    from adapters.copilot_adapter import CopilotAdapter
    
    adapter = CopilotAdapter(base_url="https://custom.api.com")
    assert adapter.base_url == "https://custom.api.com"


@pytest.mark.asyncio
async def test_chat_completion_success(mock_api_key):
    """Test successful chat completion."""
    from adapters.copilot_adapter import CopilotAdapter
    
    # Mock response
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "id": "test-id",
        "choices": [{"message": {"role": "assistant", "content": "test response"}}]
    }
    mock_response.raise_for_status = MagicMock()
    
    # Mock httpx client
    mock_client = AsyncMock()
    mock_client.post.return_value = mock_response
    mock_client.__aenter__.return_value = mock_client
    mock_client.__aexit__.return_value = None
    
    with patch('httpx.AsyncClient', return_value=mock_client):
        adapter = CopilotAdapter()
        result = await adapter.chat_completion(
            messages=[{"role": "user", "content": "test"}],
            model="copilot-gpt-4"
        )
        
        assert result["id"] == "test-id"
        assert "choices" in result
        
        # Verify correct endpoint was called
        mock_client.post.assert_called_once()
        call_args = mock_client.post.call_args
        assert "chat/completions" in call_args[0][0]


@pytest.mark.asyncio
async def test_chat_completion_with_streaming(mock_api_key):
    """Test chat completion with streaming enabled."""
    from adapters.copilot_adapter import CopilotAdapter
    
    mock_response = MagicMock()
    mock_response.json.return_value = {"id": "test-id"}
    mock_response.raise_for_status = MagicMock()
    
    mock_client = AsyncMock()
    mock_client.post.return_value = mock_response
    mock_client.__aenter__.return_value = mock_client
    mock_client.__aexit__.return_value = None
    
    with patch('httpx.AsyncClient', return_value=mock_client):
        adapter = CopilotAdapter()
        result = await adapter.chat_completion(
            messages=[{"role": "user", "content": "test"}],
            stream=True
        )
        
        # Verify stream parameter was passed
        call_args = mock_client.post.call_args
        assert call_args[1]["json"]["stream"] is True


@pytest.mark.asyncio
async def test_chat_completion_http_error(mock_api_key):
    """Test chat completion handles HTTP errors."""
    from adapters.copilot_adapter import CopilotAdapter
    
    mock_client = AsyncMock()
    mock_client.post.side_effect = httpx.HTTPStatusError(
        "Error", request=MagicMock(), response=MagicMock()
    )
    mock_client.__aenter__.return_value = mock_client
    mock_client.__aexit__.return_value = None
    
    with patch('httpx.AsyncClient', return_value=mock_client):
        adapter = CopilotAdapter()
        with pytest.raises(httpx.HTTPStatusError):
            await adapter.chat_completion(
                messages=[{"role": "user", "content": "test"}]
            )


@pytest.mark.asyncio
async def test_code_completion(mock_api_key):
    """Test code completion functionality."""
    from adapters.copilot_adapter import CopilotAdapter
    
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "id": "test-id",
        "choices": [{"message": {"role": "assistant", "content": "def hello(): pass"}}]
    }
    mock_response.raise_for_status = MagicMock()
    
    mock_client = AsyncMock()
    mock_client.post.return_value = mock_response
    mock_client.__aenter__.return_value = mock_client
    mock_client.__aexit__.return_value = None
    
    with patch('httpx.AsyncClient', return_value=mock_client):
        adapter = CopilotAdapter()
        result = await adapter.code_completion(
            prompt="write a hello function",
            language="python",
            max_tokens=500
        )
        
        assert "choices" in result
        
        # Verify temperature was set appropriately for code
        call_args = mock_client.post.call_args
        assert call_args[1]["json"]["temperature"] == 0.2


@pytest.mark.asyncio
async def test_code_completion_no_language(mock_api_key):
    """Test code completion without language specified."""
    from adapters.copilot_adapter import CopilotAdapter
    
    mock_response = MagicMock()
    mock_response.json.return_value = {"id": "test-id", "choices": []}
    mock_response.raise_for_status = MagicMock()
    
    mock_client = AsyncMock()
    mock_client.post.return_value = mock_response
    mock_client.__aenter__.return_value = mock_client
    mock_client.__aexit__.return_value = None
    
    with patch('httpx.AsyncClient', return_value=mock_client):
        adapter = CopilotAdapter()
        result = await adapter.code_completion(prompt="write code")
        
        # Verify it still works without language
        assert "id" in result


@pytest.mark.asyncio
async def test_agent_workflow(mock_api_key):
    """Test agentic workflow execution."""
    from adapters.copilot_adapter import CopilotAdapter
    
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "id": "test-id",
        "choices": [{"message": {"role": "assistant", "content": "workflow result"}}]
    }
    mock_response.raise_for_status = MagicMock()
    
    mock_client = AsyncMock()
    mock_client.post.return_value = mock_response
    mock_client.__aenter__.return_value = mock_client
    mock_client.__aexit__.return_value = None
    
    with patch('httpx.AsyncClient', return_value=mock_client):
        adapter = CopilotAdapter()
        result = await adapter.agent_workflow(
            task="complete this task",
            tools=[{"name": "search", "type": "function"}]
        )
        
        assert "choices" in result
        
        # Verify max_tokens was set higher for agent workflows
        call_args = mock_client.post.call_args
        assert call_args[1]["json"]["max_tokens"] == 2048


@pytest.mark.asyncio
async def test_agent_workflow_no_tools(mock_api_key):
    """Test agentic workflow without tools."""
    from adapters.copilot_adapter import CopilotAdapter
    
    mock_response = MagicMock()
    mock_response.json.return_value = {"id": "test-id", "choices": []}
    mock_response.raise_for_status = MagicMock()
    
    mock_client = AsyncMock()
    mock_client.post.return_value = mock_response
    mock_client.__aenter__.return_value = mock_client
    mock_client.__aexit__.return_value = None
    
    with patch('httpx.AsyncClient', return_value=mock_client):
        adapter = CopilotAdapter()
        result = await adapter.agent_workflow(task="simple task")
        
        assert "id" in result


def test_copilot_adapter_sync_init(mock_api_key):
    """Test synchronous adapter initialization."""
    from adapters.copilot_adapter import CopilotAdapterSync
    
    adapter = CopilotAdapterSync(api_key="test-key")
    assert adapter.api_key == "test-key"


def test_copilot_adapter_sync_no_key():
    """Test synchronous adapter requires API key."""
    from adapters.copilot_adapter import CopilotAdapterSync
    
    old_key = os.environ.get("GITHUB_COPILOT_API_KEY")
    if "GITHUB_COPILOT_API_KEY" in os.environ:
        del os.environ["GITHUB_COPILOT_API_KEY"]
    
    with pytest.raises(ValueError, match="GitHub Copilot API key is required"):
        CopilotAdapterSync()
    
    if old_key:
        os.environ["GITHUB_COPILOT_API_KEY"] = old_key


def test_copilot_adapter_sync_query(mock_api_key):
    """Test synchronous adapter query method."""
    from adapters.copilot_adapter import CopilotAdapterSync
    
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "choices": [{"message": {"content": "test response"}}]
    }
    mock_response.raise_for_status = MagicMock()
    
    with patch('requests.Session.post', return_value=mock_response):
        adapter = CopilotAdapterSync()
        result = adapter.query("test prompt")
        
        assert result == "test response"


def test_copilot_adapter_sync_query_empty_response(mock_api_key):
    """Test synchronous adapter handles empty response."""
    from adapters.copilot_adapter import CopilotAdapterSync
    
    mock_response = MagicMock()
    mock_response.json.return_value = {"choices": []}
    mock_response.raise_for_status = MagicMock()
    
    with patch('requests.Session.post', return_value=mock_response):
        adapter = CopilotAdapterSync()
        result = adapter.query("test prompt")
        
        assert result == ""


def test_copilot_adapter_sync_custom_base_url(mock_api_key):
    """Test synchronous adapter with custom base URL."""
    from adapters.copilot_adapter import CopilotAdapterSync
    
    adapter = CopilotAdapterSync(base_url="https://custom.url")
    assert adapter.base_url == "https://custom.url"
