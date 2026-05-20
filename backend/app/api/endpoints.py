
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlmodel import Session

from app.db import repository
from app.db.session import get_session, init_db
from app.services.rag.pipeline import Pipeline
from app.services.search.engine import Engine

app = APIRouter()

# Models
class Document(BaseModel):
    name: str

class QueryRequest(BaseModel):
    question: str

class QueryResponse(BaseModel):
    answer: str
    sources: list[str] = []

# Endpoints

app.add_event_handler("startup", init_db)

@app.get("/")
async def root():
    return {"message": "Welcome to the InterTraceAI API"}

@app.get("/documents", tags=["Documents"])
def get_documents(session: Session = Depends(get_session)):
    docs = repository.list_documents(session)
    return docs

@app.post("/search", tags=["Search"])
async def search():
    """
    Perform a search.
    """
    engine = Engine()
    docs = engine.search()
    return {"message": [doc for doc in docs]}

@app.post("/ingest", tags=["Pipeline"])
async def ingest(session: Session = Depends(get_session)):
    pipeline = Pipeline()
    engine = Engine()
    file_paths = engine.search()
    split_docs, embeddings = pipeline.run(file_paths, session)
    return {
        "message": "Pipeline run successfully",
        "documents_loaded": len(split_docs),
        "embeddings_generated": len(embeddings)
    }

@app.post("/ingest/reset", tags=["Pipeline"])
async def reset_and_ingest(session: Session = Depends(get_session)):
    pipeline = Pipeline()

    pipeline.reset_ingestion(session=session, clear_history=False)

    engine = Engine()
    file_paths = engine.search()
    split_docs, embeddings = pipeline.run(file_paths, session)

    return {
        "message": "Ingest completed",
        "documents_loaded": len(split_docs),
        "embeddings_generated": len(embeddings),
    }

@app.post("/query", tags=["Pipeline"], response_model=QueryResponse)
async def query_pipeline(request: QueryRequest, session: Session = Depends(get_session)):
    pipeline = Pipeline()
    result = await pipeline.query(request.question, session)
    return QueryResponse(answer=result["answer"], sources=result["sources"])
