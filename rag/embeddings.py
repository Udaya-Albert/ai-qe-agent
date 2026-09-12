from sentence_transformers import SentenceTransformer
from sentence_transformers.util import cos_sim

model = SentenceTransformer("all-MiniLM-L6-v2")

texts = [
    "A cancellation request must be rejected when the payment has already been settled.",
    "You cannot cancel a payment after it has been settled.",
    "The API request must contain a valid authentication token."
]
embeddings = model.encode(texts)

similarity_ab = cos_sim(embeddings[0], embeddings[1])
similarity_ac = cos_sim(embeddings[0], embeddings[2])

print(f"Similarity A-B: {similarity_ab.item():.4f}")
print(f"Similarity A-C: {similarity_ac.item():.4f}")