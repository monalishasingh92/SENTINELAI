import re

from backend.rag.retriever import retrieve_relevant_chunks
from backend.rag.llm import generate_answer
from backend.rag.answer_validator import validate_answer


def validate_and_replace_citations(answer, retrieved_chunks):
    """
    Replace reference IDs with actual document citations.
    """

    def replace_reference(match):
        reference_id = int(match.group(1))

        if reference_id < 1 or reference_id > len(retrieved_chunks):
            return "[Invalid citation]"

        chunk = retrieved_chunks[reference_id - 1]

        source = chunk["metadata"]["source"]
        page = chunk["metadata"]["page"]

        return f"[Source: {source}, Page: {page}]"

    return re.sub(r"\[(\d+)\]", replace_reference, answer)


def ask_safety_assistant(question: str) -> dict:
    """
    Answer a user's question using retrieved safety-manual content.
    """

    if not question.strip():
        raise ValueError("Question cannot be empty.")

    # Step 1: Retrieve relevant information
    retrieved_chunks = retrieve_relevant_chunks(question, top_k=3)

    if not retrieved_chunks or retrieved_chunks[0]["distance"] > 0.8:
        return {
            "question": question,
            "answer": (
                "The available safety documents do not provide "
                "sufficient information to answer this question."
            ),
            "sources": []
        }

    # Step 2: Prepare source-labelled context
    context = ""

    for index, chunk in enumerate(retrieved_chunks, start=1):
        source = chunk["metadata"]["source"]
        page = chunk["metadata"]["page"]

        context += (
            f"\n[REFERENCE {index}]\n"
            f"Source: {source}\n"
            f"Page: {page}\n"
            f"Content: {chunk['content']}\n"
        )

    # Step 3: Build the prompt
    prompt = f"""
        You are SENTINEL AI, an industrial workplace safety assistant.

        STRICT RULES:

    1. Use ONLY facts explicitly stated in the provided context.
    2. Never use general knowledge or assumptions.
    3. Never invent emergency procedures, evacuation steps, equipment, instructions, or recommendations.
    4. Do not assume that a standard safety procedure is documented unless it appears in the context.
    5. Every factual bullet point MUST have a citation.
    6. Use only the supplied reference IDs: [1], [2], [3].
    7. Never write citations such as [Reference 1].
    8. If the context does not explicitly answer part of the question, do not guess or complete the missing steps.
    9. If information is incomplete, clearly state that the available documents provide only partial information.
    10. Never repeat the same instruction.
    11. Prefer short, directly supported answers.
    12. If no useful information is available, respond: "The available safety documents do not provide sufficient
    information to answer this question."
    13. Never present an unsupported instruction as a workplace safety recommendation.

OUTPUT FORMAT:

Answer using concise bullet points.

Example:
- Hard hats protect workers from falling objects. [1]
- Safety goggles protect workers from dust and debris. [2]

CONTEXT:
{context}

USER QUESTION:
{question}

Provide a grounded answer with accurate citations.
"""

    # Step 4: Generate draft answer
    draft_answer = generate_answer(prompt)

    # Step 5: Validate individual claims against evidence
    validated_claims = validate_answer(
        draft_answer,
        retrieved_chunks
    )

    # Step 6: Reject answers with no verified claims
    if not validated_claims:
        return {
            "question": question,
            "answer": (
                "The available safety documents do not provide "
                "sufficient verified information to answer this question."
            ),
            "sources": []
        }

    # Step 7: Reconstruct the validated answer
    answer_with_references = "\n".join(
        f"- {claim}" for claim in validated_claims
    )

    # Step 8: Replace reference IDs with actual source citations
    answer = validate_and_replace_citations(
        answer_with_references,
        retrieved_chunks
    )

    # Step 9: Collect only sources cited by validated claims
    sources = []

    cited_reference_ids = {
        int(reference_id)
        for claim in validated_claims
        for reference_id in re.findall(r"\[(\d+)\]", claim)
    }

    for reference_id in sorted(cited_reference_ids):

        # Defensive check
        if reference_id < 1 or reference_id > len(retrieved_chunks):
            continue

        chunk = retrieved_chunks[reference_id - 1]

        source_info = {
            "source": chunk["metadata"]["source"],
            "page": chunk["metadata"]["page"]
        }

        if source_info not in sources:
            sources.append(source_info)

    # Step 10: Return final response
    return {
        "question": question,
        "answer": answer,
        "sources": sources
    }
