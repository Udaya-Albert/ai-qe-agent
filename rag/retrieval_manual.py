from ingestion import load_document, chunk_text
from sentence_transformers import SentenceTransformer
from sentence_transformers.util import cos_sim


document_path = "data/requirements/payment_cancellation.txt"

document = load_document(document_path)

chunks = chunk_text(
    document,
    chunk_size=20,
    overlap=5
)

print(f"Number of chunks: {len(chunks)}")

model = SentenceTransformer("all-MiniLM-L6-v2")

chunk_embeddings = model.encode(chunks)

print(f"Embedding dimensions: {len(chunk_embeddings[0])}")

query = "What happens if I try to cancel a payment after it has been settled?"

query_embedding = model.encode(query)

print(f"Query embedding dimensions: {len(query_embedding)}")

similarities = []

for index, chunk_embedding in enumerate(chunk_embeddings):
    score = cos_sim(query_embedding, chunk_embedding).item()

    similarities.append((score, index))

print("\nSimilarity scores:")

for score, index in similarities:
    print(f"Chunk {index + 1}: {score:.4f}")


top_k = 3

top_chunks = sorted(
    similarities,
    reverse=True
)[:top_k]

print("\nTop relevant chunks:")

for score, index in top_chunks:
    print(f"\nScore: {score:.4f}")
    print(f"Chunk {index + 1}:")
    print(chunks[index])   

def retrieve(query: str, top_k: int):
    query_embedding  = model.encode(query)
    similarities = []
    results = []

    for index, chunk_embedding in enumerate(chunk_embeddings):
        score = cos_sim(query_embedding, chunk_embedding).item()

        similarities.append((score, index))


    top_chunks = sorted(
        similarities,
        reverse=True
    )[:top_k]

    for score, index in top_chunks:
        results.append((score, chunks[index]))
    return results

if __name__ == "__main__":
    results = retrieve(
    "What happens if I cancel a settled payment?",
    top_k=3
    )

    for score, chunk in results:
        print(f"\nScore: {score:.4f}")
        print(chunk)