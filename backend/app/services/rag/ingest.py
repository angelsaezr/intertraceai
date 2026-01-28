import uuid
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import (
    PyMuPDFLoader,
)
from sentence_transformers import SentenceTransformer

import app.core.config as config
from app.db import repository
from app.db.chromadb import collection


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

        # Connect to Chroma vector database
        self.collection = collection

        # Optimized text splitter (fewer calls, more speed)
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=config.CHUNK_SIZE, # Chunk size for text splitting
            chunk_overlap=config.CHUNK_OVERLAP,
        )

    def load_from_paths(self, file_paths):
        """
        Load documents from given file paths.

        param file_paths: List of file paths to load
        return: List of loaded documents
        """

        def load(path):
            try:
                ext = Path(path).suffix.lower()
                if ext == ".pdf":
                    loader = PyMuPDFLoader(path)
                else:
                    return []
                return loader.load()
            except Exception as e:
                config.debug_print(f"Error loading {path}: {e}")
                return []

        documents = []
        
        # Use ThreadPoolExecutor for concurrent loading
        with ThreadPoolExecutor(max_workers=4) as executor:
            results = executor.map(load, file_paths)

        for docs in results:
            documents.extend(docs)

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

    def save_to_db(self, embeddings, split_docs, db_session, db_documents):
        
        documents_text = [d.page_content for d in split_docs]
        metadatas = [{"source": d.metadata.get("source", "unknown")} for d in split_docs]
        ids = [f"{Path(meta['source']).stem}_{uuid.uuid4()}" for meta in metadatas]

        # Save to Chroma
        self.collection.add(
            embeddings=embeddings,
            documents=documents_text,
            metadatas=metadatas,
            ids=ids
        )

        # Save chunks to SQLite
        source_to_docid = {doc.path: doc.id for doc in db_documents}

        for order, (cid, text, meta) in enumerate(zip(ids, documents_text, metadatas)):
            source = meta["source"]
            doc_id = source_to_docid.get(source)

            repository.create_chunk(
                session=db_session,
                document_id=doc_id,
                chroma_id=cid,
                text=text,
                order=order
            )

if __name__ == "__main__":
    ingest = Ingest()
    documents = ingest.load_documents()
    split_docs = ingest.split_documents(documents)
    embeddings = ingest.generate_embeddings(split_docs)
    ingest.save_to_db(embeddings, split_docs)