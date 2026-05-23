from pydantic_settings import BaseSettings
from pathlib import Path

_BASE_DIR = Path(__file__).resolve().parent.parent.parent

class Settings(BaseSettings):
    # Ollama Configuration
    OLLAMA_BASE_URL: str
    
    # Models
    GENERATION_MODEL: str = "gpt-oss:20b" 
    FINETUNED_MODEL: str = "banking-intent"
    
    # Finetuned intent model
    INTENT_MODEL_PATH: str = "imbee510/bank-intent-qwen-unsloth"

    # Project Paths
    BASE_DIR: Path = _BASE_DIR
    
    # App Settings
    APP_NAME: str = "Banking Agentic"
    DEBUG: bool = True

    class Config:
        env_file = _BASE_DIR / ".env"
        
settings = Settings()