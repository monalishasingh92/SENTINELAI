import re


def split_into_claims(answer: str) -> list[str]:
    """
    Split an LLM-generated answer into individual claims.
    """

    lines = answer.splitlines()

    claims = []

    for line in lines:
        line = line.strip()

        if not line:
            continue

        # Remove bullet markers
        line = re.sub(r"^[-*•]\s*", "", line)

        if line:
            claims.append(line)

    return claims

from backend.rag.llm import generate_answer


def validate_claim(claim: str, evidence: str) -> bool:
    """
    Check whether a claim is explicitly supported by the evidence.
    """

    prompt = f"""
You are a strict evidence validator for an industrial safety system.

Determine whether the claim is directly supported by the evidence.

Rules:
1. Accept only information explicitly supported by the evidence.
2. Do not use general knowledge.
3. Do not make assumptions.
4. If the evidence only partially supports the claim, reject it.
5. Return only YES or NO.

EVIDENCE:
{evidence}

CLAIM:
{claim}

Is this claim fully supported?
"""

    result = generate_answer(prompt).strip().upper()
    print("\n========== CLAIM VALIDATION DEBUG ==========")
    print("CLAIM:", claim)
    print("EVIDENCE:", evidence)
    print("LLM VALIDATOR RESPONSE:", result)
    print("============================================")
    
   

    return result == "YES"


def validate_answer(answer: str, retrieved_chunks: list[dict]) -> list[str]:
    """
    Keep only claims supported by their cited document evidence.
    """

    validated_claims = []

    for claim in split_into_claims(answer):

        # Extract reference IDs such as [1], [2], [3]
        reference_ids = [
            int(ref)
            for ref in re.findall(r"\[(\d+)\]", claim)
        ]

        # Reject claims without citations
        if not reference_ids:
            continue

        # Reject invalid reference IDs
        if any(
            ref < 1 or ref > len(retrieved_chunks)
            for ref in reference_ids
        ):
            continue

        # Collect evidence from cited documents only
        evidence = "\n".join(
            retrieved_chunks[ref - 1]["content"]
            for ref in set(reference_ids)
        )

        # Validate the claim
        if validate_claim(claim, evidence):
            validated_claims.append(claim)

    return validated_claims