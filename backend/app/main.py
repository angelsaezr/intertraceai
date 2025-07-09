from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import httpx
import traceback

app = FastAPI()

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "mistral:7b-instruct-q4_0"

# Root endpoint
@app.get("/")
async def root():
    return {"message": "Hello world!"}

# WebSocket endpoint for chat
@app.websocket("/chat")
async def chat(websocket: WebSocket):
    await websocket.accept()
    async with httpx.AsyncClient(timeout=httpx.Timeout(30.0)) as client:
        try:
            while True:
                try:
                    user_message = await websocket.receive_text()
                    print(f"SERVER: User message: {user_message}")

                    response = await client.post(OLLAMA_URL, json={
                        "model": MODEL_NAME,
                        "prompt": user_message,
                        "stream": False
                    })

                    response.raise_for_status()
                    data = response.json()
                    model_reply = data.get("response", "Error: no response")

                    await websocket.send_text(model_reply)

                except WebSocketDisconnect:
                    print("SERVER: WebSocket disconnected")
                    break
                except httpx.ReadTimeout:
                    await websocket.send_text("Timeout while waiting for response from model.")
                except httpx.HTTPStatusError as e:
                    await websocket.send_text(f"Error HTTP: {e.response.status_code} - {e.response.text}")
                except Exception as ex:
                    traceback.print_exc()
                    await websocket.send_text("An error occurred while processing your request.")

        except Exception as e:
            traceback.print_exc()