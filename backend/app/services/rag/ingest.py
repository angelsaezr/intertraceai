from pathlib import Path

from chromadb import PersistentClient
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import (
    PyPDFLoader,
    UnstructuredWordDocumentLoader,
)
from sentence_transformers import SentenceTransformer

import app.core.config as config


class Ingest:
    """
    Document Ingestion and Embedding Generation
    """

    def __init__(self):
        """
        Initialize the ingestion pipeline.
        """

        # Load model
        self.model = SentenceTransformer(config.EMBEDDING_MODEL)

        # Configuration parameters
        self.batch_size = config.BATCH_SIZE # Batch size for embedding generation
        self.use_normalize = config.USE_NORMALIZE
        self.show_progress = config.SHOW_PROGRESS

        # Optimized text splitter (fewer calls, more speed)
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=config.CHUNK_SIZE, # Chunk size for text splitting
            chunk_overlap=config.CHUNK_OVERLAP,
        )

    def load_from_paths(self, file_paths: list[str]):
        """
        Load documents from a list of file paths.

        param file_paths: List of file paths to load
        return: List of loaded documents
        """
        documents = []

        for path in file_paths:
            ext = Path(path).suffix.lower() # Get file extension in lowercase
            try:
                if ext == ".pdf":
                    loader = PyPDFLoader(path)
                elif ext == ".docx":
                    loader = UnstructuredWordDocumentLoader(path)
                else:
                    # Skip unsupported formats
                    continue

                docs = loader.load() # Load documents from the file
                documents.extend(docs) # Add loaded documents to the list

            except Exception as e:
                config.debug_print(f"Error loading {path}: {e}")
                continue

        return documents

    def split_documents(self, documents):
        """
        Split documents into smaller chunks.

        param documents: List of documents to split
        return: List of split document chunks
        """

        split_docs = self.text_splitter.split_documents(documents)
        return split_docs

    def generate_embeddings(self, split_docs):
        """
        Generate embeddings for the split document chunks.

        param split_docs: List of split document chunks
        return: Numpy array of document embeddings
        """

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

    def save_to_vector_db(self, embeddings, split_docs):
        """
        Save document embeddings to the vector database.

        param embeddings: Numpy array of document embeddings
        param split_docs: List of split document chunks
        """

        # Initialize Chroma client
        client = PersistentClient(path=config.CHROMA_DIR)

        # Create or get a collection for document embeddings
        collection = client.get_or_create_collection(name="document_embeddings")

        # Prepare data for insertion
        documents = [d.page_content for d in split_docs]
        ids = [f"doc_{i}" for i in range(len(documents))]  # Unique IDs for each document
        metadatas = [{"source": d.metadata.get("source", "unknown")} for d in split_docs]

        # Add embeddings to the collection
        collection.add(embeddings=embeddings, documents=documents, metadatas=metadatas, ids=ids)

        config.debug_print(f"Saved {len(embeddings)} embeddings to Chroma DB")

if __name__ == "__main__":
    ingest = Ingest()
    documents = ingest.load_documents()
    split_docs = ingest.split_documents(documents)
    embeddings = ingest.generate_embeddings(split_docs)
    ingest.save_to_vector_db(embeddings, split_docs)