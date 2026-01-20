
class Router:
    """
    Intelligent model router that selects the best model for a given task.
    
    Routes between Perplexity models (GPT-5.2, Gemini 3 Pro, Claude 4.5, Sonar)
    and GitHub Copilot models based on task characteristics.
    """
    
    def pick(self, task):
        """
        Select the best model for a task based on keywords and patterns.
        
        Args:
            task: Task description string
            
        Returns:
            Model ID to use
        """
        t = task.lower()
        
        # Coding and development tasks -> GitHub Copilot or Claude
        if any(keyword in t for keyword in ["code", "function", "class", "bug", "debug", "implement", "refactor"]):
            if "review" in t or "explain" in t:
                return "claude-4.5-sonnet"
            return "copilot-gpt-4"
        
        # Complex reasoning and logic -> GPT-5.2 or Claude
        if any(keyword in t for keyword in ["reason", "analyze", "logic", "think", "complex", "solve"]):
            if "technical" in t or "precise" in t:
                return "claude-4.5-sonnet"
            return "gpt-5.2"
        
        # Research and factual queries -> Sonar
        if any(keyword in t for keyword in ["research", "find", "search", "what is", "who is", "fact", "source"]):
            return "sonar-pro"
        
        # Large data processing and multimodal -> Gemini
        if any(keyword in t for keyword in ["data", "dataset", "analyze data", "large", "multimodal", "image", "video"]):
            return "gemini-3-pro"
        
        # Architecture and design tasks -> Sonar Large or Claude
        if any(keyword in t for keyword in ["design", "arch", "architecture", "plan", "structure"]):
            return "claude-4.5-sonnet"
        
        # Testing and debugging -> Claude or Copilot
        if any(keyword in t for keyword in ["test", "testing", "unit test", "qa"]):
            return "copilot-gpt-4"
        
        # Creative and generative tasks -> GPT-5.2
        if any(keyword in t for keyword in ["create", "generate", "write", "creative", "story", "content"]):
            return "gpt-5.2"
        
        # DevOps and automation -> Copilot Agent
        if any(keyword in t for keyword in ["deploy", "ci/cd", "pipeline", "automate", "devops"]):
            return "copilot-agent"
        
        # Default: Use GPT-5.2 for general tasks
        return "gpt-5.2"
    
    def pick_with_reasoning(self, task):
        """
        Select model and provide reasoning for the choice.
        
        Args:
            task: Task description string
            
        Returns:
            Tuple of (model_id, reasoning)
        """
        model = self.pick(task)
        
        reasons = {
            "gpt-5.2": "Best for complex reasoning, creativity, and general problem-solving",
            "gemini-3-pro": "Optimal for large data sets and multimodal analysis",
            "claude-4.5-sonnet": "Strongest for technical reasoning, coding, and structured workflows",
            "claude-4.5-opus": "Premium tier for most demanding logic tasks",
            "sonar-pro": "Best for factual research with source citations",
            "copilot-gpt-4": "Specialized for code generation and development tasks",
            "copilot-agent": "Multi-step agentic workflows for DevOps automation",
            "llama-3.1-sonar-large-128k-online": "Large context window for comprehensive tasks"
        }
        
        return model, reasons.get(model, "General purpose model")

