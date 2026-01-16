
from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect, HTTPException, Response, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field, validator
from typing import List, Dict, Optional, Union
import httpx
import json
import logging
import os
import sys
import webbrowser
import threading
import time
from pathlib import Path
from slowapi import _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from config import PERPLEXITY_KEY, BASE_URL, BRIDGE_SECRET, RATE_LIMIT
from rate_limit import limiter

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Perplexity Bridge API",
    description="""
    Proxy bridge for Perplexity AI API with comprehensive features:
    
    * **REST API**: Standard HTTP POST endpoint for chat completions
    * **WebSocket Streaming**: Real-time streaming responses
    * **Rate Limiting**: Configurable per-IP rate limiting
    * **Authentication**: API key-based authentication
    * **Error Handling**: Comprehensive error handling and logging
    
    ## Authentication
    
    Most endpoints require an `X-API-KEY` header with your bridge secret key.
    Public endpoints: `/health`, `/models`, `/docs`
    
    ## Rate Limiting
    
    Default rate limit: 10 requests per minute per IP address.
    
    ## Models
    
    Use the `/models` endpoint to get a list of available models.
    """,
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure rate limiter with app state
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static files from ui directory
ui_dir = Path(__file__).parent / "ui"
if ui_dir.exists():
    app.mount("/ui", StaticFiles(directory=str(ui_dir)), name="ui")
    
    @app.get("/")
    async def root():
        """Redirect root to UI."""
        return FileResponse(str(ui_dir / "index.html"))


class Message(BaseModel):
    """Chat message model."""
    role: str = Field(..., description="Message role (user, assistant, system)")
    content: str = Field(..., description="Message content")
    
    @validator('role')
    def validate_role(cls, v):
        valid_roles = ['user', 'assistant', 'system']
        if v not in valid_roles:
            raise ValueError(f"Role must be one of {valid_roles}")
        return v
    
    @validator('content')
    def validate_content(cls, v):
        if not v or not v.strip():
            raise ValueError("Content cannot be empty")
        return v.strip()


class ChatReq(BaseModel):
    """Chat completion request model with validation."""
    model: str = Field(..., description="Model name to use")
    messages: List[Message] = Field(..., min_items=1, description="List of chat messages")
    stream: bool = Field(False, description="Whether to stream the response")
    max_tokens: int = Field(1024, ge=1, le=4096, description="Maximum tokens to generate")
    temperature: float = Field(0.0, ge=0.0, le=2.0, description="Sampling temperature")
    frequency_penalty: float = Field(1, ge=-2.0, le=2.0, description="Frequency penalty")
    
    @validator('model')
    def validate_model(cls, v):
        if not v or not v.strip():
            raise ValueError("Model name cannot be empty")
        return v.strip()
    
    @validator('messages')
    def validate_messages(cls, v):
        if not v:
            raise ValueError("At least one message is required")
        if len(v) > 100:
            raise ValueError("Maximum 100 messages allowed")
        return v
    
    class Config:
        schema_extra = {
            "example": {
                "model": "mistral-7b-instruct",
                "messages": [
                    {"role": "user", "content": "What is Python?"}
                ],
                "stream": False,
                "max_tokens": 1024,
                "temperature": 0.0,
                "frequency_penalty": 1
            }
        }


@app.middleware("http")
async def auth(req: Request, call_next):
    """Authentication middleware for HTTP requests."""
    # Skip auth for public endpoints and UI
    public_paths = [
        "/", "/health", "/models", "/docs", "/openapi.json", "/redoc"
    ]
    if req.url.path in public_paths or req.url.path.startswith("/ui/"):
        return await call_next(req)
    
    api_key = req.headers.get("X-API-KEY")
    if api_key != BRIDGE_SECRET:
        logger.warning(f"Unauthorized request attempt from {get_remote_address(req)}")
        return Response(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content=json.dumps({"error": "Unauthorized. Invalid X-API-KEY header."}),
            media_type="application/json"
        )
    return await call_next(req)


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "perplexity-bridge",
        "version": "1.0.0"
    }


@app.get("/models")
async def get_models():
    """
    Get list of available models.
    This endpoint returns commonly used Perplexity models.
    """
    models = [
        {
            "id": "mistral-7b-instruct",
            "name": "Mistral 7B Instruct",
            "description": "7B parameter instruction-tuned model"
        },
        {
            "id": "llama-3.1-sonar-small-128k-online",
            "name": "Llama 3.1 Sonar Small (128k)",
            "description": "Small model with 128k context window and online capabilities"
        },
        {
            "id": "llama-3.1-sonar-large-128k-online",
            "name": "Llama 3.1 Sonar Large (128k)",
            "description": "Large model with 128k context window and online capabilities"
        },
        {
            "id": "llama-3.1-sonar-huge-128k-online",
            "name": "Llama 3.1 Sonar Huge (128k)",
            "description": "Huge model with 128k context window and online capabilities"
        }
    ]
    return {"models": models}


@app.post("/v1/chat/completions")
@limiter.limit(RATE_LIMIT)
async def chat(req: ChatReq, request: Request):
    """
    Chat completions endpoint.
    
    Proxies requests to Perplexity AI API with rate limiting and validation.
    
    **Authentication Required**: Include `X-API-KEY` header
    
    **Rate Limited**: 10 requests per minute per IP (default)
    
    **Request Validation**:
    - Model name must not be empty
    - At least one message required (max 100)
    - Message roles must be: user, assistant, or system
    - Message content cannot be empty
    - max_tokens: 1-4096, temperature: 0.0-2.0, frequency_penalty: -2.0-2.0
    
    **Response**:
    - Validates response structure before returning
    - Returns error if API response is malformed
    - Returns HTTP 502 if Perplexity API returns an error
    
    **Example Request**:
    ```json
    {
      "model": "mistral-7b-instruct",
      "messages": [
        {"role": "user", "content": "What is Python?"}
      ],
      "max_tokens": 1024,
      "temperature": 0.0
    }
    ```
    """
    try:
        headers = {
            "Authorization": f"Bearer {PERPLEXITY_KEY}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        
        request_data = req.dict()
        logger.info(f"Processing chat request with model: {req.model}")
        
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                BASE_URL,
                json=request_data,
                headers=headers
            )
            response.raise_for_status()
            
            # Validate response structure
            response_data = response.json()
            
            if not isinstance(response_data, dict):
                raise ValueError("Response is not a valid JSON object")
            
            if "error" in response_data:
                error_msg = response_data.get("error", {}).get("message", "Unknown API error")
                logger.error(f"Perplexity API returned error: {error_msg}")
                raise HTTPException(
                    status_code=status.HTTP_502_BAD_GATEWAY,
                    detail=f"Perplexity API error: {error_msg}"
                )
            
            # Validate that we have choices
            if "choices" not in response_data:
                logger.error("Response missing 'choices' field")
                raise HTTPException(
                    status_code=status.HTTP_502_BAD_GATEWAY,
                    detail="Invalid response format: missing 'choices' field"
                )
            
            if not isinstance(response_data["choices"], list) or len(response_data["choices"]) == 0:
                logger.error("Response has no choices")
                raise HTTPException(
                    status_code=status.HTTP_502_BAD_GATEWAY,
                    detail="Invalid response format: no choices returned"
                )
            
            # Validate choice structure
            choice = response_data["choices"][0]
            if "message" not in choice:
                logger.error("Choice missing 'message' field")
                raise HTTPException(
                    status_code=status.HTTP_502_BAD_GATEWAY,
                    detail="Invalid response format: choice missing 'message' field"
                )
            
            logger.info("Successfully validated and returning response")
            return response_data
            
    except httpx.HTTPStatusError as e:
        logger.error(f"Perplexity API error: {e.response.status_code} - {e.response.text}")
        raise HTTPException(
            status_code=e.response.status_code,
            detail=f"Perplexity API error: {e.response.text}"
        )
    except httpx.TimeoutException:
        logger.error("Request to Perplexity API timed out")
        raise HTTPException(
            status_code=status.HTTP_504_GATEWAY_TIMEOUT,
            detail="Request to Perplexity API timed out"
        )
    except httpx.RequestError as e:
        logger.error(f"Request error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"Failed to connect to Perplexity API: {str(e)}"
        )
    except Exception as e:
        logger.error(f"Unexpected error in chat endpoint: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )


@app.websocket("/ws/chat")
async def ws_chat(websocket: WebSocket):
    """
    WebSocket endpoint for streaming chat completions.
    
    **Authentication Required**: 
    - Query parameter: `?api_key=your_secret`
    - Or header: `X-API-KEY: your_secret`
    
    **Protocol**:
    1. Client connects to WebSocket
    2. Client sends JSON message with chat request
    3. Server streams response chunks in Server-Sent Events (SSE) format
    4. Server sends `[DONE]` when complete
    
    **Request Format** (same as REST API):
    ```json
    {
      "model": "mistral-7b-instruct",
      "messages": [{"role": "user", "content": "Your prompt"}],
      "stream": true
    }
    ```
    
    **Response Format**:
    - SSE format chunks: `data: {...}\n\n`
    - Final chunk: `data: [DONE]\n\n`
    
    **Error Handling**:
    - Sends JSON error messages: `{"error": "message", "type": "error"}`
    - Closes connection on critical errors
    
    **Example Usage**:
    ```javascript
    const ws = new WebSocket('ws://localhost:7860/ws/chat?api_key=secret');
    ws.onopen = () => {
      ws.send(JSON.stringify({
        model: 'mistral-7b-instruct',
        messages: [{role: 'user', content: 'Hello'}]
      }));
    };
    ws.onmessage = (e) => console.log(e.data);
    ```
    """
    # Get API key from query parameter or header
    api_key = websocket.query_params.get("api_key") or websocket.headers.get("X-API-KEY")
    
    if api_key != BRIDGE_SECRET:
        logger.warning(f"Unauthorized WebSocket connection attempt from {websocket.client}")
        await websocket.close(code=1008, reason="Unauthorized")  # 1008 = Policy Violation
        return
    
    await websocket.accept()
    logger.info(f"WebSocket connection accepted from {websocket.client}")
    
    try:
        while True:
            try:
                # Receive message from client
                data = await websocket.receive_text()
                
                # Parse payload
                try:
                    payload = json.loads(data)
                except json.JSONDecodeError as e:
                    logger.error(f"Invalid JSON in WebSocket message: {str(e)}")
                    await websocket.send_text(json.dumps({
                        "error": "Invalid JSON format",
                        "type": "error"
                    }))
                    continue
                
                # Ensure stream is True
                payload["stream"] = True
                
                headers = {
                    "Authorization": f"Bearer {PERPLEXITY_KEY}",
                    "Content-Type": "application/json"
                }
                
                logger.info(f"Processing WebSocket chat request")
                
                # Stream response from Perplexity API
                async with httpx.AsyncClient(timeout=120.0) as client:
                    try:
                        async with client.stream(
                            "POST",
                            BASE_URL,
                            json=payload,
                            headers=headers
                        ) as response:
                            response.raise_for_status()
                            
                            async for chunk in response.aiter_text():
                                if chunk:
                                    await websocket.send_text(chunk)
                                    
                    except httpx.HTTPStatusError as e:
                        logger.error(f"Perplexity API error in WebSocket: {e.response.status_code}")
                        await websocket.send_text(json.dumps({
                            "error": f"Perplexity API error: {e.response.status_code}",
                            "type": "error"
                        }))
                    except httpx.RequestError as e:
                        logger.error(f"Request error in WebSocket: {str(e)}")
                        await websocket.send_text(json.dumps({
                            "error": f"Connection error: {str(e)}",
                            "type": "error"
                        }))
                        
            except WebSocketDisconnect:
                logger.info(f"WebSocket client disconnected: {websocket.client}")
                break
            except Exception as e:
                logger.error(f"Error processing WebSocket message: {str(e)}", exc_info=True)
                try:
                    await websocket.send_text(json.dumps({
                        "error": f"Internal error: {str(e)}",
                        "type": "error"
                    }))
                except:
                    # Connection may be closed, just break
                    break
                    
    except WebSocketDisconnect:
        logger.info(f"WebSocket disconnected normally: {websocket.client}")
    except Exception as e:
        logger.error(f"WebSocket connection error: {str(e)}", exc_info=True)
    finally:
        try:
            await websocket.close()
        except:
            pass
