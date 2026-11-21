from backend.rag.document_processor import process_document

if __name__ == "__main__":
    result = process_document(
        "backend/rag/test_documents/safety_manual.pdf"
    )

    print("\n========== DOCUMENT PROCESSING TEST ==========")
    print(result)