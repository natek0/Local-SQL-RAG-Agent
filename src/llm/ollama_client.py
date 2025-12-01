import requests
import json
from typing import Dict, Any, Optional

class OllamaHandler:
    """
    A custom implementation of an LLM client that interfaces directly with 
    the local Ollama instance via REST API.
    """
    
    def __init__(self, model: str = "llama3", base_url: str = "http://localhost:11434"):
        self.model = model
        self.base_url = base_url
        self.api_endpoint = f"{base_url}/api/generate"

    def complete(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        """
        Sends a raw POST request to the Ollama API.
        """
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.1,  # Low temperature for deterministic SQL
                "num_predict": 512
            }
        }
        
        if system_prompt:
            payload["system"] = system_prompt

        try:
            response = requests.post(
                self.api_endpoint, 
                json=payload, 
                headers={"Content-Type": "application/json"}
            )
            response.raise_for_status()
            return response.json().get("response", "").strip()
            
        except requests.exceptions.RequestException as e:
            raise ConnectionError(f"Failed to connect to Ollama at {self.base_url}: {e}")

if __name__ == "__main__":
    llm = OllamaHandler()
    print("Testing connection...")
    try:
        res = llm.complete("Say 'System Ready' if you can hear me.")
        print(f"Ollama Response: {res}")
    except Exception as e:
        print(f"Error: {e}")
