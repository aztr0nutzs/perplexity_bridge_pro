# Multi-Model Integration Guide

## Overview

Perplexity Bridge Pro now supports multiple AI models from both Perplexity AI and GitHub Copilot, providing a unified interface for accessing various state-of-the-art language models for different tasks.

## Available Models

### Reasoning Models (Perplexity)

#### GPT-5.2 (ChatGPT)
- **Best for**: Complex reasoning, creativity, general problem-solving
- **Strengths**: Advanced reasoning, reduced hallucination, coding support
- **Use cases**: Brainstorming, content creation, technical explanations

#### Gemini 3 Pro (Google)
- **Best for**: Large data sets, multimodal analysis, enterprise tasks
- **Strengths**: 1M token context window, handles text/images/video/audio
- **Use cases**: Data analysis, document processing, research

#### Claude 4.5 Sonnet/Opus (Anthropic)
- **Best for**: Technical reasoning, coding, structured workflows
- **Strengths**: Deep logic, code review, agentic workflows
- **Use cases**: Code analysis, structured problem solving, automation

#### Grok 4.1 (xAI)
- **Best for**: Conversational intelligence, code understanding
- **Strengths**: Image/text understanding with reasoning toggle
- **Use cases**: General chat, code explanation

#### Kimi K2 Thinking
- **Best for**: Privacy-centric logic-driven solutions
- **Strengths**: Advanced explanations, logical reasoning
- **Use cases**: Sensitive data analysis, logical problem solving

### Search & Research Models (Perplexity)

#### Sonar Pro (Llama 3.1 70B)
- **Best for**: Real-time search, factual research
- **Strengths**: Source citation, up-to-date information
- **Use cases**: Research, fact-checking, current events

#### Llama 3.1 Sonar Models (Small/Large/Huge)
- **Best for**: Online search with varying capabilities
- **Strengths**: 128k context window, online capabilities
- **Use cases**: Extended conversations, research tasks

### Coding Models (GitHub Copilot)

#### Copilot GPT-4
- **Best for**: Code completion, generation, and explanation
- **Strengths**: Deep code understanding, IDE integration
- **Use cases**: Writing code, debugging, code review

#### Copilot Agent
- **Best for**: Multi-step DevOps workflows
- **Strengths**: Task automation, CI/CD integration
- **Use cases**: Build automation, deployment, testing

## Configuration

### Perplexity API Setup

1. Get your API key from [Perplexity AI Settings](https://www.perplexity.ai/settings/api)
2. Add to your `.env` file:
   ```
   PERPLEXITY_API_KEY=your_key_here
   ```

### GitHub Copilot API Setup

1. Generate a GitHub Personal Access Token with Copilot access
2. Add to your `.env` file:
   ```
   GITHUB_COPILOT_API_KEY=your_token_here
   ```

**Note**: GitHub Copilot integration requires an active Copilot subscription.

### Bridge Authentication

Set your bridge secret for API authentication:
```
BRIDGE_SECRET=your_secure_secret_here
```

## Using the Web UI

### Selecting Models

1. Open the web interface at `http://localhost:7860`
2. Use the **model selector dropdown** in the chat interface
3. Models are grouped by provider (Perplexity / GitHub Copilot)
4. Each model shows its category badge (REASONING, CODING, SEARCH)

### Model Categories

Models are color-coded by category in the Models tab:
- **Pink**: Reasoning models - for complex logic and analysis
- **Green**: Coding models - for development tasks
- **Purple**: Search models - for research and fact-finding
- **Cyan**: General purpose models

### Viewing All Models

1. Click the **MODELS** tab to see all available models
2. Models are grouped by provider
3. Click any model card to select it and return to chat
4. View descriptions to understand each model's strengths

## Using the API

### REST API Example

```bash
curl -X POST http://localhost:7860/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "X-API-KEY: your_bridge_secret" \
  -d '{
    "model": "gpt-5.2",
    "messages": [
      {"role": "user", "content": "Explain quantum entanglement"}
    ],
    "max_tokens": 1024,
    "temperature": 0.7
  }'
```

### Switching Between Providers

The bridge automatically routes to the correct provider based on model ID:
- Models starting with `copilot-` → GitHub Copilot API
- All other models → Perplexity API

### Streaming Responses

Enable streaming for real-time responses:

```json
{
  "model": "gpt-5.2",
  "messages": [...],
  "stream": true
}
```

**Note**: Streaming is currently only supported for Perplexity models.

## Python Integration

### Using Perplexity Models

```python
from adapters.roo_adapter import RooAdapter

adapter = RooAdapter(
    url="http://localhost:7860",
    api_key="your_bridge_secret"
)

# Use GPT-5.2
response = adapter.query(
    "What are the latest developments in AI?",
    model="gpt-5.2"
)
print(response)
```

### Using GitHub Copilot Models

```python
from adapters.copilot_adapter import CopilotAdapter

adapter = CopilotAdapter(
    api_key="your_github_token"
)

# Code completion
result = await adapter.code_completion(
    prompt="# Function to calculate fibonacci",
    language="python"
)
print(result)

# Agentic workflow
workflow = await adapter.agent_workflow(
    task="Set up a CI/CD pipeline for a Python project"
)
print(workflow)
```

## Intelligent Model Routing

The bridge includes an intelligent router (`agent/router.py`) that automatically selects the best model for a task:

```python
from agent.router import Router

router = Router()

# Automatically selects the best model
model = router.pick("Write a Python function to sort a list")
# Returns: "copilot-gpt-4"

model = router.pick("Research the history of quantum computing")
# Returns: "sonar-pro"

model = router.pick("Analyze this large dataset")
# Returns: "gemini-3-pro"
```

### Routing Logic

- **Code tasks** → Copilot or Claude
- **Research/factual** → Sonar models
- **Complex reasoning** → GPT-5.2 or Claude
- **Large data** → Gemini 3 Pro
- **DevOps/automation** → Copilot Agent
- **Creative tasks** → GPT-5.2

## Model Selection Guide

### Choose GPT-5.2 when:
- You need creative content generation
- Complex reasoning is required
- General problem-solving tasks
- Flexible dialog and ideation

### Choose Gemini 3 Pro when:
- Working with large datasets
- Processing multimodal content (text + images + video)
- Need extremely large context (1M tokens)
- Enterprise data integration

### Choose Claude 4.5 when:
- Writing or reviewing code
- Need structured, step-by-step reasoning
- Building automated workflows
- Require deep technical analysis

### Choose Sonar Pro when:
- Need current, factual information
- Require source citations
- Researching recent events
- Fact-checking claims

### Choose Copilot GPT-4 when:
- Writing code
- Debugging issues
- Understanding codebases
- Code completion tasks

### Choose Copilot Agent when:
- Multi-step DevOps workflows
- CI/CD automation
- Infrastructure as code
- Build and deployment tasks

## Advanced Features

### Reasoning Mode

Some models support enhanced reasoning mode for deeper analysis:
- Available on: GPT-5.2, Gemini 3 Pro, Claude 4.5, Grok 4.1
- Provides step-by-step logical processing
- Slower but more thorough responses

### Context Windows

Different models support different context lengths:
- **Gemini 3 Pro**: 1M tokens (largest)
- **Sonar models**: 128k tokens
- **GPT-5.2**: ~128k tokens
- **Claude 4.5**: ~200k tokens
- **Copilot**: Varies by model

### Tools and Function Calling

Pass tools configuration for function calling:

```json
{
  "model": "gpt-5.2",
  "messages": [...],
  "tools": [
    {
      "type": "function",
      "function": {
        "name": "search_database",
        "description": "Search the database",
        "parameters": {...}
      }
    }
  ]
}
```

## Troubleshooting

### "GitHub Copilot API is not configured"
- Ensure `GITHUB_COPILOT_API_KEY` is set in `.env`
- Verify your GitHub token has Copilot access
- Check you have an active Copilot subscription

### "PERPLEXITY_API_KEY is not configured"
- Ensure `PERPLEXITY_API_KEY` is set in `.env`
- Verify your API key is valid
- Check your Perplexity API quota

### "Streaming is not yet implemented for GitHub Copilot"
- Disable streaming when using Copilot models
- Streaming is only supported for Perplexity models currently

### Model not appearing in UI
- Refresh the models list in the Models tab
- Check the `/models` endpoint is accessible
- Verify your bridge secret is correct

## Performance Tips

1. **Use the right model for the task**: Don't use GPT-5.2 for simple facts (use Sonar)
2. **Adjust temperature**: 
   - Low (0.0-0.3) for factual/code tasks
   - High (0.7-1.0) for creative tasks
3. **Limit context**: Don't send unnecessary conversation history
4. **Use streaming**: For long responses, streaming provides better UX
5. **Cache frequently used prompts**: Store system prompts in the UI

## Cost Considerations

- **Perplexity**: Charges based on token usage and model selection
- **GitHub Copilot**: Requires active subscription, may have usage limits
- **Bridge**: Free and open-source (you only pay for API usage)

Monitor your usage through the Stats tab in the UI.

## Future Enhancements

Planned features:
- Streaming support for GitHub Copilot
- Model performance metrics
- Automatic model selection based on task analysis
- Cost tracking per model
- Model comparison mode
- Custom model profiles

## Support

For issues or questions:
- Check the main [README.md](README.md)
- Review API documentation at `/docs` endpoint
- Submit issues on GitHub
- Join community discussions

---

*Last updated: January 2026*
