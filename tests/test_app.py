"""Tests for the FastAPI application endpoints."""
import os
from unittest.mock import patch, AsyncMock, MagicMock
from fastapi.testclient import TestClient

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


def test_terminal_endpoint_requires_auth():
    """Test terminal endpoint requires authentication."""
    response = client.post("/terminal", json={"command": "echo test"})
    assert response.status_code == 401


def test_project_file_endpoint_requires_auth():
    """Test project file endpoint requires authentication."""
    response = client.get("/project/file?path=README.md")
    assert response.status_code == 401
