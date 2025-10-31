from pathlib import Path

# Application settings
BASE_DIR = Path(__file__).resolve().parents[3] # Base directory of the project
APP_NAME = "InterTraceAI"
DIRECTORY_TEST = str(BASE_DIR / "backend" / "test")
SQLITE_DIR = str(BASE_DIR / "backend" / "data" / "sqlite")
SQLITE_URL = f"sqlite:///{BASE_DIR / 'backend' / 'data' / 'sqlite' / 'database.db'}"
CHROMA_DIR = str(BASE_DIR / "backend" / "data" / "chroma")
LMSTUDIO_BASE_URL = "http://localhost:1234/v1/chat/completions"
LLM_MODEL = "google/gemma-3-1b"

# RAG and Embedding settings
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
BATCH_SIZE = 10 # Batch size for embedding generation
CHUNK_SIZE = 300 # Chunk size for text splitting
CHUNK_OVERLAP = 50 # Overlap size for text splitting
MAX_CONTEXT_CHARS = 800 # Max characters for context retrieval
TOP_K = 5 # Number of top documents to retrieve 

# Debug mode
DEBUG_MODE = True

def debug_print(*args, **kwargs):
    if DEBUG_MODE:
        print(*args, **kwargs)
