from typing import Optional

from sqlmodel import Session, delete, select

from app.db.models import Chunk, Document


def get_document_by_path(session: Session, path: str) -> Optional[Document]:
    statement = select(Document).where(Document.path == path)
    return session.exec(statement).first()


def create_document(session: Session, name: str, path: str) -> Document:
    doc = Document(name=name, path=path)
    session.add(doc)
    session.commit()
    session.refresh(doc)
    return doc


def create_chunk(
    session: Session,
    document_id: int,
    chroma_id: str,
    text: str,
    order: int,
) -> Chunk:
    chunk = Chunk(
        document_id=document_id,
        chroma_id=chroma_id,
        text=text,
        order=order,
    )
    session.add(chunk)
    session.commit()
    session.refresh(chunk)
    return chunk


def list_documents(session: Session) -> list[Document]:
    return session.exec(select(Document)).all()


def delete_all_chunks(session: Session) -> None:
    session.exec(delete(Chunk))
    session.commit()


def delete_all_documents(session: Session) -> None:
    session.exec(delete(Document))
    session.commit()