import faiss
from sentence_transformers import SentenceTransformer

from ingestion import load_document, chunk_text


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

index = faiss.IndexFlatL2(384)

index.add(chunk_embeddings)

print(f"Number of vectors in FAISS: {index.ntotal}")


# query = "What happens if I try to cancel a payment after it has been settled?"

# query_embedding = model.encode([query])

# top_k = 3

# distances, indices = index.search(query_embedding, top_k)

# print("\nFAISS Search Results:")

# for distance, index_position in zip(distances[0], indices[0]):
#     print(f"Distance: {distance:.4f}")
#     print(f"Chunk index: {index_position}")
#     print(f"Chunk: {chunks[index_position]}")

def retrieve(query: str, top_k: int = 3):
    query_embedding = model.encode([query])

    distances, indices = index.search(query_embedding, top_k)

    results = []

    for distance, index_position in zip(distances[0], indices[0]):
        results.append(
            (distance, chunks[index_position])
        )

    return results