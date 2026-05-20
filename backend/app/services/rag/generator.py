import traceback

import httpx

import app.core.config as config
from app.services.rag.retriever import Retriever


class Generator:
    """
    RAG Response Generator using local LLM and Retriever.
    """

    def __init__(self, retriever: Retriever):
        self.retriever = retriever
        self.llm_url = config.LMSTUDIO_BASE_URL
        self.model_name = config.LLM_MODEL
        self.temperature = config.TEMPERATURE

    async def _call_llm(self, messages: list[dict]) -> str:
        payload = {
            "model": self.model_name,
            "messages": messages,
            "temperature": self.temperature,
            "stream": False,
        }
        async with httpx.AsyncClient(timeout=httpx.Timeout(60.0)) as client:
            response = await client.post(self.llm_url, json=payload)
            response.raise_for_status()
            data = response.json()
            return data["choices"][0]["message"]["content"]

    async def generate(self, query: str) -> dict:
        try:
            context, sources = self.retriever.get_context_text(query)
            config.debug_print(f"\n=== INJECTED CONTEXT ===\n{context}")

            system_prompt = (
                "Use this context to answer the question.\n"
                f"--- CONTEXT ---\n{context}\n--- END CONTEXT ---"
            )
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": query},
            ]

            reply = await self._call_llm(messages)
            return {"answer": reply, "sources": sources}

        except Exception:
            traceback.print_exc()
            return {"answer": "An error occurred while generating the response.", "sources": []}