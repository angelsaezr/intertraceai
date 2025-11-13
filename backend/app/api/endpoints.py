import traceback

import httpx
from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect
from pydantic import BaseModel
from sqlmodel import Session

import app.core.config as config
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

# Endpoints

app.add_event_handler("startup", init_db)

@app.get("/")
async def root():
    return {"message": "Welcome to the InterTraceAI API"}

@app.get("/documents", tags=["Documents"])
def get_documents(session: Session = Depends(get_session)):
    docs = repository.list_documents(session)
    return docs

@app.post("/documents/upload", tags=["Documents"])
async def upload_document(document: Document):
    """
    Add a new document to the database.
    """

    return {"message": "Document added successfully"}

@app.delete("/documents/{doc_id}", tags=["Documents"])
async def delete_document(doc_id: str):
    """
    Delete a document from the database.
    """
    return {"message": f"Document {doc_id} deleted successfully."}

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

@app.post("/query", tags=["Pipeline"], response_model=QueryResponse)
async def query_pipeline(request: QueryRequest, session: Session = Depends(get_session)):
    pipeline = Pipeline()
    answer = await pipeline.query(request.question, session)
    return QueryResponse(answer=answer)

@app.websocket("/chat")
async def chat(websocket: WebSocket):
    await websocket.accept()
    conversation = []

    async with httpx.AsyncClient(timeout=httpx.Timeout(60.0)) as client:
        try:
            while True:
                try:
                    user_message = await websocket.receive_text()
                    print(f"SERVER: User message: {user_message}")

                    # Add user message to conversation history
                    conversation.append({"role": "user", "content": user_message})

                    payload = {
                        "model": config.LLM_MODEL,
                        "messages": conversation,
                        "temperature": 0.7,
                        "stream": False
                    }

                    response = await client.post(config.LMSTUDIO_BASE_URL, json=payload)
                    response.raise_for_status()
                    data = response.json()

                    model_reply = data["choices"][0]["message"]["content"]

                    conversation.append({"role": "assistant", "content": model_reply})

                    await websocket.send_text(model_reply)

                except WebSocketDisconnect:
                    print("SERVER: WebSocket disconnected")
                    break
                except httpx.ReadTimeout:
                    await websocket.send_text("Timeout while waiting for a response from the server.")
                except httpx.HTTPStatusError as e:
                    await websocket.send_text(f"Error HTTP: {e.response.status_code} - {e.response.text}")
                except Exception:
                    traceback.print_exc()
                    await websocket.send_text("An error occurred while processing your request.")
        except Exception:
            traceback.print_exc()
