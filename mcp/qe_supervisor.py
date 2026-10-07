
import json
import ollama

from api_agent import run_api_agent
from db_agent import run_db_agent


MODEL = "llama3.2:3b"


SPECIALISTS = {
    "api": run_api_agent,
    "db": run_db_agent
}


def ask_supervisor(payment_id, evidence, completed):
    prompt = f"""
You are a QE Supervisor.

Investigate payment {payment_id}.

Available specialist agents:
- api: validates payment through the API
- db: validates payment through the database

Execution state:
{json.dumps(completed, indent=2)}

Evidence collected so far:
{json.dumps(evidence, indent=2)}

Decide which specialist should be invoked next.

Rules:
1. Choose "api" only if API validation is incomplete.
2. Choose "db" only if DB validation is incomplete.
3. Choose "done" if both validations are complete.

Return JSON only:

{{
    "next_action": "api" | "db" | "done",
    "reason": "short explanation"
}}
"""

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

    return json.loads(response.message.content)


def main():

    payment_id = "P1001"

    evidence = []

    completed = {
        "api": False,
        "db": False
    }

    trace = {
    "proposed_actions": [],
    "tools_called": [],
    "final_action": None,
    "evidence": {}
}

    print("QE Supervisor")
    print(f"Investigating payment: {payment_id}")

    for iteration in range(5):

        print(f"\n--- Supervisor iteration {iteration + 1} ---")

        decision = ask_supervisor(
            payment_id,
            evidence,
            completed
        )

        print("Supervisor decision:")
        print(decision)

        next_action = decision["next_action"]
        trace["proposed_actions"].append(next_action)

        if next_action == "done":
            trace["final_action"] = "done"
            print("\nSupervisor finished investigation.")
            break

        # Deterministic guardrail
        if completed.get(next_action, False):
            print(
                f"\n⚠️ Guardrail blocked duplicate action: "
                f"{next_action}"
            )
            continue

        specialist = SPECIALISTS.get(next_action)

        if specialist is None:
            print(f"\nUnknown specialist: {next_action}")
            break

        print(f"\nInvoking {next_action.upper()} Agent...")

        result = specialist(payment_id)

        print("Specialist result:")
        print(result)

        evidence.append({
            "specialist": next_action,
            "result": result
        })
        trace["tools_called"].append(next_action)

        trace["evidence"][next_action] = {
            "status": result.get("status")
        }

        # Update state only after successful execution
        completed[next_action] = True

    print("\nFinal execution state:")
    print(json.dumps(completed, indent=2))

    print("\nFinal evidence:")
    print(json.dumps(evidence, indent=2))

    print("\nEvaluation Trace:")
    print(json.dumps(trace, indent=2))


if __name__ == "__main__":
    main()

