from chromadb import PersistentClient

import app.core.config as config

client = PersistentClient(path=config.CHROMA_DIR)

def get_collection():
    return client.get_or_create_collection(name=config.COLLECTION_NAME)
