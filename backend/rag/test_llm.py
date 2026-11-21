from backend.rag.llm import generate_answer

question = "Why must workers wear safety helmets at construction sites?"

print("\n========== LOCAL LLM TEST ==========")
print("Question:", question)

answer = generate_answer(question)

print("\nQwen's Answer:")
print(answer)

print("\nLLM integration successful!")