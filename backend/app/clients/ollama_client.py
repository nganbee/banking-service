import requests
from typing import Any, List, Dict, Optional, Union
from app.clients.base import BaseModelClient
from app.core.settings import settings

class OllamaClient(BaseModelClient):
    def __init__(self, base_url: Optional[str] = None):
        self.base_url = base_url or settings.OLLAMA_BASE_URL
        self.generate_url = f"{self.base_url}/api/generate"
        self.chat_url = f"{self.base_url}/api/chat"

    def generate(
        self, 
        model: str, 
        prompt: str, 
        system_prompt: Optional[str] = None,
        return_full: bool = False, 
        **kwargs: Any
    ) -> Union[str, Dict[str, Any]]:

        payload = {
            "model": model,
            "prompt": prompt,
            "stream": False,
            "logprobs": True if return_full else False,
        }
        
        if kwargs.get("options"):
            payload["options"] = kwargs["options"]
        
        if system_prompt:
            payload["system"] = system_prompt

        try:
            response = requests.post(self.generate_url, json=payload, timeout=kwargs.get("timeout", 300))
            response.raise_for_status()
            res_json = response.json()

            if return_full:
                return {
                    "text": res_json.get("response", "").strip(),
                    "logprobs": res_json.get("logprobs", [])
                }
            
            return res_json.get("response", "").strip()
        
        except requests.exceptions.RequestException as e:
            print(f"Ollama Generate Error: {e}")
            return f"Error: Could not connect to Ollama for model {model}."

    def chat(
        self, 
        model: str, 
        messages: List[Dict[str, str]], 
        **kwargs: Any
    ) -> str:

        payload = {
            "model": model,
            "messages": messages,
            "stream": False,
            "options": kwargs.get("options", {})
        }

        try:
            response = requests.post(self.chat_url, json=payload, timeout=kwargs.get("timeout", 300))
            response.raise_for_status()
            return response.json().get("message", {}).get("content", "").strip()
        except requests.exceptions.RequestException as e:
            print(f"Ollama Chat Error: {e}")
            return f"Error: Chat failed for model {model}."

ollama_client = OllamaClient()