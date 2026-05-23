from pathlib import Path

from sentence_transformers import SentenceTransformer
from sqlmodel import Session

import app.core.config as config
from app.db import repository
from app.db.chromadb import client
from app.services.rag.generator import Generator
from app.services.rag.ingest import Ingest
from app.services.rag.retriever import Retriever


class Pipeline:

    def __init__(self):
        shared_model = SentenceTransformer(config.EMBEDDING_MODEL)
        config.debug_print(f"[Pipeline] Loaded embedding model: {config.EMBEDDING_MODEL}")

        self.ingester = Ingest(model=shared_model)
        self.retriever = Retriever(model=shared_model)
        self.generator = Generator(retriever=self.retriever)

    def reset_ingestion(self, session: Session) -> None:
        try:
            client.delete_collection(name=config.COLLECTION_NAME)
            config.debug_print("[Reset] Chroma collection deleted.")
        except Exception as e:
            config.debug_print(f"[Reset] Chroma delete skipped: {e}")

        client.get_or_create_collection(name=config.COLLECTION_NAME)
        config.debug_print("[Reset] Chroma collection recreated.")

        repository.delete_all_chunks(session)
        repository.delete_all_documents(session)
        config.debug_print("[Reset] SQLite cleared (chunks, documents).")

    def ingest(self, file_paths: list[str], session: Session):
        db_documents = []
        docs_to_process = []

        existing_count = len(repository.list_documents(session))

        for path in file_paths:
            if existing_count + len(db_documents) >= config.MAX_DOCUMENTS:
                config.debug_print("[Ingest] Limit reached, stopping.")
                break

            size_mb = Path(path).stat().st_size / (1024 * 1024)
            if size_mb > config.MAX_PDF_SIZE_MB:
                config.debug_print(f"[Ingest] '{path}' too large ({size_mb:.1f} MB), skipping.")
                continue

            if repository.get_document_by_path(session, path):
                config.debug_print(f"[Ingest] '{path}' already exists, skipping.")
                continue

            for doc in self.ingester.load_from_paths([path]):
                docs_to_process.append(doc)

            db_doc = repository.create_document(
                session=session,
                name=Path(path).name,
                path=path
            )
            db_documents.append(db_doc)

        if not docs_to_process:
            config.debug_print("[Ingest] No new documents.")
            return [], []

        split_docs = self.ingester.split_documents(docs_to_process)
        embeddings = self.ingester.generate_embeddings(split_docs)
        self.ingester.save_to_db(
            embeddings=embeddings,
            split_docs=split_docs,
            db_session=session,
            db_documents=db_documents
        )
        return split_docs, embeddings

    async def query(self, user_query: str) -> dict:
        return await self.generator.generate(user_query)