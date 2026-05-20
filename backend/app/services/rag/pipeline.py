from pathlib import Path

from sqlmodel import Session

import app.core.config as config
from app.db import repository
from app.db.chromadb import client
from app.services.rag.generator import Generator
from app.services.rag.ingest import Ingest


class Pipeline:
    def __init__(self):
        self.ingest = Ingest()
        self.generator = Generator()

    def reset_ingestion(self, session: Session):
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

    def run(self, file_paths: list[str], session: Session):
        documents = self.ingest.load_from_paths(file_paths)

        docs_by_source = {}
        for doc in documents:
            source = doc.metadata.get("source")
            docs_by_source.setdefault(source, []).append(doc)

        db_documents = []
        docs_to_process = []

        for source, docs_for_source in docs_by_source.items():
            existing = repository.get_document_by_path(session, source)

            if existing:
                config.debug_print(f"[Ingest] '{source}' already exists, skipping.")
                continue

            db_doc = repository.create_document(
                session=session,
                name=Path(source).name,
                path=source
            )
            db_documents.append(db_doc)

            docs_to_process.extend(docs_for_source)

        if not docs_to_process:
            config.debug_print("[Ingest] No new documents.")
            return [], []

        split_docs = self.ingest.split_documents(docs_to_process)
        embeddings = self.ingest.generate_embeddings(split_docs)

        self.ingest.save_to_db(
            embeddings=embeddings,
            split_docs=split_docs,
            db_session=session,
            db_documents=db_documents
        )

        return split_docs, embeddings

    async def query(self, user_query: str, session: Session):
        result = await self.generator.generate(user_query)
        return result
