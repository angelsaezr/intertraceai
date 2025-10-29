from pathlib import Path

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from sentence_transformers import SentenceTransformer

import backend.app.core.config as config


class Ingest:
    def __init__(
        self,
        directory=config.DIRECTORY_TEST,
        model_name=config.EMBEDDING_MODEL,
        batch_size=config.BATCH_SIZE, # Batch size for embedding generation
        chunk_size=config.CHUNK_SIZE, # Chunk size for text splitting
        chunk_overlap=config.CHUNK_OVERLAP, # Overlap size for text splitting
        use_normalize=True,
        show_progress=True
    ):
        self.directory = str(Path(directory)) # Convert to string for DirectoryLoader

        # File loader for text files
        self.dir_loader = DirectoryLoader(
            self.directory,
            glob="*.txt",
            loader_cls=TextLoader,
            loader_kwargs={"encoding": "utf8"},
            show_progress=show_progress
        )

        # Load model only once
        self.model = SentenceTransformer(model_name)

        # Configuration parameters
        self.batch_size = batch_size
        self.use_normalize = use_normalize
        self.show_progress = show_progress

        # Optimized text splitter (fewer calls, more speed)
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
        )

    def load_documents(self):
        documents = self.dir_loader.load() # Load all documents from directory
        return documents

    def split_documents(self, documents):
        split_docs = self.text_splitter.split_documents(documents)
        return split_docs

    def generate_embeddings(self, split_docs):
        texts = [d.page_content for d in split_docs]

        embeddings = self.model.encode(
            texts,
            batch_size=self.batch_size,
            show_progress_bar=self.show_progress,
            convert_to_numpy=True, # Convert to numpy array for easier handling
            normalize_embeddings=self.use_normalize
        )

        config.debug_print(f"Embeddings shape: {embeddings.shape}")
        config.debug_print(f"Example first embedding (first 5 values): {embeddings[0][:5]}")
        return embeddings