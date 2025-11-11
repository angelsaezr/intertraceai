import traceback

import httpx

import app.core.config as config

from .retriever import Retriever


class Generator:
    """
    RAG Response Generator using local LLM and Retriever
    """

    def __init__(self):
        """
        Initialize the RAG generator.
        """
        
        self.llm_url = config.LMSTUDIO_BASE_URL
        self.model_name = config.LLM_MODEL
        self.temperature = config.TEMPERATURE
        self.retriever = Retriever()

    async def _call_llm(self, messages):
        """
        Send prompt to the local LLM (LMStudio API)
        
        param messages: List of message dicts for the LLM
        return: LLM response text
        """

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
        """
        Generate RAG response using retrieved context
        
        param query: User query
        return: Generated response text
        """

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


if __name__ == "__main__":
    import asyncio

    async def test():
        g = Generator()
        q = "How many Champions League titles has Real Madrid won?"
        ans = await g.generate(q)
        config.debug_print("\n=== RAG RESPONSE ===")
        config.debug_print(ans)

    asyncio.run(test())
