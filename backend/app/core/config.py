from pathlib import Path

# Application settings
BASE_DIR = Path(__file__).resolve().parents[3] # Base directory of the project
APP_NAME = "InterTraceAI"
DIRECTORY_TEST = str(BASE_DIR / "backend" / "test")
SQLITE_DIR = str(BASE_DIR / "backend" / "data" / "sqlite")
SQLITE_URL = f"sqlite:///{BASE_DIR / 'backend' / 'data' / 'sqlite' / 'database.sqlite3'}"
CHROMA_DIR = str(BASE_DIR / "backend" / "data" / "chroma")
LMSTUDIO_BASE_URL = "http://localhost:1234/v1/chat/completions" 
LLM_MODEL = "google/gemma-3-1b"

# RAG and Embedding settings
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
BATCH_SIZE = 32 # Batch size for embedding generation
CHUNK_SIZE = 1500 # Chunk size for text splitting
CHUNK_OVERLAP = 100 # Overlap size for text splitting
MAX_CONTEXT_TOKENS = 1200   # Max tokens for context retrieval
TOP_K = 3 # Number of top documents to retrieve 
USE_NORMALIZE = True # Whether to normalize embeddings
SHOW_PROGRESS = True # Whether to show progress bars
COLLECTION_NAME = "document_embeddings"
CONVERT_TO_NP = True # Whether to convert embeddings to numpy arrays
TEMPERATURE = 0.1 # Default temperature for LLM responses

# Search engine settings
SEARCH_MAX_DEPTH = 3
SEARCH_MAX_DIR_SIZE_MB = 200
ALLOWED_EXTENSIONS = {".pdf"}

# Debug mode
DEBUG_MODE = True

def debug_print(*args, **kwargs):
    if DEBUG_MODE:
        print(*args, **kwargs)
