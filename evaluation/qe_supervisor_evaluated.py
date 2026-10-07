
import json
import sys
from pathlib import Path

from deepeval import evaluate
from deepeval.tracing import observe, update_current_trace
from deepeval.metrics import TaskCompletionMetric
from deepeval.models import OllamaModel
from deepeval.test_case import LLMTestCase


# Add the mcp folder to Python's import path
MCP_DIR = Path(__file__).resolve().parent.parent / "mcp"
sys.path.insert(0, str(MCP_DIR))

from qe_supervisor import ask_supervisor, SPECIALISTS


@observe()
def run_evaluated_supervisor(payment_id: str):

    evidence = []

    completed = {
        "api": False,
        "db": False
    }

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

        if next_action == "done":

            final_result = {
                "payment_id": payment_id,
                "completed": completed,
                "evidence": evidence,
                "final_action": "done"
            }

            update_current_trace(
                input=f"Investigate payment {payment_id}",
                output=json.dumps(final_result)
            )

            return final_result

        # Deterministic guardrail
        if completed.get(next_action, False):

            print(
                f"⚠️ Duplicate action blocked: {next_action}"
            )

            continue

        specialist = SPECIALISTS.get(next_action)

        if specialist is None:

            final_result = {
                "payment_id": payment_id,
                "completed": completed,
                "evidence": evidence,
                "final_action": "error",
                "error": f"Unknown specialist: {next_action}"
            }

            update_current_trace(
                input=f"Investigate payment {payment_id}",
                output=json.dumps(final_result)
            )

            return final_result

        print(f"\nInvoking {next_action.upper()} Agent...")

        result = specialist(payment_id)

        print("Specialist result:")
        print(result)

        evidence.append({
            "specialist": next_action,
            "result": result
        })

        completed[next_action] = True

    final_result = {
        "payment_id": payment_id,
        "completed": completed,
        "evidence": evidence,
        "final_action": "max_iterations"
    }

    update_current_trace(
        input=f"Investigate payment {payment_id}",
        output=json.dumps(final_result)
    )

    return final_result


def main():

    payment_id = "P1001"

    print("QE Supervisor - DeepEval Evaluation")
    print(f"Investigating payment: {payment_id}")

    # --------------------------------------------------
    # 1. Run the actual supervisor
    # --------------------------------------------------

    result = run_evaluated_supervisor(payment_id)

    print("\nFinal Result:")
    print(json.dumps(result, indent=2))

    # --------------------------------------------------
    # 2. Create evaluator model
    # --------------------------------------------------

    evaluator_model = OllamaModel(
        model="llama3.2:3b",
        base_url="http://localhost:11434",
        temperature=0
    )

    # --------------------------------------------------
    # 3. Create Task Completion metric
    # --------------------------------------------------

    metric = TaskCompletionMetric(
        model=evaluator_model,
        threshold=0.5
    )

    # --------------------------------------------------
    # 4. Define evaluation test case
    # --------------------------------------------------

    test_case = LLMTestCase(
        input=(
            "Investigate payment P1001. "
            "Validate the payment using both API and DB specialists "
            "and complete the investigation."
        ),

        actual_output=json.dumps(result),

        expected_output=(
            "The investigation should complete successfully with "
            "both API and DB validations completed and the final "
            "action set to done."
        )
    )

    # --------------------------------------------------
    # 5. Evaluate
    # --------------------------------------------------

    print("\n--- DeepEval Evaluation ---")

    evaluate(
        test_cases=[test_case],
        metrics=[metric]
    )


if __name__ == "__main__":
    main()

