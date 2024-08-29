import os

from pydantic import BaseModel

class ExternalService(BaseModel):
    ollama_url: str = os.environ.get('OLLAMA_URL', 'http://localhost:11434')

class AppContext(BaseModel):
    log_level: str = "info"
    port: int
