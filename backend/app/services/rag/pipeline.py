from pathlib import Path

from sqlmodel import Session

from app.db import repository
from app.services.rag.generator import Generator
from app.services.rag.ingest import Ingest


class Pipeline:
    def __init__(self):
        self.ingest = Ingest()
        self.generator = Generator()

    def run(self, file_paths: list[str], session: Session):
        documents = self.ingest.load_from_paths(file_paths)

        db_documents = []
        for doc in documents:
            source = doc.metadata.get("source")
            db_doc = repository.create_document(
                session=session,
                name=Path(source).name,
                path=source
            )
            db_documents.append(db_doc)

        split_docs = self.ingest.split_documents(documents)
        embeddings = self.ingest.generate_embeddings(split_docs)

        self.ingest.save_to_db(
            embeddings=embeddings,
            split_docs=split_docs,
            db_session=session,
            db_documents=db_documents
        )
        return split_docs, embeddings

    async def query(self, user_query: str, session: Session):
        response = await self.generator.generate(user_query)
        repository.create_history(session, user_query, response)
        return response
