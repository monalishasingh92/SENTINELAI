from langchain_text_splitters import RecursiveCharacterTextSplitter


def chunk_documents(
    documents: list[dict],
    chunk_size: int = 500,
    chunk_overlap: int = 100
) -> list[dict]:
    """
    Divide extracted documents into smaller overlapping chunks.

    Each chunk retains its original source and page metadata.
    """

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", " ", ""]
    )

    chunks = []

    for document in documents:
        text_chunks = text_splitter.split_text(document["content"])

        for chunk in text_chunks:
            chunks.append({
                "content": chunk,
                "metadata": document["metadata"].copy()
            })

    return chunks
    