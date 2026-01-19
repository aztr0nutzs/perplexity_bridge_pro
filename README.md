![Perplexity Bridge Header](assets/per_api_header.png)

# Perplexity Bridge Pro

## Introduction

**Perplexity Bridge Pro** is a powerful, open-source FastAPI-based proxy bridge that provides unified access to multiple state-of-the-art AI models including Perplexity AI (GPT-5.2, Gemini 3 Pro, Claude 4.5) and GitHub Copilot. This project provides a robust intermediary layer with advanced features like intelligent model routing, rate limiting, real-time WebSocket streaming, a modern web-based dashboard, and integrated development tools.

### Purpose and Overview

The primary purpose of Perplexity Bridge Pro is to simplify and enhance the integration of the world's best AI models into various applications and workflows through a single, unified interface. By acting as a bridge, it offers:

- **Unified Multi-Model Access**: Access GPT-5.2, Gemini 3 Pro, Claude 4.5, Sonar models, and GitHub Copilot through one API
- **Intelligent Model Routing**: Automatically selects the best model for each task based on characteristics
- **Enhanced Security**: API key management and rate limiting to prevent abuse
- **Developer-Friendly Tools**: Web UI for testing, VSCode extension for quick queries, and Python adapters for easy integration
- **Real-Time Capabilities**: WebSocket streaming for live, interactive conversations
- **Cross-Platform Support**: Works on Windows, macOS, Linux, Android, and web browsers

Whether you're a developer building AI-powered applications, a researcher exploring language models, or an enthusiast experimenting with AI, Perplexity Bridge Pro provides the tools and infrastructure to leverage the best models for each task.

## Features and Capabilities

### Core Features

- **Multi-Provider API Access**: Seamlessly switch between Perplexity AI and GitHub Copilot APIs
- **15+ AI Models**: Access to GPT-5.2, Gemini 3 Pro, Claude 4.5, Sonar, Grok, Kimi, and more
- **Intelligent Routing**: Automatic model selection based on task characteristics
- **REST API**: Standard HTTP POST endpoint for chat completions with full OpenAI-compatible formatting
- **WebSocket Streaming**: Real-time, bidirectional streaming for interactive conversations
- **Rate Limiting**: Configurable per-IP rate limiting (default: 10 requests/minute) to manage API usage
- **Authentication**: Secure API key-based authentication system
- **Health Monitoring**: Built-in health check endpoints for system monitoring and uptime tracking

### Multi-Model Support

Access to cutting-edge AI models organized by category:

**Reasoning Models:**
- **GPT-5.2 (ChatGPT)**: Complex reasoning, creativity, general problem-solving
- **Gemini 3 Pro**: 1M token context, multimodal analysis (text/images/video)
- **Claude 4.5 Sonnet/Opus**: Technical reasoning, coding, structured workflows
- **Grok 4.1**: Conversational intelligence with reasoning toggle
- **Kimi K2 Thinking**: Privacy-centric logic-driven solutions

**Search & Research:**
- **Sonar Pro**: Real-time search with source citations
- **Llama 3.1 Sonar Models**: 128k context, online capabilities

**Coding & Development:**
- **GitHub Copilot GPT-4**: Code completion and generation
- **Copilot Agent**: Multi-step DevOps workflows and automation

### Advanced Options

- **Model Categories**: Reasoning, Coding, Search - organized for easy selection
- **Advanced Parameters**: Fine-tune responses with temperature, max tokens, frequency penalty controls
- **System Prompts**: Customizable system prompts for specialized use cases
- **Tool Calling**: Function calling support for enhanced capabilities
- **Conversation History**: Persistent chat history with export capabilities
- **Favorites System**: Save and manage favorite conversations and prompts

### Integrations

- **Web UI Dashboard**: Modern, responsive web interface with model categories and provider indicators
- **Android App**: Native Android application with WebView integration
- **VSCode Extension**: Integrated extension for querying AI directly from VSCode
- **Python Adapters**: Easy-to-use Python libraries (Roo, Copilot) for seamless integration
- **Cross-Origin Support**: CORS-enabled for web application integrations

### Additional Capabilities

- **Error Handling**: Comprehensive error handling with detailed logging and user-friendly messages
- **Statistics Tracking**: Real-time usage statistics and performance metrics
- **Export Functionality**: Export conversations and data in various formats
- **Theme Support**: Light and dark theme options for the web interface
- **Responsive Design**: Mobile-friendly interface that works across all devices

## Installation and Setup

### Prerequisites

Before installing Perplexity Bridge Pro, ensure you have:

- **Python 3.8 or higher** installed on your system
- **Perplexity AI API Key**: Obtain one from [Perplexity AI Settings](https://www.perplexity.ai/settings/api)
- **GitHub Copilot Token** (optional): For Copilot integration, get a GitHub Personal Access Token with Copilot access
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
   # GITHUB_COPILOT_API_KEY=your_github_token_here (optional)
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

After installation, access the web UI at `http://localhost:7860`. The interface provides an intuitive dashboard for interacting with multiple AI models from Perplexity and GitHub Copilot.

#### Choosing the Right Model

The bridge provides access to 15+ AI models organized by category:

- **For Creative Tasks & Reasoning**: Use GPT-5.2 (ChatGPT)
- **For Coding & Development**: Use Copilot GPT-4 or Claude 4.5 Sonnet
- **For Research & Facts**: Use Sonar Pro (includes source citations)
- **For Large Data Analysis**: Use Gemini 3 Pro (1M token context)
- **For DevOps Automation**: Use Copilot Agent

💡 **Tip**: The bridge includes intelligent routing - the `agent/router.py` can automatically select the best model based on your task description!

#### Basic Chat Interface

1. **Select a Model**: Choose from 15+ models in the dropdown, grouped by provider (Perplexity/GitHub Copilot)
2. **View Model Info**: Visit the MODELS tab to see detailed descriptions and categories
3. **Enter Your Prompt**: Type your question or prompt in the text area
4. **Configure Options**: Adjust temperature, max tokens, and other parameters as needed
5. **Send Message**: Click send or press Ctrl+Enter
6. **View Response**: Responses appear in real-time with streaming support (Perplexity models)

#### Advanced Features

- **Model Categories**: Filter models by Reasoning, Coding, or Search capabilities
- **Streaming Toggle**: Enable/disable real-time streaming for instant responses
- **System Prompts**: Add custom system prompts for specialized conversations
- **Tool Configuration**: Add function calling tools for enhanced capabilities
- **Conversation History**: Access previous conversations and continue threads
- **Export Options**: Save conversations as text files or JSON

### Multi-Model Integration

See [MULTI_MODEL_GUIDE.md](MULTI_MODEL_GUIDE.md) for comprehensive documentation on:
- Detailed model capabilities and selection guide
- GitHub Copilot setup and usage
- Intelligent routing configuration
- Python integration examples
- Performance optimization tips

### Screenshots

*(Screenshots would be included here showing the web UI, VSCode extension, and various features)*

### Examples

#### Code Generation with GitHub Copilot

```bash
curl -X POST http://localhost:7860/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "X-API-KEY: your_bridge_secret" \
  -d '{
    "model": "copilot-gpt-4",
    "messages": [
      {"role": "user", "content": "Write a Python function to calculate fibonacci sequence"}
    ],
    "max_tokens": 500,
    "temperature": 0.2
  }'
```

#### Research with Source Citations

```bash
curl -X POST http://localhost:7860/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "X-API-KEY: your_bridge_secret" \
  -d '{
    "model": "sonar-pro",
    "messages": [
      {"role": "user", "content": "What are the latest developments in quantum computing?"}
    ],
    "max_tokens": 1000
  }'
```
  -H "X-API-KEY: your_bridge_secret" \
  -d '{
    "model": "mistral-7b-instruct",
    "messages": [
      {"role": "user", "content": "Explain quantum computing in simple terms"}
    ],
    "max_tokens": 500,
    "temperature": 0.7
  }'
```

#### WebSocket Streaming Example

```javascript
const ws = new WebSocket('ws://localhost:7860/ws/chat?api_key=your_secret');

ws.onopen = () => {
  ws.send(JSON.stringify({
    model: 'llama-3.1-sonar-large-128k-online',
    messages: [{ role: 'user', content: 'What are the latest developments in AI?' }],
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

#### Python Integration

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
response = adapter.query("What is the capital of France?")
print(response)
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
- `model` (string, required): Model ID (e.g., "mistral-7b-instruct")
- `messages` (array, required): Array of message objects with `role` and `content`
- `stream` (boolean, optional): Enable streaming responses (default: false)
- `max_tokens` (integer, optional): Maximum tokens to generate (1-4096, default: 1024)
- `temperature` (float, optional): Sampling temperature (0.0-2.0, default: 0.0)
- `frequency_penalty` (float, optional): Frequency penalty (-2.0-2.0, default: 1.0)

**Example Request:**
```json
{
  "model": "mistral-7b-instruct",
  "messages": [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Hello, how are you?"}
  ],
  "stream": false,
  "max_tokens": 150,
  "temperature": 0.7
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

Retrieve available models.

**Response:**
```json
{
  "models": [
    {
      "id": "mistral-7b-instruct",
      "name": "Mistral 7B Instruct",
      "description": "7B parameter instruction-tuned model"
    },
    {
      "id": "llama-3.1-sonar-small-128k-online",
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
