#from langchain_core.document import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import DirectoryLoader, TextLoader

#from sentence_transformers import SentenceTransformer

# Recursive character text splitter splits text into chunks of a specified size, with a certain amount of overlap between chunks.

#folder = r"C:\Users\angel\Downloads"
#texts = [f for f in os.listdir(folder) if f.lower().endswith(".txt")]

dir_loader = DirectoryLoader(
    r"C:\Users\angel\Downloads",
    glob="*.txt",                           # Pattern to match files
    loader_cls=TextLoader,                  # Specify the loader class to use for each file
    loader_kwargs={"encoding": "utf8"},     # Additional arguments for the loader class
    show_progress=True                      # Show progress while loading files
)

documents = dir_loader.load()

print(f"Loaded {len(documents)} files.")
for doc in documents:
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=100, chunk_overlap=0)
    split_docs = text_splitter.split_documents([doc])
    print("----- Split Documents -----")
    for i, split_doc in enumerate(split_docs):
        print(f"Document {i}: {split_doc}")

""" # Embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")
embeddings = model.encode([doc.page_content for doc in split_docs]) # TODO: Fix split_docs
print("----- Embeddings -----")
for i, embedding in enumerate(embeddings):
    print(f"Document {i} embedding: {embedding}")
    # You can now use the embeddings for various tasks, such as similarity search or clustering
    # For example, you could store them in a database or use them to find similar documents
    # Here, we'll just print them out
    print(embedding) """
    