from pathlib import Path

# Configuration settings
APP_NAME = "InterTraceAI"
DB_URL = f"sqlite:///{Path('data/sqlite.db').absolute()}"
DIRECTORY_TEST = str(Path("backend/test").absolute())
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
CHROMA_DIR = str(Path("data/chroma").absolute())
UPLOAD_DIR = str(Path("data/uploads").absolute())
LMSTUDIO_BASE_URL = "http://localhost:1234/v1/chat/completions"
MODEL = "google/gemma-3-1b"
BATCH_SIZE = 10
CHUNK_SIZE = 40
CHUNK_OVERLAP = 5
MAX_CONTEXT_CHARS = 4000 # Maximum characters for context
TOP_K = 5 # Number of top results to return

DEBUG_MODE = True

def debug_print(*args, **kwargs):
    if DEBUG_MODE:
        print(*args, **kwargs)