from pathlib import Path

from backend.rag.document_loader import load_document
from backend.rag.chunker import chunk_documents
from backend.rag.embeddings import generate_embedding
from backend.rag.vector_store import add_documents


def process_document(file_path: str) -> dict:
    """
    Load, chunk, embed and store an uploaded document.
    """

    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"Document not found: {file_path}")

    # Step 1: Extract document text
    documents = load_document(str(path))

    # Step 2: Split text into chunks
    chunks = chunk_documents(documents)

    if not chunks:
        raise ValueError("No text chunks generated.")

    # Step 3: Generate embeddings
    embeddings = [
        generate_embedding(chunk["content"])
        for chunk in chunks
    ]

    # Step 4: Store in ChromaDB
    add_documents(chunks, embeddings)

    return {
        "filename": path.name,
        "pages_processed": len(documents),
        "chunks_created": len(chunks),
        "status": "success"
    }