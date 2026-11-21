from backend.rag.embeddings import generate_embedding

text = "Workers must wear safety helmets inside construction zones."

embedding = generate_embedding(text)

print("\n========== EMBEDDING FUNCTION TEST ==========")
print("Embedding generated successfully!")
print("Vector dimensions:", len(embedding))
print("First 10 values:", embedding[:10])