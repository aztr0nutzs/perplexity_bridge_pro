"""Tests for streaming response functionality."""
import os
import pytest
from unittest.mock import patch, AsyncMock, MagicMock

# Set test environment
os.environ["BRIDGE_SECRET"] = "test-secret-key"
os.environ["PERPLEXITY_API_KEY"] = "test-api-key"

from app import _perplexity_chat, ChatReq, Message


class TestStreamingResponse:
    """Tests for streaming response code paths."""
    
    @pytest.mark.asyncio
    async def test_perplexity_chat_streaming_success(self):
        """Test _perplexity_chat with streaming enabled."""
        req = ChatReq(
            model="test-model",
            messages=[Message(role="user", content="test")],
            stream=True
        )
        request_data = {"model": "test-model", "messages": [], "stream": True}
        
        # Mock streaming response
        class MockStreamResponse:
            status_code = 200
            
            async def aiter_text(self):
                yield "data: chunk1\n\n"
                yield "data: chunk2\n\n"
            
            async def aread(self):
                return b"error data"
            
            async def __aenter__(self):
                return self
            
            async def __aexit__(self, exc_type, exc, tb):
                pass
        
        mock_response = MockStreamResponse()
        
        mock_client = AsyncMock()
        mock_client.stream.return_value = mock_response
        mock_client.__aenter__.return_value = mock_client
        mock_client.__aexit__.return_value = None
        
        with patch('httpx.AsyncClient', return_value=mock_client):
            with patch('app.get_perplexity_key', return_value='test-key'):
                result = await _perplexity_chat(req, request_data)
                # Should return a StreamingResponse
                assert result is not None
    
    @pytest.mark.asyncio
    async def test_perplexity_chat_streaming_error(self):
        """Test _perplexity_chat with streaming API error."""
        req = ChatReq(
            model="test-model",
            messages=[Message(role="user", content="test")],
            stream=True
        )
        request_data = {"model": "test-model", "messages": [], "stream": True}
        
        # Mock streaming response with error
        class MockStreamResponse:
            status_code = 400
            
            async def aiter_text(self):
                # Should not be called
                yield ""
            
            async def aread(self):
                return b"API error occurred"
            
            async def __aenter__(self):
                return self
            
            async def __aexit__(self, exc_type, exc, tb):
                pass
        
        mock_response = MockStreamResponse()
        
        mock_client = AsyncMock()
        mock_client.stream.return_value = mock_response
        mock_client.__aenter__.return_value = mock_client
        mock_client.__aexit__.return_value = None
        
        with patch('httpx.AsyncClient', return_value=mock_client):
            with patch('app.get_perplexity_key', return_value='test-key'):
                result = await _perplexity_chat(req, request_data)
                # Should handle error and return StreamingResponse with error message
                assert result is not None
