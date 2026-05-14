"""
Verify GitHub Models auth using Microsoft Foundry Inference SDK.

Usage (PowerShell):
  $Env:GITHUB_TOKEN="<your-token>"
  .\\.venv\\Scripts\\python.exe scripts\\verify_foundry_inference.py

Optional:
  $Env:GITHUB_MODEL="openai/gpt-4.1"
"""

import os
import sys

from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.core.credentials import AzureKeyCredential
from dotenv import load_dotenv


def _resolve_token() -> str | None:
    # Preferred single-token flow from GitHub Models docs.
    return (
        os.getenv("GITHUB_TOKEN")
        or os.getenv("GITHUB_TOKEN_A")
        or os.getenv("GITHUB_TOKEN_B")
    )


def main() -> int:
    load_dotenv()

    endpoint = os.getenv("GITHUB_MODELS_BASE_URL", "https://models.github.ai/inference")
    model = os.getenv("GITHUB_MODEL", "openai/gpt-4.1")
    token = _resolve_token()

    if not token:
        print("ERROR: Missing token. Set GITHUB_TOKEN (preferred) or GITHUB_TOKEN_A/B.")
        return 2

    client = ChatCompletionsClient(
        endpoint=endpoint,
        credential=AzureKeyCredential(token),
    )

    try:
        response = client.complete(
            model=model,
            temperature=0.0,
            top_p=1.0,
            messages=[
                SystemMessage("You are a concise assistant."),
                UserMessage("Reply with exactly: AUTH_OK"),
            ],
        )

        text = (response.choices[0].message.content or "").strip()
        print(f"AUTH_SUCCESS model={model}")
        print(f"RESPONSE: {text}")
        return 0

    except Exception as exc:
        print("AUTH_FAILED")
        print(f"ERROR_TYPE: {type(exc).__name__}")
        print(f"ERROR: {exc}")
        print("HINT: Ensure PAT has models:read permission and is not expired.")
        return 1

    finally:
        client.close()


if __name__ == "__main__":
    raise SystemExit(main())
