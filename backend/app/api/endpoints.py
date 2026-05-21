from contextlib import asynccontextmanager

from fastapi import APIRouter, Depends, FastAPI
from pydantic import BaseModel
from sqlmodel import Session

from app.db import repository
from app.db.session import get_session, init_db
from app.services.rag.pipeline import Pipeline
from app.services.search.engine import Engine

_pipeline: Pipeline | None = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global _pipeline
    init_db()
    _pipeline = Pipeline()
    yield


def get_pipeline() -> Pipeline:
    assert _pipeline is not None, "Pipeline not initialized"
    return _pipeline

app = APIRouter()


class QueryRequest(BaseModel):
    question: str


class QueryResponse(BaseModel):
    answer: str
    sources: list[str] = []


@app.get("/")
async def root():
    return {"message": "Welcome to the InterTraceAI API"}


@app.get("/documents", tags=["Documents"])
def get_documents(session: Session = Depends(get_session)):
    return repository.list_documents(session)


@app.post("/search", tags=["Search"])
async def search():
    engine = Engine()
    docs = engine.search()
    return {"message": docs}


@app.post("/ingest", tags=["Pipeline"])
async def ingest(
    session: Session = Depends(get_session),
    pipeline: Pipeline = Depends(get_pipeline),
):
    engine = Engine()
    file_paths = engine.search()
    split_docs, embeddings = pipeline.ingest(file_paths, session)
    return {
        "message": "Pipeline run successfully",
        "documents_loaded": len(split_docs),
        "embeddings_generated": len(embeddings),
    }


@app.post("/ingest/reset", tags=["Pipeline"])
async def reset_and_ingest(
    session: Session = Depends(get_session),
    pipeline: Pipeline = Depends(get_pipeline),
):
    pipeline.reset_ingestion(session=session)
    engine = Engine()
    file_paths = engine.search()
    split_docs, embeddings = pipeline.ingest(file_paths, session)
    return {
        "message": "Ingest completed",
        "documents_loaded": len(split_docs),
        "embeddings_generated": len(embeddings),
    }


@app.post("/query", tags=["Pipeline"], response_model=QueryResponse)
async def query_pipeline(request: QueryRequest, pipeline: Pipeline = Depends(get_pipeline)):
    result = await pipeline.query(request.question)
    return QueryResponse(answer=result["answer"], sources=result["sources"])