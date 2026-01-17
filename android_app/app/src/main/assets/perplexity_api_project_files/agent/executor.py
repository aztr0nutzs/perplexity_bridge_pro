
import requests

class Executor:
    def __init__(self,bridge,secret):
        self.bridge=bridge
        self.secret=secret

    def run(self,task,model):
        body={
         "model":model,
         "messages":[{"role":"user","content":task}]
        }
        r=requests.post(self.bridge+"/v1/chat/completions",
         headers={"X-API-KEY":self.secret},
         json=body)
        return r.json()["choices"][0]["message"]["content"]
