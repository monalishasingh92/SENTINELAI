from backend.rag.retriever import retrieve_relevant_chunks

# Test question
question = "What protective equipment should workers wear at construction sites?"

# Retrieve the 3 most relevant chunks
results = retrieve_relevant_chunks(question, top_k=3)

print("\n========== SEMANTIC RETRIEVAL TEST ==========")

print("Question:", question)
print("Results found:", len(results))

for index, result in enumerate(results, start=1):
    print(f"\n========== RESULT {index} ==========")

    print("Source:", result["metadata"]["source"])
    print("Page:", result["metadata"]["page"])
    print("Distance:", result["distance"])

    print("\nRetrieved content:")
    print(result["content"])