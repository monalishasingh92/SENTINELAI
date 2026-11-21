from backend.rag.document_loader import load_pdf
from backend.rag.chunker import chunk_documents

# Step 1: Load the PDF
file_path = "backend/rag/test_documents/safety_manual.pdf"

documents = load_pdf(file_path)

# Step 2: Divide documents into chunks
chunks = chunk_documents(documents)

# Step 3: Display results
print("\n========== CHUNKING RESULTS ==========")

print(f"Total pages: {len(documents)}")
print(f"Total chunks generated: {len(chunks)}")

print("\n========== FIRST 3 CHUNKS ==========")

for index, chunk in enumerate(chunks[:3], start=1):
    print(f"\nChunk {index}")
    print("Metadata:", chunk["metadata"])
    print("Content:")
    print(chunk["content"])
    print("Character count:", len(chunk["content"]))