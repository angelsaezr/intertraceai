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
USE_NORMALIZE = True # Whether to normalize embeddings
SHOW_PROGRESS = True # Whether to show progress bars
COLLECTION_NAME = "document_embeddings"
CONVERT_TO_NP = True # Whether to convert embeddings to numpy arrays
TEMPERATURE = 0.7 # Default temperature for LLM responses

# Search engine settings
SEARCH_MAX_DEPTH = 500
SEARCH_MAX_DIR_SIZE_MB = 999999999999
EXCLUDED_FOLDERS = {
    # --- Windows  ---
    r"C:\Windows",
    r"C:\Program Files",
    r"C:\Program Files (x86)",
    r"C:\ProgramData",
    r"C:\Recovery",
    r"C:\$Recycle.Bin",
    r"C:\System Volume Information",
    r"AppData",
    r"Contacts",
    r"Favorites",
    r"Searches",
    r"Application Data",
    r"Cookies",
    r"Recent",
    r"SendTo",
    r"Start Menu",
    r"Videos\Captures",
    r"Saved Games",
    r"MicrosoftEdgeBackups",
    r"OneDrive\~tmp",
    r"NTUSER.DAT",
    r"node_modules",

    # --- Linux  ---
    "/bin",
    "/sbin",
    "/boot",
    "/dev",
    "/proc",
    "/sys",
    "/run",
    "/lib",
    "/lib64",
    "/var",
    "/usr",
    "~/.cache",
    "~/.config",
    "~/.local/share",
    "~/.mozilla",
    "~/.vscode",
}

# Debug mode
DEBUG_MODE = True

def debug_print(*args, **kwargs):
    if DEBUG_MODE:
        print(*args, **kwargs)
