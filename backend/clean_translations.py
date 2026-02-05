
import chromadb
from chromadb.config import Settings

client = chromadb.PersistentClient(path="./data/chroma")
collection = client.get_collection("health_knowledge")

# Get all documents
results = collection.get(include=["metadatas"])

print(f"Total documents to clean: {len(results['ids'])}")

for i, doc_id in enumerate(results["ids"]):
    metadata = results["metadatas"][i]
    if not metadata:
        continue
        
    # Force clean all translation cache fields
    metadata["title_zh"] = ""
    metadata["content_zh"] = ""
    metadata["title_en"] = ""
    metadata["content_en"] = ""
    
    collection.update(ids=[doc_id], metadatas=[metadata])

print("Full database translation cleanup complete.")
