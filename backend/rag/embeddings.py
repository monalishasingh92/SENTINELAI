import ollama

EMBEDDING_MODEL = "nomic-embed-text"


def generate_embedding(text: str) -> list[float]:
    """
    Convert text into a numerical embedding using Ollama.
    """

    if not text.strip():
        raise ValueError("Cannot generate an embedding for empty text.")

    response = ollama.embed(
        model=EMBEDDING_MODEL,
        input=text
    )

    return response["embeddings"][0]