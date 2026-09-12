import ollama
from retrieval_faiss import retrieve


def build_prompt(query: str, retrieved_chunks: list[str]) -> str:
    context = "\n\n".join(retrieved_chunks)

    prompt = f"""
You are a QE assistant.

Answer the user's question using ONLY the provided context.
If the answer is not available in the context, say that it is not available.

Context:
{context}

User Question:
{query}
"""

    return prompt


def generate_answer(query: str, retrieved_chunks: list[str]) -> str:
     prompt = build_prompt(query, retrieved_chunks) 
     response = ollama.chat( 
          model="llama3.2:3b", 
          messages=[ 
               { "role": "user", 
                "content": prompt 
                } ] ) 
     return response["message"]["content"]


query = "What happens if I try to cancel a payment after it has been settled?"

# retrieved_chunks = [
#     "A cancellation request must be rejected when the payment has already been settled.",
#     "The cancellation API must return HTTP 409 when cancellation is rejected because the payment has already been settled.",
#     "The cancellation response must contain error code PAYMENT_ALREADY_SETTLED."
# ]

results = retrieve(query, top_k=3)
retrieved_chunks =  [chunk for distance, chunk in results]

answer = generate_answer(query, retrieved_chunks)

print("\nGenerated Answer:") 
print(answer)

