# Perplexity Bridge Pro

A FastAPI-based proxy bridge for the Perplexity AI API with rate limiting, WebSocket streaming support, web UI, and VSCode extension integration.

## Features

- ✅ **REST API** - Standard HTTP POST endpoint for chat completions
- ✅ **WebSocket Streaming** - Real-time streaming responses via WebSocket
- ✅ **Rate Limiting** - Configurable rate limiting (default: 10 requests/minute per IP)
- ✅ **Web UI** - Built-in dashboard for testing and interaction
- ✅ **VSCode Extension** - Integrated VSCode extension for quick queries
- ✅ **Roo Adapter** - Python adapter for easy integration
- ✅ **Authentication** - API key-based authentication
- ✅ **Error Handling** - Comprehensive error handling and logging
- ✅ **CORS Support** - Configured for cross-origin requests
- ✅ **Health Checks** - Health check endpoint for monitoring

## Prerequisites

- Python 3.8 or higher
- Perplexity AI API Key ([Get one here](https://www.perplexity.ai/settings/api))
- Node.js 14+ (for VSCode extension development, optional)

## Installation

### 🚀 Quick Start (Recommended)

**For detailed installation instructions, see [INSTALL.md](INSTALL.md)**

#### Windows:
1. Double-click `install_windows.bat`
2. Edit `.env` file and add your `PERPLEXITY_API_KEY`
3. Double-click `Launch Perplexity Bridge.vbs` or `start.bat`

#### Linux:
```bash
chmod +x install.sh && ./install.sh
nano .env  # Add your PERPLEXITY_API_KEY
./start.sh
```

The browser will automatically open to the UI!

### 📋 Manual Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd perplexity_bridge_pro
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   # Copy the example file
   cp env.example .env
   
   # Edit .env and add your Perplexity API key
   # PERPLEXITY_API_KEY=your_api_key_here
   # BRIDGE_SECRET=your_secure_secret_here
   ```

   Or export directly:
   ```bash
   export PERPLEXITY_API_KEY=your_api_key_here
   export BRIDGE_SECRET=your_secure_secret_here  # Optional, defaults to "dev-secret"
   ```

## Usage

### Starting the Server

```bash
uvicorn app:app --host 0.0.0.0 --port 7860
```

The server will start on `http://localhost:7860` by default.

### Web UI

The UI is automatically served and the browser opens when you run `start.py` or `start.bat`/`start.sh`.

Manual access:
- Main UI: `http://localhost:7860/` (redirects to UI)
- Direct UI: `http://localhost:7860/ui/`

**Features:**
- Configure API URL and secret key
- Settings are persisted in browser localStorage
- Choose between REST or WebSocket streaming
- Support for multiple models
- Real-time streaming responses

### REST API

#### Chat Completions

```bash
curl -X POST http://localhost:7860/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "X-API-KEY: your_secret_here" \
  -d '{
    "model": "mistral-7b-instruct",
    "messages": [
      {"role": "user", "content": "What is Python?"}
    ]
  }'
```

#### Get Available Models

```bash
curl http://localhost:7860/models
```

#### Health Check

```bash
curl http://localhost:7860/health
```

### WebSocket Streaming

```javascript
const ws = new WebSocket('ws://localhost:7860/ws/chat?api_key=your_secret_here');

ws.onopen = () => {
  ws.send(JSON.stringify({
    model: 'mistral-7b-instruct',
    messages: [{ role: 'user', content: 'Tell me about AI' }],
    stream: true
  }));
};

ws.onmessage = (event) => {
  console.log('Chunk:', event.data);
};
```

### Python Roo Adapter

```python
from adapters.roo_adapter import RooAdapter

# Initialize adapter
adapter = RooAdapter(
    url="http://localhost:7860",
    api_key="your_secret_here"
)

# Query the API
response = adapter.query("What is machine learning?")
print(response)
```

Or use environment variables:

```bash
export ROO_BRIDGE_URL=http://localhost:7860
export ROO_BRIDGE_KEY=your_secret_here
```

```python
from adapters.roo_adapter import RooAdapter

adapter = RooAdapter()  # Uses environment variables
response = adapter.query("What is Python?")
```

### VSCode Extension

1. **Install dependencies** (for development):
   ```bash
   cd vscode_extension
   npm install
   ```

2. **Configure settings** in VSCode:
   - Open Settings (Ctrl+, / Cmd+,)
   - Search for "Perplexity Bridge"
   - Set:
     - `perplexityBridge.url`: Your bridge URL (default: `http://localhost:7860`)
     - `perplexityBridge.apiKey`: Your API secret key
     - `perplexityBridge.model`: Default model to use

3. **Use the extension**:
   - Press `Ctrl+Shift+P` (or `Cmd+Shift+P` on Mac)
   - Type "Ask Perplexity"
   - Enter your question

## API Reference

### Endpoints

#### `POST /v1/chat/completions`
Chat completion endpoint.

**Headers:**
- `X-API-KEY`: Your bridge secret key (required)
- `Content-Type`: application/json

**Request Body:**
```json
{
  "model": "string (required)",
  "messages": [
    {
      "role": "user|assistant|system",
      "content": "string"
    }
  ],
  "stream": false,
  "max_tokens": 1024,
  "temperature": 0.0,
  "frequency_penalty": 1.0
}
```

**Response:**
```json
{
  "choices": [
    {
      "message": {
        "role": "assistant",
        "content": "Response text..."
      }
    }
  ]
}
```

#### `GET /health`
Health check endpoint (no authentication required).

**Response:**
```json
{
  "status": "healthy",
  "service": "perplexity-bridge",
  "version": "1.0.0"
}
```

#### `GET /models`
Get available models (no authentication required).

**Response:**
```json
{
  "models": [
    {
      "id": "mistral-7b-instruct",
      "name": "Mistral 7B Instruct",
      "description": "7B parameter instruction-tuned model"
    }
  ]
}
```

#### `WS /ws/chat`
WebSocket endpoint for streaming.

**Query Parameters:**
- `api_key`: Your bridge secret key

**Message Format:** Same as REST API request body

**Response:** Server-Sent Events (SSE) format chunks

## Configuration

### Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `PERPLEXITY_API_KEY` | Yes | - | Your Perplexity AI API key |
| `BRIDGE_SECRET` | No | `dev-secret` | Secret key for bridge authentication |
| `ROO_BRIDGE_URL` | No | `http://localhost:7860` | Bridge URL for RooAdapter |
| `ROO_BRIDGE_KEY` | No | `dev-secret` | API key for RooAdapter |

### Rate Limiting

Default rate limit: **10 requests per minute per IP address**

To modify, edit `config.py`:
```python
RATE_LIMIT = "20/minute"  # Adjust as needed
```

### CORS Configuration

Edit `app.py` to restrict CORS origins for production:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com"],  # Specify allowed origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## Security Notes

⚠️ **Important for Production:**

1. **Never use default secrets** - Always set a strong `BRIDGE_SECRET`
2. **Restrict CORS origins** - Don't use `allow_origins=["*"]` in production
3. **Use HTTPS** - Run behind a reverse proxy (nginx, Apache) with SSL
4. **Environment variables** - Store secrets securely, never commit `.env` files
5. **Rate limiting** - Adjust based on your usage and API limits

## Development

### Running in Development Mode

```bash
uvicorn app:app --reload --host 0.0.0.0 --port 7860
```

### Project Structure

```
perplexity_bridge_pro/
├── app.py                 # Main FastAPI application
├── config.py              # Configuration and validation
├── rate_limit.py          # Rate limiting setup
├── requirements.txt       # Python dependencies
├── env.example            # Environment variable template
├── README.md              # This file
├── adapters/
│   └── roo_adapter.py    # Python adapter for easy integration
├── ui/
│   ├── index.html        # Web UI
│   ├── app.js            # UI JavaScript
│   └── style.css         # UI styles
└── vscode_extension/
    ├── extension.js      # VSCode extension code
    └── package.json      # Extension manifest
```

## Troubleshooting

### "PERPLEXITY_API_KEY environment variable is required"
- Make sure you've set the `PERPLEXITY_API_KEY` environment variable
- Or created a `.env` file with the key

### "Unauthorized" errors
- Check that you're sending the correct `X-API-KEY` header
- Verify `BRIDGE_SECRET` matches what you're sending

### CORS errors in browser
- Ensure CORS middleware is properly configured
- Check that your origin is allowed (if restricted)

### Rate limit errors
- You've exceeded 10 requests per minute
- Wait or adjust the rate limit in `config.py`

### Connection refused (RooAdapter)
- Make sure the bridge server is running
- Verify the `ROO_BRIDGE_URL` is correct

## License

[Your License Here]

## Contributing

[Your Contributing Guidelines Here]

## Support

For issues, questions, or contributions, please [open an issue](https://github.com/yourusername/perplexity_bridge_pro/issues).
