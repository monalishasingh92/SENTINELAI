from backend.rag.rag_pipeline import ask_safety_assistant

question = "What protective equipment should workers wear at construction sites?"

result = ask_safety_assistant(question)

print("\n========== SENTINEL AI CITATION TEST ==========")

print("\nQUESTION:")
print(result["question"])

print("\nGENERATED ANSWER:")
print(result["answer"])

print("\nSOURCE REFERENCES:")

for source in result["sources"]:
    print(f"- {source['source']}, Page {source['page']}")

print("\n========== TEST COMPLETE ==========")