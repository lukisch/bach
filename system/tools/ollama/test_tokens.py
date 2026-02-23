# SPDX-License-Identifier: MIT
import json
import requests

def test_ollama_tokens():
    url = "http://localhost:11434/api/generate"
    payload = {
        "model": "llama3.2",
        "prompt": "Say hello in one word",
        "stream": False
    }
    
    try:
        response = requests.post(url, json=payload, timeout=30)
        if response.status_code == 200:
            data = response.json()
            print(f"Response: {data.get('response')}")
            print(f"Prompt Tokens: {data.get('prompt_eval_count')}")
            print(f"Response Tokens: {data.get('eval_count')}")
            print(f"Total Duration: {data.get('total_duration')}")
        else:
            print(f"Error: {response.status_code}")
    except Exception as e:
        print(f"Exception: {e}")

if __name__ == "__main__":
    test_ollama_tokens()
