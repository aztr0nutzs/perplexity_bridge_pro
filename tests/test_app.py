"""Tests for the FastAPI application endpoints."""
import os
import pytest
import json
from unittest.mock import patch, AsyncMock, MagicMock
from fastapi.testclient import TestClient
import httpx

# Set test environment before importing app
os.environ["BRIDGE_SECRET"] = "test-secret-key"
os.environ["PERPLEXITY_API_KEY"] = "test-api-key"

from app import app

client = TestClient(app)


def test_health_endpoint():
    """Test health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "perplexity-bridge"
    assert data["version"] == "1.0.0"


def test_root_endpoint():
    """Test root endpoint serves UI."""
    response = client.get("/")
    assert response.status_code == 200
    # Should return HTML file


def test_root_endpoint_ui_not_found():
    """Test root endpoint when UI file doesn't exist."""
    with patch('app.UI_FILE') as mock_ui_file:
        mock_ui_file.exists.return_value = False
        response = client.get("/")
        assert response.status_code == 404


def test_models_endpoint():
    """Test models endpoint returns valid data."""
    response = client.get("/models")
    assert response.status_code == 200
    data = response.json()
    assert "models" in data
    assert "data" in data
    assert isinstance(data["models"], list)
    assert len(data["models"]) > 0
    
    # Verify each model has required fields
    for model in data["models"]:
        assert "id" in model
        assert "name" in model
        assert "description" in model
        assert "provider" in model
        assert "category" in model


def test_models_endpoint_structure():
    """Test models endpoint data structure matches expected format."""
    response = client.get("/models")
    data = response.json()
    
    # Check that data list matches models
    assert len(data["data"]) == len(data["models"])
    
    # Each item in data should have 'object' field
    for item in data["data"]:
        assert item["object"] == "model"


def test_models_endpoint_with_copilot():
    """Test models endpoint includes GitHub Copilot models when configured."""
    with patch('app.has_github_copilot', return_value=True):
        response = client.get("/models")
        data = response.json()
        
        # Should include copilot models
        copilot_models = [m for m in data["models"] if m["provider"] == "github-copilot"]
        assert len(copilot_models) > 0


def test_auth_middleware_blocks_unauthorized():
    """Test authentication middleware blocks requests without API key."""
    response = client.post("/v1/chat/completions", json={
        "model": "test-model",
        "messages": [{"role": "user", "content": "test"}]
    })
    assert response.status_code == 401


def test_auth_middleware_allows_authorized():
    """Test authentication middleware allows requests with valid API key."""
    # Create mock response
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "id": "test-id",
        "model": "test-model", 
        "choices": [{"message": {"role": "assistant", "content": "test response"}}]
    }
    mock_response.raise_for_status = MagicMock()
    
    # Create mock client
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
        # Auth should pass (not 401) - test may fail for other reasons like 
        # model validation, but the key point is auth passes
        assert response.status_code != 401


def test_chat_endpoint_invalid_response_type():
    """Test chat endpoint handles non-dict responses."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = "not a dict"  # Invalid type
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
        # Should get internal server error due to ValueError
        assert response.status_code == 500


def test_chat_endpoint_http_status_error():
    """Test chat endpoint handles HTTP status errors."""
    mock_response = MagicMock()
    mock_response.status_code = 429
    mock_response.text = "Rate limit exceeded"
    
    mock_client = AsyncMock()
    mock_client.post.side_effect = httpx.HTTPStatusError(
        "Error", request=MagicMock(), response=mock_response
    )
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
        assert response.status_code == 429


def test_chat_endpoint_timeout():
    """Test chat endpoint handles timeouts."""
    mock_client = AsyncMock()
    mock_client.post.side_effect = httpx.TimeoutException("Timeout")
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
        assert response.status_code == 504


def test_chat_endpoint_request_error():
    """Test chat endpoint handles request errors."""
    mock_client = AsyncMock()
    mock_client.post.side_effect = httpx.RequestError("Connection failed")
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
        assert response.status_code == 502


def test_chat_endpoint_generic_exception():
    """Test chat endpoint handles generic exceptions."""
    mock_client = AsyncMock()
    mock_client.post.side_effect = Exception("Unexpected error")
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
        assert response.status_code == 500


def test_chat_endpoint_copilot_routing():
    """Test chat endpoint routes to GitHub Copilot for copilot models."""
    with patch('app.has_github_copilot', return_value=True):
        mock_adapter = AsyncMock()
        mock_adapter.chat_completion.return_value = {
            "id": "test-id",
            "choices": [{"message": {"role": "assistant", "content": "response"}}]
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
            # Should route to copilot
            assert mock_adapter.chat_completion.called


def test_terminal_endpoint_requires_auth():
    """Test terminal endpoint requires authentication."""
    response = client.post("/terminal", json={"command": "echo test"})
    assert response.status_code == 401


def test_project_file_endpoint_requires_auth():
    """Test project file endpoint requires authentication."""
    response = client.get("/project/file?path=README.md")
    assert response.status_code == 401
