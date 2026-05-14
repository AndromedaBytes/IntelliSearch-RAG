"""
Ask the same question to two models (GitHub Models + Llama) via Foundry SDK

Usage:
  $Env:GITHUB_TOKEN="..." ; .\.venv\Scripts\python.exe scripts\ask_models.py

Outputs labeled answers per model.
"""

import os
from dotenv import load_dotenv
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.core.credentials import AzureKeyCredential


def resolve_token():
    return os.getenv("GITHUB_TOKEN") or os.getenv("GITHUB_TOKEN_A") or os.getenv("GITHUB_TOKEN_B")


def ask_model(client, model, prompt):
    resp = client.complete(
        model=model,
        messages=[SystemMessage("You are a concise assistant."), UserMessage(prompt)],
        temperature=0.0,
        top_p=1.0,
        max_tokens=512,
    )
    return (resp.choices[0].message.content or "").strip()


def main():
    load_dotenv()
    token = resolve_token()
    if not token:
        print("ERROR: No token found. Set GITHUB_TOKEN or GITHUB_TOKEN_A/B in .env or env.")
        return 2

    endpoint = os.getenv("GITHUB_MODELS_BASE_URL", "https://models.github.ai/inference")
    models = [
        os.getenv("GITHUB_MODEL", "openai/gpt-4.1"),
        os.getenv("GITHUB_LLAMA_MODEL", "meta/Meta-Llama-3.1-405B-Instruct"),
    ]

    prompt = os.getenv("ASK_PROMPT", "Who is the president of the United Kingdom?")

    client = ChatCompletionsClient(endpoint=endpoint, credential=AzureKeyCredential(token))

    try:
        for m in models:
            try:
                answer = ask_model(client, m, prompt)
                print(f"--- MODEL: {m} ---")
                print(answer)
                print()
            except Exception as e:
                print(f"--- MODEL: {m} ERROR ---")
                print(type(e).__name__, e)
                print()
    finally:
        client.close()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
