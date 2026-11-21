import ollama

LLM_MODEL = "qwen2.5:1.5b"


def generate_answer(prompt: str) -> str:
    """
    Generate a response using the local Qwen LLM.
    """

    response = ollama.chat(
        model=LLM_MODEL,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response["message"]["content"]