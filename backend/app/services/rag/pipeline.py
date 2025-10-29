from backend.app.core.config import debug_print

from .ingest import Ingest


class Pipeline:
    def __init__(self):
        self.ingest = Ingest()

    def run(self):
        documents = self.ingest.load_documents()
        split_docs = self.ingest.split_documents(documents)
        embeddings = self.ingest.generate_embeddings(split_docs)
        return split_docs, embeddings
    
if __name__ == "__main__":
    pipeline = Pipeline()
    split_docs, embeddings = pipeline.run()
    debug_print(f"Pipeline completed with {len(split_docs)} document chunks and {len(embeddings)} embeddings.")
    