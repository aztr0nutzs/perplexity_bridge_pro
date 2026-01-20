# Quick Start Guide - Multi-Model Integration

## 🎉 What's New

Your Perplexity Bridge Pro now supports **15+ AI models** from both **Perplexity AI** and **GitHub Copilot** through a single, unified interface!

## 🚀 Quick Setup (3 Steps)

### Step 1: Configure API Keys

Edit your `.env` file:

```bash
# Required - Perplexity AI
PERPLEXITY_API_KEY=your_perplexity_key_here

# Optional - GitHub Copilot (for coding features)
GITHUB_COPILOT_API_KEY=your_github_token_here

# Your bridge secret
BRIDGE_SECRET=dev-secret
```

### Step 2: Start the Server

```bash
uvicorn app:app --host 0.0.0.0 --port 7860
```

### Step 3: Open the UI

Navigate to: `http://localhost:7860`

## 🤖 Available Models

### Reasoning Models (Perplexity)
- **GPT-5.2** - Best for complex reasoning and creativity
- **Gemini 3 Pro** - 1M token context, multimodal analysis
- **Claude 4.5 Sonnet** - Technical reasoning and coding
- **Grok 4.1** - Conversational intelligence
- **Kimi K2 Thinking** - Logic-driven solutions

### Search Models (Perplexity)
- **Sonar Pro** - Real-time search with citations
- **Llama 3.1 Sonar** variants - Online capabilities

### Coding Models (GitHub Copilot)
- **Copilot GPT-4** - Code generation and completion
- **Copilot Agent** - Multi-step DevOps workflows

## 💡 How to Use

### In the Web UI

1. Click the **model dropdown** at the top
2. Choose a model (e.g., "GPT-5.2" or "Copilot GPT-4")
3. Type your message
4. Click "TRANSMIT"

**Tip**: Visit the **MODELS** tab to see all models with descriptions!

### Via API

```bash
curl -X POST http://localhost:7860/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "X-API-KEY: dev-secret" \
  -d '{
    "model": "gpt-5.2",
    "messages": [{"role": "user", "content": "Your question here"}]
  }'
```

### In Python

```python
from adapters.roo_adapter import RooAdapter

adapter = RooAdapter(url="http://localhost:7860", api_key="dev-secret")
response = adapter.query("What is Python?", model="gpt-5.2")
print(response)
```

## 🎯 Which Model Should I Use?

- **Writing code?** → `copilot-gpt-4`
- **Need facts with sources?** → `sonar-pro`
- **Complex reasoning task?** → `gpt-5.2`
- **Large data analysis?** → `gemini-3-pro`
- **Code review?** → `claude-4.5-sonnet`

## 🔍 Smart Model Selection

The bridge can automatically choose the best model for you:

```python
from agent.router import Router

router = Router()
model = router.pick("Write a Python function")  # Returns: "copilot-gpt-4"
model = router.pick("Research quantum computing")  # Returns: "sonar-pro"
```

## 📚 Learn More

- **Full Model Guide**: [MULTI_MODEL_GUIDE.md](MULTI_MODEL_GUIDE.md)
- **Testing Guide**: [TESTING_GUIDE.md](TESTING_GUIDE.md)
- **Implementation Details**: [IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md)

## ❓ Troubleshooting

### "PERPLEXITY_API_KEY is not configured"
➡️ Add your Perplexity API key to the `.env` file

### "GitHub Copilot API is not configured"
➡️ This is optional! Only needed if you want Copilot features. Add `GITHUB_COPILOT_API_KEY` to use it.

### Models not showing in UI
➡️ Refresh the page and check the Models tab

### Need help?
➡️ Check [TESTING_GUIDE.md](TESTING_GUIDE.md) for detailed testing procedures

## ✨ Features at a Glance

✅ **15+ AI models** in one place  
✅ **Automatic model routing** based on task  
✅ **Simple UI** with model categories  
✅ **API compatible** with existing code  
✅ **GitHub Copilot** integration ready  
✅ **Zero breaking changes** - everything still works!  

## 🎓 Example Use Cases

**Creative Writing**
```
Model: gpt-5.2
Prompt: "Write a short story about a robot learning to paint"
```

**Code Generation**
```
Model: copilot-gpt-4
Prompt: "Write a Python function to validate email addresses"
```

**Research**
```
Model: sonar-pro
Prompt: "What are the latest developments in quantum computing?"
```

**Data Analysis**
```
Model: gemini-3-pro
Prompt: "Analyze this large dataset and find patterns: [data]"
```

---

**Ready to go!** Start the server and visit `http://localhost:7860` to try it out! 🚀
