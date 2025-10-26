from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from sentence_transformers import SentenceTransformer


class Ingest:
    def __init__(self):
        self.dir_loader = DirectoryLoader( # Directory loader for text files
            r"C:\Users\angel\Proyectos\intertraceai\backend\tests",
            glob="*.txt",
            loader_cls=TextLoader,
            loader_kwargs={"encoding": "utf8"},
            show_progress=True
        )
        self.model = SentenceTransformer("all-MiniLM-L6-v2") # Pre-trained embedding model

    def load_documents(self):
        documents = self.dir_loader.load() # Load documents from directory
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=100, chunk_overlap=0) # Splitter for text chunks
        all_split_docs = text_splitter.split_documents(documents) # Split documents into smaller chunks

        print(f"Loaded {len(documents)} files. Split into {len(all_split_docs)} chunks.")
        return all_split_docs

    def generate_embeddings(self, split_docs):
        embeddings = self.model.encode([d.page_content for d in split_docs]) # Generate embeddings for each text chunk
        print("----- Embeddings -----")
        print(embeddings[0])
        return embeddings

if __name__ == "__main__":
    ingest = Ingest()
    split_docs = ingest.load_documents()
    embeddings = ingest.generate_embeddings(split_docs)
