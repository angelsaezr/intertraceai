import traceback

import httpx
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from pydantic import BaseModel

import app.core.config as config
from app.services.rag.ingest import Ingest
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

# Initialize services
engine = Engine()
pipeline = Pipeline()
ingest = Ingest()

# Endpoints

@app.get("/")
async def root():
    return {"message": "Welcome to the InterTraceAI API"}

@app.get("/documents")
async def get_documents():
    """
    Retrieve all documents from the database.
    """
    
    return {"message": "List of documents"}

@app.post("/documents")
async def add_document(document: Document):
    """
    Add a new document to the database.
    """

    return {"message": "Document added successfully"}

@app.post("/pipeline/query", tags=["Pipeline"], response_model=QueryResponse)
async def query_pipeline(request: QueryRequest):
    """
    Query the RAG pipeline with a question and get an answer.
    """
    pipeline = Pipeline()
    answer = await pipeline.query(request.question)
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
