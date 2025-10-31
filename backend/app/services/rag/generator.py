import traceback

import httpx

import backend.app.core.config as config

from .retriever import Retriever


class Generator:
    def __init__(
        self,
        llm_url=config.LMSTUDIO_BASE_URL,
        model_name=config.LLM_MODEL,
        temperature=0.7
    ):
        self.llm_url = llm_url
        self.model_name = model_name
        self.temperature = temperature
        self.retriever = Retriever()

    async def _call_llm(self, messages):
        """Send prompt to the local LLM (LMStudio API)"""

        payload = {
            "model": self.model_name,
            "messages": messages,
            "temperature": self.temperature,
            "stream": False
        }

        async with httpx.AsyncClient(timeout=httpx.Timeout(60.0)) as client:
            response = await client.post(self.llm_url, json=payload)
            response.raise_for_status()
            data = response.json()
            return data["choices"][0]["message"]["content"]

    async def generate(self, query: str) -> str:
        """Generate RAG response using retrieved context"""

        try:
            # Retrieve context from ChromaDB
            context = self.retriever.get_context_text(query)
            config.debug_print(f"\n=== INJECTED CONTEXT ===\n{context}")

            # System prompt enforcing RAG behavior
            system_prompt = (
                "Use this context to answer the question.\n"
                f"--- CONTEXT ---\n{context}\n--- END CONTEXT ---"
            )


            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": query}
            ]

            # Send to local LLM
            reply = await self._call_llm(messages)
            return reply

        except Exception:
            traceback.print_exc()
            return "An error occurred while generating the response."


# Manual test
if __name__ == "__main__":
    import asyncio

    async def test():
        g = Generator()
        q = "What said Tom when he smiled?"
        ans = await g.generate(q)
        print("\n=== RAG RESPONSE ===")
        print(ans)

    asyncio.run(test())
