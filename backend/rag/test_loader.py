from backend.rag.document_loader import load_pdf

file_path = "backend/rag/test_documents/safety_manual.pdf"

documents = load_pdf(file_path)

print(f"\nTotal pages extracted: {len(documents)}")

for document in documents:
    print("\n-----------------------------")
    print("Metadata:", document["metadata"])
    print("Extracted text:")
    print(document["content"][:500])