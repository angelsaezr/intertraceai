from pathlib import Path

# Configuration settings
APP_NAME = "InterTraceAI"
DB_URL = f"sqlite:///{Path('data/sqlite.db').absolute()}"
CHROMA_DIR = str(Path("data/chroma").absolute())
UPLOAD_DIR = str(Path("data/uploads").absolute())
LMSTUDIO_BASE_URL = "http://localhost:1234/v1/chat/completions"
LMSTUDIO_MODEL = "google/gemma-3-1b"
MAX_CONTEXT_CHARS = 4000 # Maximum characters for context
TOP_K = 5 # Number of top results to return

DEBUG_MODE = True

def debug_print(*args, **kwargs):
    if DEBUG_MODE:
        print(*args, **kwargs)