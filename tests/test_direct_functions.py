"""Direct unit tests for app.py functions to increase coverage."""
import os
import pytest
from unittest.mock import patch, AsyncMock, MagicMock

# Set test environment
os.environ["BRIDGE_SECRET"] = "test-secret-key"
os.environ["PERPLEXITY_API_KEY"] = "test-api-key"

# Now import app module
import app
from app import get_model_provider, get_perplexity_key


class TestDirectFunctionCalls:
    """Direct tests of helper functions."""
    
    def test_get_model_provider_perplexity_models(self):
        """Test get_model_provider for various Perplexity models."""
        assert get_model_provider("gpt-5.2") == "perplexity"
        assert get_model_provider("mistral-7b-instruct") == "perplexity"
        assert get_model_provider("sonar-small-chat") == "perplexity"
        assert get_model_provider("claude-4.5") == "perplexity"
        assert get_model_provider("gemini-3-pro") == "perplexity"
    
    def test_get_model_provider_copilot_models(self):
        """Test get_model_provider for Copilot models."""
        assert get_model_provider("copilot-gpt-4") == "github-copilot"
        assert get_model_provider("copilot-agent") == "github-copilot"
        assert get_model_provider("copilot-anything") == "github-copilot"
    
    def test_get_perplexity_key_with_valid_key(self):
        """Test get_perplexity_key with valid key."""
        with patch('app.PERPLEXITY_KEY', 'test-key-123'):
            key = get_perplexity_key()
            assert key == 'test-key-123'
    
    def test_get_perplexity_key_with_whitespace(self):
        """Test get_perplexity_key strips whitespace."""
        with patch('app.PERPLEXITY_KEY', '  test-key  '):
            key = get_perplexity_key()
            assert key == 'test-key'
    
    def test_get_perplexity_key_none(self):
        """Test get_perplexity_key with None."""
        with patch('app.PERPLEXITY_KEY', None):
            from fastapi import HTTPException
            with pytest.raises(HTTPException) as exc_info:
                get_perplexity_key()
            assert exc_info.value.status_code == 400
    
    def test_get_perplexity_key_empty_string(self):
        """Test get_perplexity_key with empty string."""
        with patch('app.PERPLEXITY_KEY', ''):
            from fastapi import HTTPException
            with pytest.raises(HTTPException) as exc_info:
                get_perplexity_key()
            assert exc_info.value.status_code == 400
    
    def test_get_perplexity_key_whitespace_only(self):
        """Test get_perplexity_key with whitespace only."""
        with patch('app.PERPLEXITY_KEY', '   '):
            from fastapi import HTTPException
            with pytest.raises(HTTPException) as exc_info:
                get_perplexity_key()
            assert exc_info.value.status_code == 400


class TestPerplexityChatFunction:
    """Tests for _perplexity_chat function."""
    
    @pytest.mark.asyncio
    async def test_perplexity_chat_success(self):
        """Test _perplexity_chat with successful response."""
        from app import _perplexity_chat, ChatReq, Message
        
        # Create a valid request
        req = ChatReq(
            model="test-model",
            messages=[Message(role="user", content="test")]
        )
        request_data = {"model": "test-model", "messages": [{"role": "user", "content": "test"}]}
        
        # Mock HTTP response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "id": "test-123",
            "choices": [
                {"message": {"role": "assistant", "content": "response"}}
            ]
        }
        mock_response.raise_for_status = MagicMock()
        
        mock_client = AsyncMock()
        mock_client.post.return_value = mock_response
        mock_client.__aenter__.return_value = mock_client
        mock_client.__aexit__.return_value = None
        
        with patch('httpx.AsyncClient', return_value=mock_client):
            with patch('app.get_perplexity_key', return_value='test-key'):
                result = await _perplexity_chat(req, request_data)
                assert result["id"] == "test-123"
                assert len(result["choices"]) > 0
    
    @pytest.mark.asyncio
    async def test_perplexity_chat_with_error_response(self):
        """Test _perplexity_chat with error in response."""
        from app import _perplexity_chat, ChatReq, Message
        from fastapi import HTTPException
        
        req = ChatReq(
            model="test-model",
            messages=[Message(role="user", content="test")]
        )
        request_data = {"model": "test-model", "messages": []}
        
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "error": {"message": "API error"}
        }
        mock_response.raise_for_status = MagicMock()
        
        mock_client = AsyncMock()
        mock_client.post.return_value = mock_response
        mock_client.__aenter__.return_value = mock_client
        mock_client.__aexit__.return_value = None
        
        with patch('httpx.AsyncClient', return_value=mock_client):
            with patch('app.get_perplexity_key', return_value='test-key'):
                with pytest.raises(HTTPException) as exc_info:
                    await _perplexity_chat(req, request_data)
                assert exc_info.value.status_code == 502
    
    @pytest.mark.asyncio
    async def test_perplexity_chat_missing_choices(self):
        """Test _perplexity_chat with missing choices."""
        from app import _perplexity_chat, ChatReq, Message
        from fastapi import HTTPException
        
        req = ChatReq(
            model="test-model",
            messages=[Message(role="user", content="test")]
        )
        request_data = {}
        
        mock_response = MagicMock()
        mock_response.json.return_value = {"id": "test-123"}  # No choices
        mock_response.raise_for_status = MagicMock()
        
        mock_client = AsyncMock()
        mock_client.post.return_value = mock_response
        mock_client.__aenter__.return_value = mock_client
        mock_client.__aexit__.return_value = None
        
        with patch('httpx.AsyncClient', return_value=mock_client):
            with patch('app.get_perplexity_key', return_value='test-key'):
                with pytest.raises(HTTPException) as exc_info:
                    await _perplexity_chat(req, request_data)
                assert exc_info.value.status_code == 502
    
    @pytest.mark.asyncio
    async def test_perplexity_chat_empty_choices(self):
        """Test _perplexity_chat with empty choices."""
        from app import _perplexity_chat, ChatReq, Message
        from fastapi import HTTPException
        
        req = ChatReq(
            model="test-model",
            messages=[Message(role="user", content="test")]
        )
        request_data = {}
        
        mock_response = MagicMock()
        mock_response.json.return_value = {"id": "test-123", "choices": []}
        mock_response.raise_for_status = MagicMock()
        
        mock_client = AsyncMock()
        mock_client.post.return_value = mock_response
        mock_client.__aenter__.return_value = mock_client
        mock_client.__aexit__.return_value = None
        
        with patch('httpx.AsyncClient', return_value=mock_client):
            with patch('app.get_perplexity_key', return_value='test-key'):
                with pytest.raises(HTTPException) as exc_info:
                    await _perplexity_chat(req, request_data)
                assert exc_info.value.status_code == 502
    
    @pytest.mark.asyncio
    async def test_perplexity_chat_choice_missing_message(self):
        """Test _perplexity_chat with choice missing message field."""
        from app import _perplexity_chat, ChatReq, Message
        from fastapi import HTTPException
        
        req = ChatReq(
            model="test-model",
            messages=[Message(role="user", content="test")]
        )
        request_data = {}
        
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "id": "test-123",
            "choices": [{"index": 0}]  # Missing message
        }
        mock_response.raise_for_status = MagicMock()
        
        mock_client = AsyncMock()
        mock_client.post.return_value = mock_response
        mock_client.__aenter__.return_value = mock_client
        mock_client.__aexit__.return_value = None
        
        with patch('httpx.AsyncClient', return_value=mock_client):
            with patch('app.get_perplexity_key', return_value='test-key'):
                with pytest.raises(HTTPException) as exc_info:
                    await _perplexity_chat(req, request_data)
                assert exc_info.value.status_code == 502


class TestCopilotChatFunction:
    """Tests for _copilot_chat function."""
    
    @pytest.mark.asyncio
    async def test_copilot_chat_not_configured(self):
        """Test _copilot_chat when Copilot is not configured."""
        from app import _copilot_chat, ChatReq, Message
        from fastapi import HTTPException
        
        req = ChatReq(
            model="copilot-gpt-4",
            messages=[Message(role="user", content="test")]
        )
        request_data = {}
        
        with patch('app.has_github_copilot', return_value=False):
            with pytest.raises(HTTPException) as exc_info:
                await _copilot_chat(req, request_data)
            assert exc_info.value.status_code == 400
    
    @pytest.mark.asyncio
    async def test_copilot_chat_success(self):
        """Test _copilot_chat with successful response."""
        from app import _copilot_chat, ChatReq, Message
        
        req = ChatReq(
            model="copilot-gpt-4",
            messages=[Message(role="user", content="test")]
        )
        request_data = {"model": "copilot-gpt-4", "messages": []}
        
        mock_adapter = AsyncMock()
        mock_adapter.chat_completion.return_value = {
            "id": "copilot-123",
            "choices": [{"message": {"role": "assistant", "content": "response"}}]
        }
        
        with patch('app.has_github_copilot', return_value=True):
            with patch('app.CopilotAdapter', return_value=mock_adapter):
                result = await _copilot_chat(req, request_data)
                assert result["id"] == "copilot-123"
