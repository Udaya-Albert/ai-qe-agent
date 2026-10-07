
import ollama


MODEL = "llama3.2:3b"


def main():

    prompt = """
You must choose the next action.

Current state:
- API completed = false
- DB completed = true

Allowed actions:
- api
- db
- done

Rules:
- If API is false, API must be selected.
- If DB is false, DB may be selected.
- If both are true, select done.
- NEVER select a completed specialist.

What is the next action?

Return JSON only:

{
    "next_action": "api" | "db" | "done",
    "reason": "short explanation"
}
"""

    print("===== PROMPT SENT TO LLM =====")
    print(prompt)

    response = ollama.chat(
        model=MODEL,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        format="json"
    )

    print("\n===== LLM RESPONSE =====")
    print(response.message.content)


if __name__ == "__main__":
    main()

