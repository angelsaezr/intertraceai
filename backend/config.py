from pathlib import Path

# Configuration settings for the application
APP_NAME = "InterTraceAI"
DB_URL = f"sqlite:///{Path('data/sqlite.db').absolute()}"
CHROMA_DIR = str(Path("data/chroma").absolute())
UPLOAD_DIR = str(Path("data/uploads").absolute())
LMSTUDIO_BASE_URL = "http://localhost:1234/v1/chat/completions"
LMSTUDIO_MODEL = "google/gemma-3-1b"
MAX_CONTEXT_CHARS = 4000
TOP_K = 5