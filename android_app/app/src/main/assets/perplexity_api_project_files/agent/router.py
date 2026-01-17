
class Router:
    def pick(self,task):
        t=task.lower()
        if "design" in t or "arch" in t:
            return "sonar-large"
        if "test" in t or "debug" in t:
            return "llama-3"
        return "mistral-7b-instruct"
