from backend.rag.document_loader import load_pdf
from backend.rag.chunker import chunk_documents
from backend.rag.embeddings import generate_embedding
from backend.rag.vector_store import add_documents, collection

# Step 1: Load the safety manual
file_path = "backend/rag/test_documents/safety_manual.pdf"

documents = load_pdf(file_path)

# Step 2: Divide documents into chunks
chunks = chunk_documents(documents)

print("\n========== VECTOR DATABASE TEST ==========")
print("Total pages:", len(documents))
print("Total chunks:", len(chunks))

# Step 3: Generate embeddings
print("\nGenerating embeddings...")

embeddings = [
    generate_embedding(chunk["content"])
    for chunk in chunks
]

print("Embeddings generated:", len(embeddings))

# Step 4: Store everything in ChromaDB
add_documents(chunks, embeddings)

# Step 5: Verify stored data
print("\n========== DATABASE VERIFICATION ==========")
print("Total records in ChromaDB:", collection.count())

print("\nVector database setup successful!")