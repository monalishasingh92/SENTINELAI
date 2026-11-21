import chromadb
from pathlib import Path

# Persistent database location
DB_PATH = Path("backend/rag/chroma_db")

# Create ChromaDB client
client = chromadb.PersistentClient(path=str(DB_PATH))

# Create or retrieve safety documents collection
collection = client.get_or_create_collection(
    name="safety_documents",
    metadata={"description": "Factory safety manual knowledge base"}
)


def add_documents(chunks: list[dict], embeddings: list[list[float]]):
    """
    Store document chunks, embeddings and metadata in ChromaDB.
    """

    if len(chunks) != len(embeddings):
        raise ValueError("Number of chunks and embeddings must match.")

    if not chunks:
        return

    ids = [
        f"{chunk['metadata']['source']}_page_{chunk['metadata']['page']}_chunk_{index}"
        for index, chunk in enumerate(chunks)
    ]

    collection.upsert(
        ids=ids,
        documents=[chunk["content"] for chunk in chunks],
        embeddings=embeddings,
        metadatas=[chunk["metadata"] for chunk in chunks]
    )

    print(f"Successfully stored {len(chunks)} chunks in ChromaDB.")