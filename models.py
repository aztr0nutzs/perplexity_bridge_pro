"""Model definitions for Perplexity Bridge API."""

MODELS = [
    # OpenAI GPT Models
    {
        "id": "gpt-5.2",
        "name": "GPT-5.2 (ChatGPT)",
        "description": "Advanced reasoning, coding, creativity. Best for generative tasks and complex problem-solving",
        "provider": "perplexity",
        "category": "reasoning"
    },
    # Google Gemini Models
    {
        "id": "gemini-3-pro",
        "name": "Gemini 3 Pro",
        "description": "Multimodal AI with 1M token context. Ideal for large data sets and enterprise tasks",
        "provider": "perplexity",
        "category": "reasoning"
    },
    {
        "id": "gemini-3-flash",
        "name": "Gemini 3 Flash",
        "description": "Fast variant of Gemini 3 optimized for speed while maintaining strong performance",
        "provider": "perplexity",
        "category": "reasoning"
    },
    # Anthropic Claude Models
    {
        "id": "claude-4.5-sonnet",
        "name": "Claude 4.5 Sonnet",
        "description": "Technical reasoning, coding, agentic workflows. Strong for structured problem solving",
        "provider": "perplexity",
        "category": "reasoning"
    },
    {
        "id": "claude-4.5-opus",
        "name": "Claude 4.5 Opus",
        "description": "Most advanced Claude model with superior reasoning for Pro/Max/Enterprise users",
        "provider": "perplexity",
        "category": "reasoning"
    },
    # xAI Grok
    {
        "id": "grok-4.1",
        "name": "Grok 4.1",
        "description": "Conversational intelligence, code, image/text understanding with reasoning toggle",
        "provider": "perplexity",
        "category": "reasoning"
    },
    # Moonshot Kimi
    {
        "id": "kimi-k2-thinking",
        "name": "Kimi K2 Thinking",
        "description": "Privacy-first model with step-by-step reasoning always enabled, ideal for technical analysis",
        "provider": "perplexity",
        "category": "reasoning"
    },
    # Perplexity Sonar Models
    {
        "id": "sonar-pro",
        "name": "Sonar Pro (Llama 3.1 70B)",
        "description": "Real-time search, rapid summarization, transparent source citation. Best for factual research",
        "provider": "perplexity",
        "category": "search"
    },
    {
        "id": "sonar-70b",
        "name": "Sonar 70B",
        "description": "Perplexity's flagship model optimized for real-time search, retrieval, and web summarization",
        "provider": "perplexity",
        "category": "search"
    },
    {
        "id": "llama-3.1-sonar-small-128k-online",
        "name": "Llama 3.1 Sonar Small (128k)",
        "description": "Small Sonar model with 128k context window and online capabilities, fast and efficient",
        "provider": "perplexity",
        "category": "search"
    },
    {
        "id": "llama-3.1-sonar-large-128k-online",
        "name": "Llama 3.1 Sonar Large (128k)",
        "description": "Large Sonar model with 128k context window and online capabilities, balanced performance",
        "provider": "perplexity",
        "category": "search"
    },
    {
        "id": "llama-3.1-sonar-huge-128k-online",
        "name": "Llama 3.1 Sonar Huge (128k)",
        "description": "Huge Sonar model with 128k context window and online capabilities, maximum accuracy",
        "provider": "perplexity",
        "category": "search"
    },
    # Additional Llama Models
    {
        "id": "llama-3.1-70b-instruct",
        "name": "Llama 3.1 70B Instruct",
        "description": "Meta's Llama 3.1 70B instruction-tuned model for general-purpose tasks",
        "provider": "perplexity",
        "category": "general"
    },
    {
        "id": "llama-3.3-90b-instruct",
        "name": "Llama 3.3 90B Instruct",
        "description": "Best-in-class open-source model. Excellent for chat, instruction-following, and general tasks",
        "provider": "perplexity",
        "category": "general"
    },
    {
        "id": "mistral-7b-instruct",
        "name": "Mistral 7B Instruct",
        "description": "Efficient 7B parameter instruction-tuned model for quick responses",
        "provider": "perplexity",
        "category": "general"
    },
]
