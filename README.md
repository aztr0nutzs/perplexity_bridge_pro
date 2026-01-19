![Perplexity Bridge Header](assets/per_api_header.png)

# Perplexity Bridge Pro

## Introduction

**Perplexity Bridge Pro** is a powerful, open-source FastAPI-based proxy bridge that connects seamlessly to the Perplexity AI API. This project provides a robust intermediary layer with advanced features like rate limiting, real-time WebSocket streaming, a modern web-based dashboard, and integrated development tools including a VSCode extension and Python adapters.

### Purpose and Overview

The primary purpose of Perplexity Bridge Pro is to simplify and enhance the integration of Perplexity AI's powerful language models into various applications and workflows. By acting as a bridge, it offers:

- **Unified API Access**: Standardized endpoints for chat completions and model management
- **Enhanced Security**: API key management and rate limiting to prevent abuse
- **Developer-Friendly Tools**: Web UI for testing, VSCode extension for quick queries, and Python adapters for easy integration
- **Real-Time Capabilities**: WebSocket streaming for live, interactive conversations
- **Cross-Platform Support**: Works on Windows, macOS, Linux, and web browsers

Whether you're a developer building AI-powered applications, a researcher exploring language models, or an enthusiast experimenting with AI, Perplexity Bridge Pro provides the tools and infrastructure to make integration smooth and efficient.

## Features and Capabilities

### Core Features

- **REST API**: Standard HTTP POST endpoint for chat completions with full OpenAI-compatible formatting
- **WebSocket Streaming**: Real-time, bidirectional streaming for interactive conversations
- **Rate Limiting**: Configurable per-IP rate limiting (default: 10 requests/minute) to manage API usage
- **Authentication**: Secure API key-based authentication system
- **Health Monitoring**: Built-in health check endpoints for system monitoring and uptime tracking

### Advanced Options

- **Comprehensive Model Support**: Access to all Perplexity-supported AI models including:
  - **GPT-5.2** (OpenAI) - Advanced reasoning, coding, and deep logic
  - **Claude 4.5 Sonnet & Opus** (Anthropic) - Superior reasoning and coding with safety focus
  - **Gemini 3 Pro & Flash** (Google) - Multimodal AI with massive context windows
  - **Grok 4.1** (xAI) - Real-time web access and conversational intelligence
  - **Kimi K2** (Moonshot) - Privacy-first with always-on reasoning
  - **Sonar Models** (Perplexity/Llama 3.1) - Optimized for real-time search with citations
  - **Llama 3.1 & Mistral** - Efficient general-purpose models
- **Reasoning Modes**: Many models support explicit reasoning toggles for deeper analysis
- **Advanced Parameters**: Fine-tune responses with temperature, max tokens, frequency penalty controls
- **System Prompts**: Customizable system prompts for specialized use cases
- **Conversation History**: Persistent chat history with export capabilities
- **Favorites System**: Save and manage favorite conversations and prompts

### Integrations

- **Web UI Dashboard**: Modern, responsive web interface for testing and managing interactions
- **VSCode Extension**: Integrated extension for querying Perplexity directly from VSCode
- **Python Roo Adapter**: Easy-to-use Python library for seamless integration into Python projects
- **Cross-Origin Support**: CORS-enabled for web application integrations

### Additional Capabilities

- **Error Handling**: Comprehensive error handling with detailed logging and user-friendly messages
- **Statistics Tracking**: Real-time usage statistics and performance metrics
- **Export Functionality**: Export conversations and data in various formats
- **Theme Support**: Light and dark theme options for the web interface
- **Responsive Design**: Mobile-friendly interface that works across all devices

## Available Models

Perplexity Bridge Pro provides access to the **complete range of models** available through the Perplexity AI API. All models are accessible through this bridge, exactly as Perplexity offers them - that's the whole point of this unique bridge application! Model availability depends on your Perplexity API subscription tier and valid API key.

### OpenAI GPT Models

#### GPT-5.2
- **Model ID**: `gpt-5.2`
- **Reasoning**: ✅ Advanced reasoning mode available
- **Best For**: Deep logical reasoning, complex coding tasks, structured content generation, long-context analysis
- **Strengths**: Generalist model with high accuracy, creativity, and state-of-the-art hallucination mitigation
- **Context Window**: Large context support
- **Use Cases**: Essays, code debugging, multi-step planning, complex problem-solving

### Anthropic Claude Models

#### Claude 4.5 Sonnet
- **Model ID**: `claude-4.5-sonnet`
- **Reasoning**: ✅ Reasoning mode available
- **Best For**: Efficient coding, business automation, technical problem-solving
- **Strengths**: High-reliability reasoning, safe and structured responses, excellent for agentic workflows
- **Use Cases**: Production code, automated workflows, technical documentation

#### Claude 4.5 Opus
- **Model ID**: `claude-4.5-opus`
- **Reasoning**: ✅ Full reasoning capabilities (Pro/Max/Enterprise)
- **Best For**: Most demanding reasoning tasks, enterprise use cases
- **Strengths**: Superior reasoning, advanced coding abilities, nuanced responses for complex scenarios
- **Use Cases**: Complex business logic, critical decision-making, sophisticated analysis

### Google Gemini Models

#### Gemini 3 Pro
- **Model ID**: `gemini-3-pro`
- **Reasoning**: ✅ Always-on reasoning
- **Best For**: Multimodal AI tasks, large-scale data analysis, enterprise search
- **Strengths**: Native support for huge context windows (up to 1M tokens), seamless across text/code/video/audio
- **Context Window**: Up to 1 million tokens
- **Use Cases**: Organization-wide document search, video/audio analysis, complex data summarization

#### Gemini 3 Flash
- **Model ID**: `gemini-3-flash`
- **Reasoning**: ✅ Fast reasoning
- **Best For**: Speed-optimized multimodal tasks
- **Strengths**: Faster inference while maintaining strong performance
- **Use Cases**: Real-time applications, quick analysis, rapid prototyping

### xAI Grok

#### Grok 4.1
- **Model ID**: `grok-4.1`
- **Reasoning**: ✅ Reasoning toggle available
- **Best For**: Real-time data access, trend detection, social media analysis
- **Strengths**: Up-to-date web/social data (especially X/Twitter), creative responses, emerging event analysis
- **Use Cases**: Social listening, trend detection, current events, breaking news analysis

### Moonshot Kimi

#### Kimi K2 Thinking
- **Model ID**: `kimi-k2-thinking`
- **Reasoning**: ✅ Always-on step-by-step reasoning
- **Best For**: Privacy-first technical analysis, logical problem-solving
- **Strengths**: Strong privacy focus, stepwise reasoning built-in, technical explanations
- **Use Cases**: Confidential analysis, privacy-sensitive organizations, detailed technical breakdowns

### Perplexity Sonar Models (Real-time Search)

Perplexity's proprietary models built on Llama 3.1, optimized for real-time web search with source citations.

#### Sonar 70B
- **Model ID**: `sonar-70b`
- **Reasoning**: ✅ Reasoning toggle available
- **Best For**: Fast real-time search, current information retrieval
- **Strengths**: Source-cited, fresh data, highly reliable for current events
- **Use Cases**: Research, fact-checking, news aggregation, up-to-date information

#### Sonar Small (128k) Online
- **Model ID**: `llama-3.1-sonar-small-128k-online`
- **Context Window**: 128k tokens
- **Best For**: Fast lookups, quick queries with online capabilities
- **Strengths**: Efficient, fast responses with web access
- **Use Cases**: Quick research, rapid fact-checking

#### Sonar Large (128k) Online
- **Model ID**: `llama-3.1-sonar-large-128k-online`
- **Context Window**: 128k tokens
- **Best For**: Balanced performance with online search capabilities
- **Strengths**: Good balance of speed and accuracy with real-time web data
- **Use Cases**: General research, comprehensive queries, detailed lookups

#### Sonar Huge (128k) Online
- **Model ID**: `llama-3.1-sonar-huge-128k-online`
- **Context Window**: 128k tokens
- **Best For**: Maximum accuracy with online capabilities
- **Strengths**: Most accurate Sonar variant, deep analysis with web access
- **Use Cases**: Critical research, detailed analysis, comprehensive investigations

### Other Models

#### Llama 3.1 70B Instruct
- **Model ID**: `llama-3.1-70b-instruct`
- **Best For**: General-purpose instruction following
- **Strengths**: Meta's powerful instruction-tuned model, versatile
- **Use Cases**: General tasks, instruction following, conversational AI

#### Mistral 7B Instruct
- **Model ID**: `mistral-7b-instruct`
- **Best For**: Efficient quick responses
- **Strengths**: Fast, lightweight, efficient for simple tasks
- **Use Cases**: Quick queries, simple tasks, resource-constrained environments

### Model Selection Guide

**For Coding & Technical Tasks**: Claude 4.5 Sonnet/Opus, GPT-5.2  
**For Research & Current Information**: Sonar models, Grok 4.1  
**For Multimodal & Large Context**: Gemini 3 Pro/Flash  
**For Privacy-Sensitive Work**: Kimi K2 Thinking  
**For Complex Reasoning**: GPT-5.2, Claude 4.5 Opus, Gemini 3 Pro  
**For Speed & Efficiency**: Gemini 3 Flash, Mistral 7B, Sonar Small  
**For Real-time Trends**: Grok 4.1, Sonar models  

### Important Notes

- **Valid API Key Required**: All models require a valid Perplexity API key with appropriate subscription tier
- **Subscription Tiers**: Some models (like Claude 4.5 Opus) require Pro/Max/Enterprise subscriptions
- **Model Availability**: Model availability may vary based on your Perplexity account tier and region
- **Reasoning Modes**: Models with reasoning capabilities can be toggled for deeper analysis at the cost of response time
- **Context Windows**: Respect model-specific context window limits for optimal performance
- **API Costs**: Usage incurs costs based on your Perplexity API pricing plan and model selection

## Installation and Setup

### Prerequisites

Before installing Perplexity Bridge Pro, ensure you have:

- **Python 3.8 or higher** installed on your system
- **Perplexity AI API Key**: Obtain one from [Perplexity AI Settings](https://www.perplexity.ai/settings/api)
- **Node.js 14+** (optional, required only for VSCode extension development)

### Quick Start Installation

For the fastest setup experience, use our automated installers:

#### Windows

1. Download or clone the repository
2. Double-click `install_windows.bat` to install dependencies
3. Edit the generated `.env` file and add your `PERPLEXITY_API_KEY`
4. Double-click `Launch Perplexity Bridge.vbs` or `start.bat` to start the application

The web UI will automatically open in your default browser at `http://localhost:7860`.

#### macOS

1. Open Terminal and navigate to the project directory
2. Run the installation script:
   ```bash
   chmod +x install.sh && ./install.sh
   ```
3. Edit `.env` file with your API key:
   ```bash
   nano .env  # Add PERPLEXITY_API_KEY=your_key_here
   ```
4. Start the application:
   ```bash
   ./start.sh
   ```

#### Linux

1. Open a terminal in the project directory
2. Make scripts executable and run installation:
   ```bash
   chmod +x install.sh start.sh
   ./install.sh
   ```
3. Configure environment:
   ```bash
   nano .env  # Add your PERPLEXITY_API_KEY
   ```
4. Launch the application:
   ```bash
   ./start.sh
   ```

#### Web Browsers (Browser Extension)

Perplexity Bridge Pro runs as a web application and works in all modern browsers including Chrome, Firefox, Safari, and Edge.

### Manual Installation

For advanced users or custom deployments:

1. **Clone the Repository**
   ```bash
   git clone https://github.com/yourusername/perplexity_bridge_pro.git
   cd perplexity_bridge_pro
   ```

2. **Create Virtual Environment** (recommended)
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment Variables**
   ```bash
   cp env.example .env
   # Edit .env with your settings:
   # PERPLEXITY_API_KEY=your_api_key_here
   # BRIDGE_SECRET=your_secure_secret_here
   ```

5. **Start the Server**
   ```bash
   uvicorn app:app --host 0.0.0.0 --port 7860
   ```

### Docker Installation (Coming Soon)

Docker support is planned for future releases to enable containerized deployments.

## Usage Guides

### Getting Started

After installation, access the web UI at `http://localhost:7860`. The interface provides an intuitive dashboard for interacting with Perplexity AI models.

#### Basic Chat Interface

1. **Select a Model**: Choose from all available models including GPT-5.2, Claude 4.5, Gemini 3 Pro, Grok 4.1, Kimi K2, and Sonar variants
2. **Enter Your Prompt**: Type your question or prompt in the text area
3. **Configure Options**: Adjust temperature, max tokens, and other parameters as needed
4. **Send Message**: Click send or press Ctrl+Enter
5. **View Response**: Responses appear in real-time with streaming support

#### Advanced Features

- **Streaming Toggle**: Enable/disable real-time streaming for instant responses
- **System Prompts**: Add custom system prompts for specialized conversations
- **Conversation History**: Access previous conversations and continue threads
- **Export Options**: Save conversations as text files or JSON

### Screenshots

*(Screenshots would be included here showing the web UI, VSCode extension, and various features)*

### Examples

#### Using GPT-5.2 for Complex Reasoning

```bash
curl -X POST http://localhost:7860/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "X-API-KEY: your_bridge_secret" \
  -d '{
    "model": "gpt-5.2",
    "messages": [
      {"role": "user", "content": "Explain quantum entanglement and its implications for quantum computing"}
    ],
    "max_tokens": 1000,
    "temperature": 0.2
  }'
```

#### Using Claude 4.5 Sonnet for Code Generation

```bash
curl -X POST http://localhost:7860/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "X-API-KEY: your_bridge_secret" \
  -d '{
    "model": "claude-4.5-sonnet",
    "messages": [
      {"role": "user", "content": "Write a Python function to implement binary search with comprehensive error handling"}
    ],
    "max_tokens": 1500,
    "temperature": 0.3
  }'
```

#### Using Gemini 3 Pro for Multimodal Analysis

```bash
curl -X POST http://localhost:7860/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "X-API-KEY: your_bridge_secret" \
  -d '{
    "model": "gemini-3-pro",
    "messages": [
      {"role": "user", "content": "Analyze this large codebase and provide architectural recommendations"}
    ],
    "max_tokens": 2000,
    "temperature": 0.4
  }'
```

#### Using Grok 4.1 for Real-time Information

```bash
curl -X POST http://localhost:7860/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "X-API-KEY: your_bridge_secret" \
  -d '{
    "model": "grok-4.1",
    "messages": [
      {"role": "user", "content": "What are the latest trends in AI development this week?"}
    ],
    "max_tokens": 800,
    "temperature": 0.6
  }'
```

#### Using Sonar for Research with Citations

```bash
curl -X POST http://localhost:7860/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "X-API-KEY: your_bridge_secret" \
  -d '{
    "model": "sonar-70b",
    "messages": [
      {"role": "user", "content": "What are the recent breakthroughs in fusion energy research?"}
    ],
    "max_tokens": 1200,
    "temperature": 0.5
  }'
```

#### WebSocket Streaming with Different Models

```javascript
// Using Claude for streaming code assistance
const ws = new WebSocket('ws://localhost:7860/ws/chat?api_key=your_secret');

ws.onopen = () => {
  ws.send(JSON.stringify({
    model: 'claude-4.5-sonnet',
    messages: [{ role: 'user', content: 'Help me optimize this Python code for performance' }],
    stream: true,
    temperature: 0.3
  }));
};

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  if (data.choices && data.choices[0].delta) {
    console.log('Chunk:', data.choices[0].delta.content);
  }
};
```

```javascript
// Using Sonar for real-time research
const ws = new WebSocket('ws://localhost:7860/ws/chat?api_key=your_secret');

ws.onopen = () => {
  ws.send(JSON.stringify({
    model: 'llama-3.1-sonar-large-128k-online',
    messages: [{ role: 'user', content: 'What are the latest developments in renewable energy?' }],
    stream: true,
    temperature: 0.5
  }));
};

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  if (data.choices && data.choices[0].delta) {
    console.log('Chunk:', data.choices[0].delta.content);
  }
};
```

#### Python Integration with Multiple Models

```python
from adapters.roo_adapter import RooAdapter

# Initialize with explicit settings
adapter = RooAdapter(
    url="http://localhost:7860",
    api_key="your_bridge_secret"
)

# Or use environment variables
import os
os.environ['ROO_BRIDGE_URL'] = 'http://localhost:7860'
os.environ['ROO_BRIDGE_KEY'] = 'your_bridge_secret'

adapter = RooAdapter()

# Use GPT-5.2 for complex reasoning
response = adapter.query(
    "Explain the implications of quantum supremacy",
    model="gpt-5.2"
)
print(response)

# Use Claude for code generation
code_response = adapter.query(
    "Generate a REST API endpoint for user authentication",
    model="claude-4.5-sonnet"
)
print(code_response)

# Use Sonar for research
research = adapter.query(
    "What are the latest advancements in CRISPR gene editing?",
    model="sonar-70b"
)
print(research)

# Use Gemini for large context analysis
analysis = adapter.query(
    "Analyze these 50 documents and provide a comprehensive summary",
    model="gemini-3-pro"
)
print(analysis)
```

### VSCode Extension Usage

1. **Install the Extension**: Use the provided `.vsix` file or publish to marketplace
2. **Configure Settings**:
   - Open VSCode Settings (Ctrl+,)
   - Search for "Perplexity Bridge"
   - Set URL, API key, and default model
3. **Use Commands**:
   - Press `Ctrl+Shift+P` (Cmd+Shift+P on Mac)
   - Type "Ask Perplexity" and select
   - Enter your question in the input box

### Troubleshooting

#### Common Issues

**"PERPLEXITY_API_KEY environment variable is required"**
- Ensure you've set the `PERPLEXITY_API_KEY` in your `.env` file or environment variables
- Restart the application after making changes

**"Unauthorized" errors**
- Verify the `X-API-KEY` header matches your `BRIDGE_SECRET`
- Check for typos in API keys

**CORS errors in browser**
- Ensure the bridge server is running on the correct port
- Check CORS configuration in `app.py` for production deployments

**Rate limit exceeded**
- Default limit is 10 requests per minute per IP
- Wait for the limit to reset or adjust `RATE_LIMIT` in `config.py`

**Connection refused**
- Verify the server is running on the expected port (default: 7860)
- Check firewall settings and network configuration

**WebSocket connection fails**
- Ensure you're using the correct WebSocket URL: `ws://localhost:7860/ws/chat`
- Include `api_key` as query parameter or `X-API-KEY` header

#### Performance Tips

- Use streaming for better responsiveness with long responses
- Adjust `max_tokens` based on your needs to control response length
- Lower temperature values (0.0-0.3) for more deterministic responses
- Higher temperature values (0.7-1.0) for more creative outputs

## API Documentation

### Authentication

All API endpoints (except health and models) require authentication via the `X-API-KEY` header:

```
X-API-KEY: your_bridge_secret
```

### Endpoints

#### `POST /v1/chat/completions`

Main chat completion endpoint compatible with OpenAI API format.

**Parameters:**
- `model` (string, required): Model ID - see Available Models section for complete list
  - Examples: "gpt-5.2", "claude-4.5-sonnet", "gemini-3-pro", "grok-4.1", "kimi-k2-thinking", "sonar-70b"
- `messages` (array, required): Array of message objects with `role` and `content`
- `stream` (boolean, optional): Enable streaming responses (default: false)
- `max_tokens` (integer, optional): Maximum tokens to generate (1-4096, default: 1024)
- `temperature` (float, optional): Sampling temperature (0.0-2.0, default: 0.0)
- `frequency_penalty` (float, optional): Frequency penalty (-2.0-2.0, default: 1.0)

**Example Request with GPT-5.2:**
```json
{
  "model": "gpt-5.2",
  "messages": [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Explain quantum computing"}
  ],
  "stream": false,
  "max_tokens": 500,
  "temperature": 0.3
}
```

**Example Request with Claude 4.5:**
```json
{
  "model": "claude-4.5-sonnet",
  "messages": [
    {"role": "user", "content": "Write a Python function for sorting"}
  ],
  "stream": false,
  "max_tokens": 800,
  "temperature": 0.2
}
```

**Response:**
```json
{
  "id": "chatcmpl-123",
  "object": "chat.completion",
  "created": 1677652288,
  "model": "mistral-7b-instruct",
  "choices": [{
    "index": 0,
    "message": {
      "role": "assistant",
      "content": "Hello! I'm doing well, thank you for asking. How can I help you today?"
    },
    "finish_reason": "stop"
  }],
  "usage": {
    "prompt_tokens": 13,
    "completion_tokens": 17,
    "total_tokens": 30
  }
}
```

#### `GET /models`

Retrieve all available models including GPT, Claude, Gemini, Grok, Kimi, and Sonar variants.

**Response:**
```json
{
  "models": [
    {
      "id": "gpt-5.2",
      "name": "GPT-5.2",
      "description": "OpenAI's latest flagship model with advanced reasoning capabilities"
    },
    {
      "id": "claude-4.5-sonnet",
      "name": "Claude 4.5 Sonnet",
      "description": "Efficient Claude model with strong coding and reasoning abilities"
    },
    {
      "id": "gemini-3-pro",
      "name": "Gemini 3 Pro",
      "description": "Google's multimodal AI with large context windows (up to 1M tokens)"
    },
    {
      "id": "grok-4.1",
      "name": "Grok 4.1",
      "description": "xAI's model with real-time web access"
    },
    {
      "id": "kimi-k2-thinking",
      "name": "Kimi K2 Thinking",
      "description": "Privacy-first model with step-by-step reasoning"
    },
    {
      "id": "sonar-70b",
      "name": "Sonar 70B",
      "description": "Perplexity's flagship model optimized for real-time search with citations"
    }
      "name": "Llama 3.1 Sonar Small (128k)",
      "description": "Small model with 128k context window and online capabilities"
    }
  ]
}
```

#### `GET /health`

Health check endpoint.

**Response:**
```json
{
  "status": "healthy",
  "service": "perplexity-bridge",
  "version": "1.0.0",
  "uptime": "1h 23m 45s"
}
```

#### `WS /ws/chat`

WebSocket endpoint for real-time streaming.

**Connection:** `ws://localhost:7860/ws/chat?api_key=your_secret`

**Message Format:** Same as REST API request body with `stream: true`

**Response Format:** Server-Sent Events with JSON chunks

### Error Codes

- `400`: Bad Request - Invalid parameters
- `401`: Unauthorized - Invalid or missing API key
- `429`: Too Many Requests - Rate limit exceeded
- `500`: Internal Server Error - Server-side issues
- `502`: Bad Gateway - Perplexity API errors

## Supported Environments and Use Cases

### Supported Environments

- **Operating Systems**: Windows 10+, macOS 10.15+, Linux (Ubuntu 18.04+, CentOS 7+)
- **Web Browsers**: Chrome 80+, Firefox 75+, Safari 13+, Edge 80+
- **Python Versions**: 3.8, 3.9, 3.10, 3.11
- **Development Environments**: VSCode, PyCharm, Jupyter, command line

### Use Cases

#### Development and Prototyping

- **API Testing**: Use the web UI to test Perplexity API integrations
- **Rapid Prototyping**: Quickly build and test AI-powered features
- **Debugging**: Monitor API calls and responses with detailed logging

#### Production Applications

- **Chatbots**: Build conversational AI applications
- **Content Generation**: Automated content creation and summarization
- **Research Tools**: Academic research and data analysis
- **Educational Platforms**: Interactive learning and tutoring systems

#### Integration Scenarios

- **Web Applications**: Frontend apps needing AI capabilities
- **Mobile Apps**: Backend services for mobile AI features
- **Desktop Applications**: Standalone tools with AI assistance
- **IoT Devices**: Smart devices with voice AI interfaces

#### Limitations

- **Rate Limits**: Subject to Perplexity API limits and bridge rate limiting
- **Context Window**: Limited by selected model capabilities
- **Internet Required**: Requires active internet for Perplexity API access
- **API Costs**: Usage incurs costs based on Perplexity API pricing

## Contribution Guidelines

We welcome contributions from the community! Here's how you can help improve Perplexity Bridge Pro:

### Getting Started

1. **Fork the Repository**: Create your own fork on GitHub
2. **Clone Your Fork**: `git clone https://github.com/yourusername/perplexity_bridge_pro.git`
3. **Create a Branch**: `git checkout -b feature/your-feature-name`
4. **Set Up Development Environment**: Follow the installation instructions above

### Development Workflow

1. **Code Standards**:
   - Follow PEP 8 for Python code
   - Use meaningful variable and function names
   - Add docstrings to all functions and classes
   - Write comprehensive unit tests

2. **Testing**:
   - Test your changes thoroughly
   - Ensure all existing tests pass
   - Add new tests for new features

3. **Documentation**:
   - Update README.md for any new features
   - Add inline comments for complex logic
   - Update API documentation if endpoints change

### Submitting Changes

1. **Commit Messages**: Use clear, descriptive commit messages
   ```bash
   git commit -m "Add feature: brief description of changes"
   ```

2. **Pull Request**:
   - Push your branch to GitHub
   - Create a pull request with detailed description
   - Reference any related issues

3. **Code Review**:
   - Address review feedback promptly
   - Make requested changes and push updates

### Areas for Contribution

- **Bug Fixes**: Identify and fix issues
- **Feature Enhancements**: Add new capabilities
- **Documentation**: Improve guides and examples
- **Testing**: Write and maintain test suites
- **Performance**: Optimize for speed and efficiency
- **UI/UX**: Enhance the web interface
- **Integrations**: Add support for new platforms

### Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Help newcomers learn and contribute
- Follow our community guidelines

## Licensing Information

Perplexity Bridge Pro is licensed under the MIT License.

### MIT License

Copyright (c) 2024 Perplexity Bridge Pro Contributors

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

### Third-Party Licenses

This project uses the following third-party libraries:

- **FastAPI**: Licensed under MIT
- **Uvicorn**: Licensed under BSD
- **httpx**: Licensed under BSD
- **python-dotenv**: Licensed under BSD
- **slowapi**: Licensed under MIT

For full license texts, see the respective project repositories.

## FAQ

### General Questions

**Q: What is Perplexity Bridge Pro?**
A: It's an open-source proxy bridge that provides a standardized interface to Perplexity AI's language models, with additional features like rate limiting, web UI, and developer tools.

**Q: Do I need a Perplexity API key?**
A: Yes, you need a valid Perplexity AI API key to use this bridge. Get one from their website.

**Q: Is it free to use?**
A: The bridge software is free and open-source. You'll incur costs based on your Perplexity API usage.

**Q: What's the difference between this and direct Perplexity API access?**
A: This bridge adds authentication, rate limiting, web UI, streaming support, and developer tools on top of the base API.

### Technical Questions

**Q: Can I run this on my server?**
A: Yes, you can deploy it on any server that supports Python. For production, consider using a reverse proxy with SSL.

**Q: How do I change the default port?**
A: Modify the port in your startup command: `uvicorn app:app --host 0.0.0.0 --port YOUR_PORT`

**Q: Can I use this with other AI APIs?**
A: Currently, it's designed specifically for Perplexity AI. Support for other APIs may be added in future versions.

**Q: How do I backup my conversation history?**
A: Use the export feature in the web UI or access the browser's localStorage data.

### Troubleshooting

**Q: The web UI won't load. What should I do?**
A: Check that the server is running on the correct port and that your firewall allows connections.

**Q: I'm getting rate limit errors. How can I fix this?**
A: Increase the rate limit in `config.py` or wait for the current limit to reset. For high usage, contact Perplexity about API limits.

**Q: The VSCode extension isn't working. What could be wrong?**
A: Verify your settings in VSCode and ensure the bridge server is running. Check the developer console for error messages.

**Q: How do I update to the latest version?**
A: Pull the latest changes from the repository and reinstall dependencies: `pip install -r requirements.txt`

### Support

For additional help:
- Check the [Issues](https://github.com/yourusername/perplexity_bridge_pro/issues) page
- Review the [Documentation](https://github.com/yourusername/perplexity_bridge_pro/wiki)
- Join our [Community Discussions](https://github.com/yourusername/perplexity_bridge_pro/discussions)

---

*Perplexity Bridge Pro is not affiliated with Perplexity AI. This is an independent project.*
