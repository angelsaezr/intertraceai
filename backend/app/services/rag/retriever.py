from pathlib import Path

import tiktoken
from sentence_transformers import SentenceTransformer

import app.core.config as config
from app.db.chromadb import get_collection


class Retriever:
    """
    Document Retriever for RAG Pipeline.
    """

    def __init__(self, model: SentenceTransformer):
        self.model = model
        self.top_k = config.TOP_K
        self.use_normalize = config.USE_NORMALIZE

    def embed_query(self, query: str):
        return self.model.encode(
            [query],
            convert_to_numpy=config.CONVERT_TO_NP,
            normalize_embeddings=self.use_normalize,
        )

    def search(self, query: str) -> list[dict]:
        query_vec = self.embed_query(query)

        collection = get_collection()

        results = collection.query(
            query_embeddings=query_vec,
            n_results=self.top_k
        )

        docs = results.get("documents", [[]])[0]
        metadatas = results.get("metadatas", [[]])[0]
        ids = results.get("ids", [[]])[0]
        distances = results.get("distances", [[]])[0]

        retrieved = []
        for doc, meta, doc_id, dist in zip(docs, metadatas, ids, distances):
            if dist > config.DISTANCE_THRESHOLD:
                config.debug_print(f"[Filter] Discarded chunk {doc_id} by distance {dist:.4f}")
                continue

            retrieved.append({
                "id": doc_id,
                "text": doc,
                "metadata": meta,
                "distance": dist,
            })

        config.debug_print(f"Query: {query}")
        for r in retrieved:
            config.debug_print(
                f"- {r['id']} (dist={r['distance']:.4f}) source={r['metadata'].get('source')}"
            )

        return retrieved

    def get_context_text(self, query: str, max_tokens: int = config.MAX_CONTEXT_TOKENS) -> tuple[str, list[str]]:
        retrieved_docs = self.search(query)
        config.debug_print(f"[DEBUG] retrieved_docs: {retrieved_docs}")

        keywords = query.lower().split()

        def score(doc):
            text = doc["text"].lower()
            return sum(text.count(k) for k in keywords)

        retrieved_docs = sorted(retrieved_docs, key=score, reverse=True)

        encoder = tiktoken.get_encoding("cl100k_base")
        combined = ""
        total_tokens = 0
        sources: list[str] = []

        for item in retrieved_docs:
            text = item["text"]
            tokens = len(encoder.encode(text))
            if total_tokens + tokens > max_tokens:
                break
            source = item["metadata"].get("source", "unknown")
            combined += f"\n\n[CHUNK id={item['id']} source={source}]\n{text}"
            total_tokens += tokens
            name = Path(source).name
            if name not in sources:
                sources.append(name)

        config.debug_print(f"[ContextBuilder] Total tokens used: {total_tokens}/{max_tokens}")
        return combined.strip(), sources