import tiktoken
from sentence_transformers import SentenceTransformer

import app.core.config as config
from app.db.chromadb import get_collection


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
        self.collection = get_collection()

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

    def get_context_text(self, query: str, max_tokens=config.MAX_CONTEXT_TOKENS):
        """
        Build context limited by token count instead of character count.
        
        param query: User query
        param max_tokens: Maximum tokens allowed in context
        return: Combined context text
        """

        # Retrieve documents
        retrieved_docs = self.search(query)

        # Simple keyword-based re-ranking for better relevance
        keywords = query.lower().split()

        def score(doc):
            text = doc["text"].lower()
            return sum(text.count(k) for k in keywords)

        # Sort documents by lexical score (descending)
        retrieved_docs = sorted(retrieved_docs, key=score, reverse=True)

        # Load tokenizer
        encoder = tiktoken.get_encoding("cl100k_base")

        combined = ""
        total_tokens = 0

        for item in retrieved_docs:
            text = item["text"]
            tokens = len(encoder.encode(text))

            # If adding this chunk would exceed max tokens → stop
            if total_tokens + tokens > max_tokens:
                break
            
            # Append chunk with metadata
            combined += (
                f"\n\n[CHUNK id={item['id']} source={item['metadata'].get('source','unknown')}]"
                f"\n{text}"
            )

            total_tokens += tokens

        config.debug_print(f"[ContextBuilder] Total tokens used: {total_tokens}/{max_tokens}")

        return combined.strip()

if __name__ == "__main__":
    retriever = Retriever()

    query = "What said Tom when he smiled?"
    context = retriever.get_context_text(query)

    config.debug_print("\n=== RETRIEVED CONTEXT ===")
    config.debug_print(context)
