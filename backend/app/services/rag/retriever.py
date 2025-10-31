from chromadb import PersistentClient
from sentence_transformers import SentenceTransformer

import backend.app.core.config as config


class Retriever:
    def __init__(
        self,
        model_name=config.EMBEDDING_MODEL,
        top_k=config.TOP_K,
        use_normalize=True
    ):
        self.model = SentenceTransformer(model_name)
        self.top_k = top_k
        self.use_normalize = use_normalize

        # Connect to Chroma vector database
        self.client = PersistentClient(path=config.CHROMA_DIR)
        self.collection = self.client.get_or_create_collection(name="document_embeddings")

    # Embed a query string
    def embed_query(self, query: str):
        embedding = self.model.encode(
            [query],
            convert_to_numpy=True,
            normalize_embeddings=self.use_normalize
        )
        return embedding

    # Search for similar documents
    def search(self, query: str):
        query_vec = self.embed_query(query)

        results = self.collection.query(
            query_embeddings=query_vec,
            n_results=self.top_k
        )

        docs = results.get("documents", [[]])[0]
        metadatas = results.get("metadatas", [[]])[0]
        ids = results.get("ids", [[]])[0]
        distances = results.get("distances", [[]])[0]

        # Format results
        retrieved = []
        for doc, meta, doc_id, dist in zip(docs, metadatas, ids, distances):
            retrieved.append({
                "id": doc_id,
                "text": doc,
                "metadata": meta,
                "distance": dist
            })
        config.debug_print(f"Query: {query}")
        config.debug_print("Results:")
        for r in retrieved:
            config.debug_print(f"- {r['id']} (dist={r['distance']:.4f}) source={r['metadata'].get('source')}")

        return retrieved

    # Get context text for a query
    def get_context_text(self, query: str, max_chars=config.MAX_CONTEXT_CHARS):
        retrieved_docs = self.search(query)

        # Combine texts up to max_chars
        combined = ""
        for item in retrieved_docs:
            if len(combined) + len(item["text"]) <= max_chars:
                combined += "\n" + item["text"]
            else:
                break

        return combined.strip()

if __name__ == "__main__":
    retriever = Retriever()

    query = "What said Tom"
    context = retriever.get_context_text(query)

    print("\n=== CONTEXTO RECUPERADO ===")
    print(context)
