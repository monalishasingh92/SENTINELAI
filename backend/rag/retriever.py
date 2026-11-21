from backend.rag.embeddings import generate_embedding
from backend.rag.vector_store import collection


def retrieve_relevant_chunks(
    question: str,
    top_k: int = 3
) -> list[dict]:
    """
    Retrieve the most relevant safety-manual chunks
    for a user's question.
    """

    if not question.strip():
        raise ValueError("Question cannot be empty.")

    if collection.count() == 0:
        return []

    # Step 1: Convert the question into an embedding
    question_embedding = generate_embedding(question)

    # Step 2: Search ChromaDB
    results = collection.query(
        query_embeddings=[question_embedding],
        n_results=min(top_k, collection.count()),
        include=["documents", "metadatas", "distances"]
    )

    # Step 3: Organize retrieved results
    retrieved_chunks = []

    for index in range(len(results["documents"][0])):
        retrieved_chunks.append({
            "content": results["documents"][0][index],
            "metadata": results["metadatas"][0][index],
            "distance": results["distances"][0][index]
        })

    return retrieved_chunks