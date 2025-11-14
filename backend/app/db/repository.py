from typing import Optional

from sqlmodel import Session, select

from app.db.models import Chunk, Document, History


def get_document_by_path(session: Session, path: str) -> Optional[Document]:
    statement = select(Document).where(Document.path == path)
    return session.exec(statement).first()

def create_document(session: Session, name: str, path: str) -> Document:
    doc = Document(name=name, path=path)
    session.add(doc)
    session.commit()
    session.refresh(doc)
    return doc

def create_chunk(session: Session, document_id: int, chroma_id: str, text: str, order: int):
    chunk = Chunk(
        document_id=document_id,
        chroma_id=chroma_id,
        text=text,
        order=order
    )
    session.add(chunk)
    session.commit()
    session.refresh(chunk)
    return chunk

def create_history(session: Session, query: str, response: str) -> History:
    h = History(query=query, response=response)
    session.add(h)
    session.commit()
    session.refresh(h)
    return h

def list_documents(session: Session):
    return session.exec(select(Document)).scalars().all()
