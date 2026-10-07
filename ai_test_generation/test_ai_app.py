from deepeval import evaluate
from deepeval.metrics import GEval
from deepeval.models import OllamaModel
from deepeval.test_case import LLMTestCase, SingleTurnParams


def validate_payment_response(actual_response, expected_status):

    if expected_status.lower() in actual_response.lower():
        return True

    return False


if __name__ == "__main__":

    expected_status = "CANCELLED"

    actual_response = (
        "Payment P1001 is COMPLETED."
    )

    # -----------------------------
    # Deterministic validation
    # -----------------------------

    deterministic_result = validate_payment_response(
        actual_response,
        expected_status
    )

    print(
        "Deterministic validation:",
        deterministic_result
    )

    # -----------------------------
    # Semantic validation
    # -----------------------------

    model = OllamaModel(
        model="llama3.2:3b"
    )

    semantic_metric = GEval(
        name="Payment Status Correctness",
        criteria="""
        Determine whether the actual response correctly communicates
        that payment P1001 has a CANCELLED status.

        The response does not need to use the exact word 'CANCELLED'.
        Equivalent natural-language expressions are acceptable.

        Do not consider the response correct if it says that the payment
        is COMPLETED, PENDING, FAILED, or another status.
        """,
        evaluation_params=[
            SingleTurnParams.ACTUAL_OUTPUT
        ],
        model=model,
        threshold=0.7
    )

    test_case = LLMTestCase(
        input="What is the status of payment P1001?",
        actual_output=actual_response
    )

    result = semantic_metric.measure(test_case)

    print(
        "Semantic score:",
        result
    )

    print(
        "Semantic reason:",
        semantic_metric.reason
    )