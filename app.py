
from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect, HTTPException, Response, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field, validator
from typing import List, Dict, Optional, Union, Any
import asyncio
import httpx
import json
import logging
import os
import time
import shlex
from pathlib import Path
from slowapi import _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from config import (
    PERPLEXITY_KEY, BASE_URL, BRIDGE_SECRET, RATE_LIMIT,
    GITHUB_COPILOT_KEY, GITHUB_COPILOT_BASE_URL, has_github_copilot
)
from rate_limit import limiter
from adapters.copilot_adapter import CopilotAdapter
from models import MODELS

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
    allow_origins=[
        "http://localhost:7860",
        "http://127.0.0.1:7860",
        os.getenv("ALLOWED_ORIGIN", ""),  # Add production domain via env var
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type", "X-API-KEY", "Authorization"],
)

# Paths
PROJECT_ROOT = Path(__file__).parent.resolve()
UI_FILE = PROJECT_ROOT / "ui" / "perplex_index2.html"

# Serve static files from ui directory
ui_dir = Path(__file__).parent / "ui"
if ui_dir.exists():
    app.mount("/ui", StaticFiles(directory=str(ui_dir)), name="ui")

# Serve assets directory
assets_dir = Path(__file__).parent / "assets"
if assets_dir.exists():
    app.mount("/assets", StaticFiles(directory=str(assets_dir)), name="assets")

@app.get("/")
async def root():
    """Serve the main UI."""
    if UI_FILE.exists():
        return FileResponse(str(UI_FILE))
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="UI not found")


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
    tools: Optional[List[Dict[str, Union[str, Dict, List]]]] = Field(
        default=None,
        description="Optional tools configuration"
    )
    
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
        json_schema_extra = {
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

class TerminalReq(BaseModel):
    """Terminal execution request."""
    command: str = Field(..., description="Shell command to execute")


def get_perplexity_key() -> str:
    if not PERPLEXITY_KEY or not PERPLEXITY_KEY.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="PERPLEXITY_API_KEY is not configured on the server"
        )
    return PERPLEXITY_KEY.strip()


def get_model_provider(model_id: str) -> str:
    """
    Determine which API provider to use based on model ID.
    
    Returns:
        'perplexity' or 'github-copilot'
    """
    if model_id.startswith("copilot-"):
        return "github-copilot"
    return "perplexity"


async def _perplexity_chat(req: ChatReq, request_data: dict) -> Any:
    """Handle chat request via Perplexity API."""
    key = get_perplexity_key()
    headers = {
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    
    if req.stream:
        async def stream_response():
            async with httpx.AsyncClient(timeout=120.0) as client:
                async with client.stream(
                    "POST",
                    BASE_URL,
                    json=request_data,
                    headers=headers
                ) as response:
                    if response.status_code >= 400:
                        error_text = await response.aread()
                        error_payload = json.dumps({
                            "error": f"Perplexity API error: {error_text.decode(errors='replace')}",
                            "type": "error"
                        })
                        yield f"data: {error_payload}\n\n"
                        return
                    async for chunk in response.aiter_text():
                        if chunk:
                            yield chunk

        return StreamingResponse(stream_response(), media_type="text/event-stream")
    
    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.post(
            BASE_URL,
            json=request_data,
            headers=headers
        )
        response.raise_for_status()
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
        
        choice = response_data["choices"][0]
        if "message" not in choice:
            logger.error("Choice missing 'message' field")
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail="Invalid response format: choice missing 'message' field"
            )
        
        logger.info("Successfully validated and returning response")
        return response_data


async def _copilot_chat(req: ChatReq, request_data: dict) -> Any:
    """Handle chat request via GitHub Copilot API."""
    if not has_github_copilot():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="GitHub Copilot API is not configured. Please set GITHUB_COPILOT_API_KEY."
        )
    
    try:
        adapter = CopilotAdapter(api_key=GITHUB_COPILOT_KEY, base_url=GITHUB_COPILOT_BASE_URL)
        
        if req.stream:
            # For streaming, we'd need to implement streaming in the adapter
            # For now, return a note that streaming is not yet supported for Copilot
            raise HTTPException(
                status_code=status.HTTP_501_NOT_IMPLEMENTED,
                detail="Streaming is not yet implemented for GitHub Copilot. Please disable streaming."
            )
        
        response_data = await adapter.chat_completion(
            messages=[m.dict() for m in req.messages],
            model=req.model,
            stream=False,
            max_tokens=req.max_tokens,
            temperature=req.temperature
        )
        
        logger.info("Successfully received response from GitHub Copilot")
        return response_data
        
    except Exception as e:
        logger.error(f"GitHub Copilot API error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"GitHub Copilot API error: {str(e)}"
        )


@app.middleware("http")
async def auth(req: Request, call_next):
    """Authentication middleware for HTTP requests."""
    # Skip auth for public endpoints and UI
    public_paths = [
        "/", "/health", "/models", "/docs", "/openapi.json", "/redoc"
    ]
    if (
        req.url.path in public_paths
        or req.url.path.startswith("/ui/")
        or req.url.path == "/ui"
        or req.url.path.startswith("/assets/")
        or req.url.path == "/assets"
    ):
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
    Get list of available models from both Perplexity and GitHub Copilot.
    This endpoint returns all supported models including GPT, Gemini, Claude, and reasoning models.
    Model availability depends on your Perplexity API subscription tier.
    """
    models = list(MODELS)  # Make a copy to avoid modifying the original
    
    # Add GitHub Copilot models if configured
    if has_github_copilot():
        models.extend([
            {
                "id": "copilot-gpt-4",
                "name": "Copilot GPT-4",
                "description": "GitHub Copilot powered by GPT-4, optimized for code generation and completion",
                "provider": "github-copilot",
                "category": "coding"
            },
            {
                "id": "copilot-agent",
                "name": "Copilot Agent",
                "description": "GitHub Copilot agent mode for autonomous coding tasks",
                "provider": "github-copilot",
                "category": "coding"
            },
        ])
    
    data = [
        {
            "id": m["id"],
            "name": m["name"],
            "description": m["description"],
            "provider": m["provider"],
            "category": m["category"],
            "object": "model"
        }
        for m in models
    ]
    return {"models": models, "data": data}


@app.post("/v1/chat/completions")
@limiter.limit(RATE_LIMIT)
async def chat(req: ChatReq, request: Request):
    """
    Chat completions endpoint.
    
    Proxies requests to Perplexity AI API or GitHub Copilot API based on model selection.
    
    **Authentication Required**: Include `X-API-KEY` header
    
    **Rate Limited**: 10 requests per minute per IP (default)
    
    **Request Validation**:
    - Model name must not be empty
    - At least one message required (max 100)
    - Message roles must be: user, assistant, or system
    - Message content cannot be empty
    - max_tokens: 1-4096, temperature: 0.0-2.0, frequency_penalty: -2.0-2.0
    
    **Supported Providers**:
    - Perplexity: GPT-5.2, Gemini 3 Pro, Claude 4.5, Sonar models, etc.
    - GitHub Copilot: copilot-gpt-4, copilot-agent
    
    **Response**:
    - Validates response structure before returning
    - Returns error if API response is malformed
    - Returns HTTP 502 if upstream API returns an error
    
    **Example Request**:
    ```json
    {
      "model": "gpt-5.2",
      "messages": [
        {"role": "user", "content": "What is Python?"}
      ],
      "max_tokens": 1024,
      "temperature": 0.0
    }
    ```
    """
    try:
        request_data = req.dict()
        provider = get_model_provider(req.model)
        logger.info(f"Processing chat request with model: {req.model} (provider: {provider})")
        
        if provider == "github-copilot":
            return await _copilot_chat(req, request_data)
        else:
            return await _perplexity_chat(req, request_data)
            
    except httpx.HTTPStatusError as e:
        logger.error(f"API error: {e.response.status_code} - {e.response.text}")
        raise HTTPException(
            status_code=e.response.status_code,
            detail=f"API error: {e.response.text}"
        )
    except httpx.TimeoutException:
        logger.error("Request to API timed out")
        raise HTTPException(
            status_code=status.HTTP_504_GATEWAY_TIMEOUT,
            detail="Request to API timed out"
        )
    except httpx.RequestError as e:
        logger.error(f"Request error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"Failed to connect to API: {str(e)}"
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
                
                try:
                    key = get_perplexity_key()
                except HTTPException as e:
                    await websocket.send_text(json.dumps({
                        "error": e.detail,
                        "type": "error"
                    }))
                    await websocket.close(code=1011, reason="Server configuration error")
                    return
                headers = {
                    "Authorization": f"Bearer {key}",
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


def _validate_terminal_command(command: str) -> List[str]:
    if not command or not command.strip():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Command cannot be empty")
    if len(command) > 200:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Command too long")
    if any(token in command for token in ["&&", "||", ";", "|", "`", "$(", ">", "<"]):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Unsupported shell operators")

    args = shlex.split(command)
    if not args:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid command")

    allowlist = {
        "echo", "printf", "pwd", "ls", "dir", "whoami", "date", "uname",
        "cat", "head", "tail", "sed", "awk", "rg", "find",
        "sleep", "wc", "sort", "uniq", "grep"
    }
    cmd = args[0]
    if cmd not in allowlist:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Command not allowed: {cmd}")

    for arg in args[1:]:
        if "\x00" in arg:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid argument")
        if arg.startswith(("/", "~", "\\")) or ".." in arg:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Path outside project is not allowed")
        if len(arg) >= 2 and arg[1] == ":":
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Path outside project is not allowed")

    return args


@app.post("/terminal")
@limiter.limit(RATE_LIMIT)
async def terminal(req: TerminalReq, request: Request):
    """Execute a command with streaming output and guardrails."""
    args = _validate_terminal_command(req.command)
    max_output_bytes = 64 * 1024
    timeout_seconds = 8
    start_time = time.monotonic()

    async def stream_output():
        output_bytes = 0
        proc = await asyncio.create_subprocess_exec(
            *args,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            cwd=str(PROJECT_ROOT)
        )

        async def read_line(stream):
            return await stream.readline()

        tasks = {
            asyncio.create_task(read_line(proc.stdout)): "stdout",
            asyncio.create_task(read_line(proc.stderr)): "stderr"
        }

        while tasks:
            if time.monotonic() - start_time > timeout_seconds:
                proc.kill()
                yield 'data: {"type":"error","message":"Command timed out"}\n\n'
                break
            done, _ = await asyncio.wait(
                tasks.keys(),
                timeout=0.1,
                return_when=asyncio.FIRST_COMPLETED
            )
            if not done:
                if proc.returncode is not None:
                    break
                continue
            for task in done:
                label = tasks.pop(task)
                line = task.result()
                if line:
                    output_bytes += len(line)
                    if output_bytes > max_output_bytes:
                        proc.kill()
                        yield 'data: {"type":"error","message":"Output limit exceeded"}\n\n'
                        tasks.clear()
                        break
                    payload = json.dumps({
                        "type": "stream",
                        "stream": label,
                        "text": line.decode(errors="replace")
                    })
                    yield f"data: {payload}\n\n"
                    tasks[asyncio.create_task(read_line(getattr(proc, label)))] = label

        try:
            await asyncio.wait_for(proc.wait(), timeout=1)
        except asyncio.TimeoutError:
            proc.kill()

        exit_payload = json.dumps({
            "type": "exit",
            "code": proc.returncode if proc.returncode is not None else -1
        })
        yield f"data: {exit_payload}\n\n"

    return StreamingResponse(stream_output(), media_type="text/event-stream")


@app.get("/project/file")
@limiter.limit(RATE_LIMIT)
async def project_file(path: str, request: Request):
    """Read a project file safely with size limits."""
    if not path or path.strip() == "":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Path is required")
    if path.startswith("/") or ".." in path:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid path")

    file_path = (PROJECT_ROOT / path).resolve()
    if not str(file_path).startswith(str(PROJECT_ROOT)):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Path outside project root")
    if not file_path.exists() or not file_path.is_file():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="File not found")

    max_bytes = 200 * 1024
    truncated = False
    with open(file_path, "rb") as handle:
        data = handle.read(max_bytes + 1)
        if len(data) > max_bytes:
            data = data[:max_bytes]
            truncated = True

    content = data.decode("utf-8", errors="replace")
    return {"path": path, "content": content, "truncated": truncated}
