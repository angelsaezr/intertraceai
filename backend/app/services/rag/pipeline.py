import asyncio

import app.core.config as config

from .generator import Generator
from .ingest import Ingest


class Pipeline:
    """
    RAG Ingestion and Embedding Pipeline
    """

    def __init__(self):
        """
        Initialize the RAG pipeline.
        """

        self.ingest = Ingest()
        self.generator = Generator()

    def run(self, file_paths: list[str]):
        """
        Execute the ingestion and embedding pipeline.

        param file_paths: List of file paths to ingest
        return: Tuple of (split documents, embeddings)
        """

        # Load documents
        documents = self.ingest.load_from_paths(file_paths)
        
        # Split documents into chunks
        split_docs = self.ingest.split_documents(documents)
        
        # Generate embeddings for the document chunks
        embeddings = self.ingest.generate_embeddings(split_docs)
        
        # Save embeddings to the vector database
        self.ingest.save_to_vector_db(embeddings, split_docs)
        
        return split_docs, embeddings

    async def query(self, user_query):
        """
        Process a user query through the RAG pipeline.

        param user_query: The query string from the user
        return: Generated response from the pipeline
        """
        
        response = await self.generator.generate(user_query)
        return response

if __name__ == "__main__":
    #engine = Engine()
    pipeline = Pipeline()

    #engine_results = engine.search()

    #split_docs, embeddings = pipeline.run(file_paths=engine_results)

    user_query = "Is latex a mathematics typesetting program that is the standard for most professional mathematics writing?"
    config.debug_print("Processing query...")
    response = asyncio.run(pipeline.query(user_query))
    config.debug_print("\nResponse:", response)
