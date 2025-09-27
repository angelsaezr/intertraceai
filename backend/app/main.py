from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import httpx
import traceback

app = FastAPI()

LMSTUDIO_URL = "http://localhost:1234/v1/chat/completions"
MODEL_NAME = "google/gemma-3-1b"

@app.get("/")
async def root():
    return {"message": "Hello world!"}

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
                        "model": MODEL_NAME,
                        "messages": conversation,
                        "temperature": 0.7,
                        "stream": False
                    }

                    response = await client.post(LMSTUDIO_URL, json=payload)
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
