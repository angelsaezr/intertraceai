from datetime import datetime, timezone

from sqlmodel import Field, Relationship, SQLModel


class Chunk(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    document_id: int = Field(foreign_key="document.id")
    chroma_id: str
    text: str
    order: int
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    document: "Document" = Relationship(back_populates="chunks")

class Document(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    path: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    chunks: list["Chunk"] = Relationship(back_populates="document")

class History(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    query: str
    response: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
