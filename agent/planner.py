
import requests

class Planner:
    def __init__(self,bridge,secret,model):
        self.bridge=bridge
        self.secret=secret
        self.model=model

    def plan(self,goal):
        prompt=f"You are a senior architect. Break into JSON steps: {goal}"
        body={
          "model":self.model,
          "messages":[{"role":"user","content":prompt}]
        }
        r=requests.post(self.bridge+"/v1/chat/completions",
         headers={"X-API-KEY":self.secret},
         json=body)
        return r.json()["choices"][0]["message"]["content"]
