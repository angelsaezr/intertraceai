from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from sentence_transformers import SentenceTransformer

from backend.config import debug_print


class Ingest:
    def __init__(self):
        self.dir_loader = DirectoryLoader( # Directory loader for text files
            r"C:\Users\angel\Proyectos\intertraceai\backend\test",
            glob="*.txt",
            loader_cls=TextLoader,                  # Text file loader
            loader_kwargs={"encoding": "utf8"},     # Loader arguments
            show_progress=True
        )
        self.model = SentenceTransformer("all-MiniLM-L6-v2") # Pre-trained embedding model

    def load_documents(self):
        documents = self.dir_loader.load() # Load documents from directory
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=100, chunk_overlap=0) # Splitter for text chunks
        all_split_docs = text_splitter.split_documents(documents) # Split documents into smaller chunks

        debug_print(f"Loaded and split {len(all_split_docs)} document chunks.")
        return all_split_docs

    def generate_embeddings(self, split_docs):
        embeddings = self.model.encode([d.page_content for d in split_docs]) # Generate embeddings for each text chunk
        debug_print(f"Generated embeddings for {len(embeddings)} chunks.")
        debug_print(embeddings[0])
        return embeddings
    