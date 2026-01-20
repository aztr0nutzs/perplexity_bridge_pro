# Testing Guide - Perplexity Bridge Pro

This guide helps you verify that all features of Perplexity Bridge Pro are working correctly.

## Prerequisites

Before testing, ensure you have:
- ✅ Python 3.8+ installed
- ✅ All dependencies installed (`pip install -r requirements.txt`)
- ✅ `.env` file configured with at least `PERPLEXITY_API_KEY`
- ✅ Optionally, `GITHUB_COPILOT_API_KEY` for Copilot features

## Quick Start Test

### 1. Start the Server

```bash
cd /path/to/perplexity_bridge_pro
uvicorn app:app --host 0.0.0.0 --port 7860
```

Expected output:
```
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:7860
```

### 2. Test Health Endpoint

```bash
curl http://localhost:7860/health
```

Expected response:
```json
{
  "status": "healthy",
  "service": "perplexity-bridge",
  "version": "1.0.0"
}
```

### 3. Test Models Endpoint

```bash
curl http://localhost:7860/models
```

Expected: JSON with 15+ models including:
- `gpt-5.2`
- `gemini-3-pro`
- `claude-4.5-sonnet`
- `sonar-pro`
- `copilot-gpt-4`

### 4. Test Web UI

Open browser to: `http://localhost:7860`

Expected: Cyberpunk-themed UI should load with:
- Header with "DEAD ANGEL // OMNI-BRIDGE"
- Model selector dropdown
- Chat interface
- Multiple tabs (CHAT, HISTORY, PROJECTS, SETTINGS, MODELS, STATS)

## Feature Testing

### Test 1: Model Selection UI

1. Open `http://localhost:7860`
2. Click the **MODELS** tab
3. Verify models are grouped by provider:
   - **perplexity** section with multiple models
   - **github-copilot** section with Copilot models
4. Each model card should show:
   - Model name
   - Category badge (REASONING/CODING/SEARCH)
   - Description

✅ **Pass**: All models visible with correct categories
❌ **Fail**: Models missing or not grouped

### Test 2: Perplexity API Integration

```bash
curl -X POST http://localhost:7860/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "X-API-KEY: dev-secret" \
  -d '{
    "model": "sonar-pro",
    "messages": [
      {"role": "user", "content": "What is 2+2?"}
    ],
    "max_tokens": 100
  }'
```

Expected response structure:
```json
{
  "id": "...",
  "object": "chat.completion",
  "created": 1234567890,
  "model": "sonar-pro",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "2+2 equals 4."
      },
      "finish_reason": "stop"
    }
  ],
  "usage": {...}
}
```

✅ **Pass**: Response received with correct structure
❌ **Fail**: Error response or missing fields

### Test 3: Model Routing

Test that different models route correctly:

**Test GPT-5.2 (Perplexity):**
```bash
curl -X POST http://localhost:7860/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "X-API-KEY: dev-secret" \
  -d '{"model": "gpt-5.2", "messages": [{"role": "user", "content": "Hi"}]}'
```

**Test Copilot (requires GITHUB_COPILOT_API_KEY):**
```bash
curl -X POST http://localhost:7860/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "X-API-KEY: dev-secret" \
  -d '{"model": "copilot-gpt-4", "messages": [{"role": "user", "content": "Write hello world"}]}'
```

✅ **Pass**: Both requests route to correct providers
❌ **Fail**: Routing errors or incorrect provider

### Test 4: Streaming (Perplexity only)

```bash
curl -X POST http://localhost:7860/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "X-API-KEY: dev-secret" \
  -d '{
    "model": "sonar-pro",
    "messages": [{"role": "user", "content": "Count to 5"}],
    "stream": true
  }'
```

Expected: Streaming response with SSE format:
```
data: {"choices":[{"delta":{"content":"1"}}]}

data: {"choices":[{"delta":{"content":","}}]}

data: [DONE]
```

✅ **Pass**: Chunks arrive progressively
❌ **Fail**: No streaming or errors

### Test 5: Intelligent Router

Test the automatic model selection:

```python
from agent.router import Router

router = Router()

# Should select Copilot for code
model = router.pick("Write a Python function")
assert model == "copilot-gpt-4", f"Expected copilot-gpt-4, got {model}"

# Should select Sonar for research
model = router.pick("Research quantum computing")
assert model == "sonar-pro", f"Expected sonar-pro, got {model}"

# Should select GPT for reasoning
model = router.pick("Explain why the sky is blue")
assert model == "gpt-5.2", f"Expected gpt-5.2, got {model}"

print("✅ All router tests passed!")
```

✅ **Pass**: Router selects appropriate models
❌ **Fail**: Wrong model selections

### Test 6: Authentication

**Test without API key (should fail):**
```bash
curl -X POST http://localhost:7860/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model": "gpt-5.2", "messages": [{"role": "user", "content": "Hi"}]}'
```

Expected: HTTP 401 Unauthorized

**Test with wrong API key (should fail):**
```bash
curl -X POST http://localhost:7860/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "X-API-KEY: wrong-key" \
  -d '{"model": "gpt-5.2", "messages": [{"role": "user", "content": "Hi"}]}'
```

Expected: HTTP 401 Unauthorized

✅ **Pass**: Unauthorized requests rejected
❌ **Fail**: Unauthorized requests accepted

### Test 7: Rate Limiting

Run this script to test rate limiting:

```bash
for i in {1..15}; do
  echo "Request $i"
  curl -s -o /dev/null -w "%{http_code}\n" \
    -X POST http://localhost:7860/v1/chat/completions \
    -H "Content-Type: application/json" \
    -H "X-API-KEY: dev-secret" \
    -d '{"model": "gpt-5.2", "messages": [{"role": "user", "content": "Hi"}]}'
  sleep 0.1
done
```

Expected: First 10 requests succeed (200), then rate limit kicks in (429)

✅ **Pass**: Rate limiting works after 10 requests
❌ **Fail**: All requests succeed or rate limit incorrect

## Web UI Tests

### Test 8: Model Dropdown Updates

1. Open `http://localhost:7860`
2. Check model selector dropdown
3. Verify it contains models from both providers
4. Each option should show: `Model Name [provider]`

Example options:
- `GPT-5.2 (ChatGPT) [perplexity]`
- `GitHub Copilot GPT-4 [github-copilot]`

✅ **Pass**: Dropdown populated with all models
❌ **Fail**: Missing models or no provider labels

### Test 9: Send Message

1. Open `http://localhost:7860`
2. Select model "gpt-5.2"
3. Enter message: "What is Python?"
4. Click "TRANSMIT ➤"
5. Wait for response

Expected:
- Loading indicator appears
- Response streams in (if streaming enabled)
- Message appears in conversation
- Stats update (bottom of page)

✅ **Pass**: Complete flow works
❌ **Fail**: Errors or no response

### Test 10: Model Card Selection

1. Open `http://localhost:7860`
2. Click **MODELS** tab
3. Click any model card (e.g., "Claude 4.5 Sonnet")
4. Verify:
   - Returns to CHAT tab
   - Model selector shows selected model
   - Toast notification appears

✅ **Pass**: Model selection works
❌ **Fail**: Selection doesn't change dropdown

## Python Adapter Tests

### Test 11: Roo Adapter

```python
from adapters.roo_adapter import RooAdapter

adapter = RooAdapter(
    url="http://localhost:7860",
    api_key="dev-secret"
)

response = adapter.query("What is 1+1?", model="gpt-5.2")
print(f"Response: {response}")

assert len(response) > 0, "Response is empty"
print("✅ Roo adapter test passed!")
```

### Test 12: Copilot Adapter (requires token)

```python
import asyncio
from adapters.copilot_adapter import CopilotAdapter

async def test_copilot():
    adapter = CopilotAdapter(
        api_key="your_github_token"
    )
    
    result = await adapter.code_completion(
        prompt="# Function to add two numbers",
        language="python"
    )
    
    print(f"Result: {result}")
    assert "choices" in result, "Invalid response structure"
    print("✅ Copilot adapter test passed!")

asyncio.run(test_copilot())
```

## Android App Tests

### Test 13: Android WebView

1. Build and install the Android app
2. Launch the app
3. Verify:
   - WebView loads the bridge UI
   - All tabs accessible
   - Model selector works
   - Can send messages
   - Responses display correctly

✅ **Pass**: Full functionality on Android
❌ **Fail**: UI broken or features missing

## Performance Tests

### Test 14: Response Time

Test average response time for different models:

```bash
#!/bin/bash
for model in "gpt-5.2" "sonar-pro" "claude-4.5-sonnet"; do
  echo "Testing $model..."
  time curl -s -X POST http://localhost:7860/v1/chat/completions \
    -H "Content-Type: application/json" \
    -H "X-API-KEY: dev-secret" \
    -d "{\"model\": \"$model\", \"messages\": [{\"role\": \"user\", \"content\": \"Hi\"}]}" \
    > /dev/null
done
```

Expected: Response times < 5 seconds for short prompts

✅ **Pass**: Reasonable response times
❌ **Fail**: Very slow or timeout

## Troubleshooting

### Common Issues

**Issue**: "PERPLEXITY_API_KEY is not configured"
- **Fix**: Add `PERPLEXITY_API_KEY=your_key` to `.env`

**Issue**: "GitHub Copilot API is not configured"
- **Fix**: Add `GITHUB_COPILOT_API_KEY=your_token` to `.env` or skip Copilot tests

**Issue**: Models not loading in UI
- **Fix**: Check browser console for errors, verify `/models` endpoint works

**Issue**: CORS errors in browser
- **Fix**: Ensure server is running, check browser isn't blocking requests

**Issue**: Rate limit exceeded immediately
- **Fix**: Wait 60 seconds, or increase `RATE_LIMIT` in `config.py`

## Test Summary Checklist

Use this checklist to track your testing:

- [ ] Server starts successfully
- [ ] Health endpoint responds
- [ ] Models endpoint returns all models
- [ ] Web UI loads correctly
- [ ] Models grouped by provider in UI
- [ ] Can send messages via UI
- [ ] Perplexity API integration works
- [ ] Model routing works (Perplexity vs Copilot)
- [ ] Streaming works for Perplexity models
- [ ] Intelligent router selects correct models
- [ ] Authentication blocks unauthorized requests
- [ ] Rate limiting enforces limits
- [ ] Model dropdown populates correctly
- [ ] Model card selection works
- [ ] Roo adapter works
- [ ] Copilot adapter works (if configured)
- [ ] Android app works (if applicable)
- [ ] Response times acceptable

## Reporting Issues

If tests fail, please provide:
1. Which test failed
2. Error messages
3. Browser console logs (for UI issues)
4. Server logs
5. Your configuration (without API keys)

---

**Last updated**: January 2026
