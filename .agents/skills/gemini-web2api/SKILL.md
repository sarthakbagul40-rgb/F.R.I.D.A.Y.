---
name: gemini-web2api
description: Access Google Gemini Web reverse-engineered API on localhost:8081 for OpenAI-compatible completions, massive context windows, and Google web search grounding.
---

# Gemini-Web2API Bridge

This skill provides access to the local `gemini-web2api` daemon running on `http://localhost:8081/v1`.

## Capabilities
- **Models Available:**
  - `gemini-auto`: Intelligent automatic model selection
  - `gemini-3.7-flash`: Flagship fast reasoning model
  - `gemini-3.6-flash`: High-speed general assistant
  - `gemini-3.5-flash-thinking`: Deep chain-of-thought thinking mode
  - `gemini-3.1-pro`: Advanced reasoning and coding
- **Endpoint:** `http://localhost:8081/v1/chat/completions` (OpenAI format)
- **Features:** Streaming SSE, multimodal image inputs, Google search grounding, and zero API cost.

## Usage Example (Python)
```python
import requests

payload = {
    "model": "gemini-auto",
    "messages": [
        {"role": "user", "content": "Explain quantum computing in simple terms"}
    ]
}

response = requests.post("http://localhost:8081/v1/chat/completions", json=payload)
print(response.json()["choices"][0]["message"]["content"])
```
