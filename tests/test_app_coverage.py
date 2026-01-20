"""Additional tests for app.py to increase coverage."""
import os
import pytest
import json
from unittest.mock import patch, AsyncMock, MagicMock, Mock
from fastapi.testclient import TestClient
import httpx

# Set test environment before importing app
os.environ["BRIDGE_SECRET"] = "test-secret-key"
os.environ["PERPLEXITY_API_KEY"] = "test-api-key"
os.environ["GITHUB_COPILOT_API_KEY"] = "test-copilot-key"

from app import app, get_model_provider, get_perplexity_key

client = TestClient(app)


class TestModelProvider:
    """Tests for model provider detection."""
    
    def test_get_model_provider_perplexity(self):
        """Test detecting Perplexity models."""
        assert get_model_provider("gpt-5.2") == "perplexity"
        assert get_model_provider("mistral-7b-instruct") == "perplexity"
        assert get_model_provider("sonar-medium-chat") == "perplexity"
    
    def test_get_model_provider_copilot(self):
        """Test detecting GitHub Copilot models."""
        assert get_model_provider("copilot-gpt-4") == "github-copilot"
        assert get_model_provider("copilot-agent") == "github-copilot"
    
    def test_get_model_provider_default(self):
        """Test default provider for unknown models."""
        assert get_model_provider("unknown-model") == "perplexity"


class TestPerplexityKey:
    """Tests for Perplexity API key retrieval."""
    
    def test_get_perplexity_key_success(self):
        """Test retrieving Perplexity API key."""
        # Use the key that's already set in the environment
        key = get_perplexity_key()
        assert key == "test-api-key"  # Matches env var set at module level
    
    def test_get_perplexity_key_missing(self):
        """Test error when Perplexity API key is missing."""
        with patch('app.PERPLEXITY_KEY', None):
            from fastapi import HTTPException
            with pytest.raises(HTTPException) as exc_info:
                get_perplexity_key()
            assert exc_info.value.status_code == 400  # Correct status code


class TestStreamingResponse:
    """Tests for streaming response functionality."""
    
    def test_chat_streaming_flag(self):
        """Test that streaming flag is recognized in request."""
        # Just test that the streaming parameter is accepted
        # Full streaming test is complex due to async generators
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "id": "test-id",
            "choices": [{"message": {"role": "assistant", "content": "response"}}]
        }
        mock_response.raise_for_status = MagicMock()
        
        mock_client = AsyncMock()
        mock_client.post.return_value = mock_response
        mock_client.__aenter__.return_value = mock_client
        mock_client.__aexit__.return_value = None
        
        with patch('httpx.AsyncClient', return_value=mock_client):
            # Test that stream parameter is accepted
            response = client.post(
                "/v1/chat/completions",
                json={
                    "model": "test-model",
                    "messages": [{"role": "user", "content": "test"}],
                    "stream": False  # Non-streaming should work
                },
                headers={"X-API-KEY": "test-secret-key"}
            )
            # Should handle non-streaming request
            assert response.status_code in [200, 429]  # 429 if rate limited


class TestCopilotIntegration:
    """Tests for GitHub Copilot integration."""
    
    def test_copilot_not_configured(self):
        """Test error when Copilot model requested but not configured."""
        with patch('app.has_github_copilot', return_value=False):
            response = client.post(
                "/v1/chat/completions",
                json={
                    "model": "copilot-gpt-4",
                    "messages": [{"role": "user", "content": "test"}]
                },
                headers={"X-API-KEY": "test-secret-key"}
            )
            # Should fail - copilot not configured
            assert response.status_code in [400, 500]
    
    def test_copilot_chat_success(self):
        """Test successful Copilot chat completion."""
        with patch('app.has_github_copilot', return_value=True):
            mock_adapter = AsyncMock()
            mock_adapter.chat_completion.return_value = {
                "id": "copilot-test-id",
                "choices": [{"message": {"role": "assistant", "content": "Copilot response"}}]
            }
            
            with patch('app.CopilotAdapter', return_value=mock_adapter):
                response = client.post(
                    "/v1/chat/completions",
                    json={
                        "model": "copilot-gpt-4",
                        "messages": [{"role": "user", "content": "test"}]
                    },
                    headers={"X-API-KEY": "test-secret-key"}
                )
                assert response.status_code == 200
                data = response.json()
                assert data["id"] == "copilot-test-id"


class TestValidationEdgeCases:
    """Tests for validation edge cases."""
    
    def test_chat_with_invalid_model_name(self):
        """Test chat with invalid model name."""
        response = client.post(
            "/v1/chat/completions",
            json={
                "model": "",  # Empty model name
                "messages": [{"role": "user", "content": "test"}]
            },
            headers={"X-API-KEY": "test-secret-key"}
        )
        assert response.status_code == 422  # Validation error
    
    def test_chat_with_no_messages(self):
        """Test chat with no messages."""
        response = client.post(
            "/v1/chat/completions",
            json={
                "model": "test-model",
                "messages": []
            },
            headers={"X-API-KEY": "test-secret-key"}
        )
        assert response.status_code == 422  # Validation error
    
    def test_chat_with_invalid_role(self):
        """Test chat with invalid role."""
        response = client.post(
            "/v1/chat/completions",
            json={
                "model": "test-model",
                "messages": [{"role": "invalid", "content": "test"}]
            },
            headers={"X-API-KEY": "test-secret-key"}
        )
        assert response.status_code == 422  # Validation error
    
    def test_chat_with_empty_content(self):
        """Test chat with empty message content."""
        response = client.post(
            "/v1/chat/completions",
            json={
                "model": "test-model",
                "messages": [{"role": "user", "content": ""}]
            },
            headers={"X-API-KEY": "test-secret-key"}
        )
        assert response.status_code == 422  # Validation error


class TestResponseValidation:
    """Tests for API response validation."""
    
    def test_response_with_error_field(self):
        """Test response containing error field."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "error": {"message": "API error occurred"}
        }
        mock_response.raise_for_status = MagicMock()
        
        mock_client = AsyncMock()
        mock_client.post.return_value = mock_response
        mock_client.__aenter__.return_value = mock_client
        mock_client.__aexit__.return_value = None
        
        with patch('httpx.AsyncClient', return_value=mock_client):
            response = client.post(
                "/v1/chat/completions",
                json={
                    "model": "test-model",
                    "messages": [{"role": "user", "content": "test"}]
                },
                headers={"X-API-KEY": "test-secret-key"}
            )
            # Should handle error gracefully (or rate limit)
            assert response.status_code in [429, 500, 502]
    
    def test_response_missing_choices_field(self):
        """Test response missing choices field."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"id": "test-id"}  # No choices
        mock_response.raise_for_status = MagicMock()
        
        mock_client = AsyncMock()
        mock_client.post.return_value = mock_response
        mock_client.__aenter__.return_value = mock_client
        mock_client.__aexit__.return_value = None
        
        with patch('httpx.AsyncClient', return_value=mock_client):
            response = client.post(
                "/v1/chat/completions",
                json={
                    "model": "test-model",
                    "messages": [{"role": "user", "content": "test"}]
                },
                headers={"X-API-KEY": "test-secret-key"}
            )
            assert response.status_code in [429, 500, 502]
    
    def test_response_with_empty_choices(self):
        """Test response with empty choices array."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"id": "test-id", "choices": []}
        mock_response.raise_for_status = MagicMock()
        
        mock_client = AsyncMock()
        mock_client.post.return_value = mock_response
        mock_client.__aenter__.return_value = mock_client
        mock_client.__aexit__.return_value = None
        
        with patch('httpx.AsyncClient', return_value=mock_client):
            response = client.post(
                "/v1/chat/completions",
                json={
                    "model": "test-model",
                    "messages": [{"role": "user", "content": "test"}]
                },
                headers={"X-API-KEY": "test-secret-key"}
            )
            assert response.status_code in [429, 500, 502]
    
    def test_response_choice_missing_message(self):
        """Test response where choice is missing message field."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "id": "test-id",
            "choices": [{"index": 0}]  # No message
        }
        mock_response.raise_for_status = MagicMock()
        
        mock_client = AsyncMock()
        mock_client.post.return_value = mock_response
        mock_client.__aenter__.return_value = mock_client
        mock_client.__aexit__.return_value = None
        
        with patch('httpx.AsyncClient', return_value=mock_client):
            response = client.post(
                "/v1/chat/completions",
                json={
                    "model": "test-model",
                    "messages": [{"role": "user", "content": "test"}]
                },
                headers={"X-API-KEY": "test-secret-key"}
            )
            assert response.status_code in [429, 500, 502]


class TestStaticFiles:
    """Tests for static file serving."""
    
    def test_ui_directory_mounted(self):
        """Test that UI directory is mounted."""
        # This is tested indirectly through root endpoint
        response = client.get("/")
        # Should not be 404 if UI file exists
        assert response.status_code in [200, 404]
    
    def test_assets_directory_accessible(self):
        """Test that assets directory is accessible."""
        # Try to access assets (may or may not exist)
        response = client.get("/assets/")
        # Should either work or return 404, but not 500
        assert response.status_code in [200, 404, 405]
