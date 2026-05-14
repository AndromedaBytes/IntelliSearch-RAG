import sys
from pathlib import Path

from pydantic import BaseModel, ValidationError
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application Configuration"""
    
    # GitHub Models API Keys
    GITHUB_TOKEN: str | None = None
    GITHUB_TOKEN_A: str | None = None
    GITHUB_TOKEN_B: str | None = None
    GITHUB_MODELS_BASE_URL: str = "https://models.github.ai/inference"
    
    # ChromaDB Configuration
    CHROMA_PERSIST_DIR: str = "./chroma_storage"
    CHROMA_COLLECTION_NAME: str = "intellisearch_v2_corpus"
    
    # Security
    CLIENT_KEY: str
    NEXT_PUBLIC_CLIENT_KEY: str = ""
    
    # Model Names
    GPT4O_MODEL: str = "gpt-4o"
    LLAMA_MODEL: str = "Meta-Llama-3.1-405B-Instruct"
    
    # Retrieval Parameters
    TOP_K_RETRIEVAL: int = 15
    SIMILARITY_THRESHOLD: float = 0.70
    
    # Chunking Parameters
    CHUNK_SIZE: int = 512
    CHUNK_OVERLAP: int = 64

    def model_post_init(self, __context) -> None:
        """Allow either one shared token or separate model tokens."""
        if self.GITHUB_TOKEN and not self.GITHUB_TOKEN_A:
            self.GITHUB_TOKEN_A = self.GITHUB_TOKEN
        if self.GITHUB_TOKEN and not self.GITHUB_TOKEN_B:
            self.GITHUB_TOKEN_B = self.GITHUB_TOKEN

        if not self.GITHUB_TOKEN_A or not self.GITHUB_TOKEN_B:
            raise ValueError(
                "Set GITHUB_TOKEN, or set both GITHUB_TOKEN_A and GITHUB_TOKEN_B in .env"
            )
    
    model_config = SettingsConfigDict(env_file=str(Path(__file__).resolve().parents[2] / ".env"))


def _resolve_env_file() -> str | None:
    """Find a usable .env file in source or packaged layouts."""
    candidates = []

    if getattr(sys, "frozen", False):
        candidates.append(Path(sys.executable).resolve().parent / ".env")
        candidates.append(Path(sys._MEIPASS) / ".env")

    candidates.append(Path(__file__).resolve().parents[2] / ".env")
    candidates.append(Path.cwd() / ".env")

    for candidate in candidates:
        if candidate.exists():
            return str(candidate)

    return None

try:
    env_file = _resolve_env_file()
    if env_file:
        Settings.model_config["env_file"] = env_file
    settings = Settings()
    if not settings.NEXT_PUBLIC_CLIENT_KEY:
        settings.NEXT_PUBLIC_CLIENT_KEY = settings.CLIENT_KEY
except ValidationError:
    if "pytest" in sys.modules:
        settings = Settings.model_validate(
            {
                "GITHUB_TOKEN": "test-token",
                "GITHUB_TOKEN_A": "test-token-a",
                "GITHUB_TOKEN_B": "test-token-b",
                "CLIENT_KEY": "test-key",
                "NEXT_PUBLIC_CLIENT_KEY": "test-key",
            }
        )
    else:
        raise
