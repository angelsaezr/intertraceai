import uuid
from pathlib import Path

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyMuPDFLoader
from sentence_transformers import SentenceTransformer

import app.core.config as config
from app.db import repository
from app.db.chromadb import get_collection


class Ingest:
    """
    Document Ingestion and Embedding Generation.
    """

    def __init__(self, model: SentenceTransformer):
        self.model = model

        self.batch_size = config.BATCH_SIZE
        self.use_normalize = config.USE_NORMALIZE
        self.show_progress = config.SHOW_PROGRESS

        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=config.CHUNK_SIZE,
            chunk_overlap=config.CHUNK_OVERLAP,
        )

    def load_from_paths(self, file_paths: list[str]):
        for path in file_paths:
            try:
                ext = Path(path).suffix.lower()
                if ext == ".pdf":
                    loader = PyMuPDFLoader(path)
                else:
                    continue
                for doc in loader.load():
                    yield doc
            except Exception as e:
                config.debug_print(f"Error loading {path}: {e}")

    def split_documents(self, documents):
        return self.text_splitter.split_documents(documents)

    def generate_embeddings(self, split_docs):
        texts = [d.page_content for d in split_docs]
        embeddings = self.model.encode(
            texts,
            batch_size=self.batch_size,
            show_progress_bar=self.show_progress,
            convert_to_numpy=True,
            normalize_embeddings=self.use_normalize
        )
        config.debug_print(f"Embeddings shape: {embeddings.shape}")
        config.debug_print(f"Example first embedding (first 5 values): {embeddings[0][:5]}")
        return embeddings

    def save_to_db(self, embeddings, split_docs, db_session, db_documents):
        documents_text = [d.page_content for d in split_docs]
        metadatas = [{"source": d.metadata.get("source", "unknown")} for d in split_docs]
        ids = [f"{Path(meta['source']).stem}_{uuid.uuid4()}" for meta in metadatas]

        get_collection().add(
            embeddings=embeddings,
            documents=documents_text,
            metadatas=metadatas,
            ids=ids
        )

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