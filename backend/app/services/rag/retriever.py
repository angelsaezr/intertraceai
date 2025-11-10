from chromadb import PersistentClient
from sentence_transformers import SentenceTransformer

import app.core.config as config


class Retriever:
    """
    Document Retriever for RAG Pipeline
    """

    def __init__(self):
        """
        Initialize the document retriever.
        """

        self.model = SentenceTransformer(config.EMBEDDING_MODEL)
        self.top_k = config.TOP_K
        self.use_normalize = config.USE_NORMALIZE

        # Connect to Chroma vector database
        self.client = PersistentClient(path=config.CHROMA_DIR)
        self.collection = self.client.get_or_create_collection(name=config.COLLECTION_NAME)

    def embed_query(self, query: str):
        """
        Embed a query string into a vector representation.

        param query: Query string
        return: Numpy array of query embedding
        """

        embedding = self.model.encode(
            [query],
            convert_to_numpy=config.CONVERT_TO_NP,
            normalize_embeddings=self.use_normalize
        )
        return embedding

    def search(self, query: str):
        """
        Search for similar documents in the collection.

        param query: Query string
        return: List of retrieved documents
        """

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

    def get_context_text(self, query: str, max_chars=config.MAX_CONTEXT_CHARS):
        """
        Get context text for a query.
        
        param query: User query
        param max_chars: Maximum characters for context
        return: Combined context text
        """

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

    query = "What said Tom when he smiled?"
    context = retriever.get_context_text(query)

    config.debug_print("\n=== RETRIEVED CONTEXT ===")
    config.debug_print(context)
