import json
import ollama


def query_ollama_llm(prompt: str, model: str = "llama32") -> dict:
    response = ollama.generate(model=model, prompt=prompt)
    return json.loads(response["response"])

