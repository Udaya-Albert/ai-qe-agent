from deepeval import evaluate
from deepeval.metrics import GEval
from deepeval.models import OllamaModel
from deepeval.test_case import LLMTestCase
from deepeval.test_case import SingleTurnParams


def main():

    evaluator_model = OllamaModel(
        model="llama3.2:3b",
        base_url="http://localhost:11434",
        temperature=0
    )

    metric = GEval(
        name="Correctness",
        criteria=(
            "Evaluate whether the actual output is factually consistent "
            "with the expected output. Penalize contradictions or "
            "incorrect factual claims."
        ),
        evaluation_params=[
            SingleTurnParams.INPUT,
            SingleTurnParams.EXPECTED_OUTPUT,
            SingleTurnParams.ACTUAL_OUTPUT
        ],
        model=evaluator_model,
        threshold=0.5
    )

    test_case = LLMTestCase(
        input="What is the status of payment P1001?",
        expected_output="Payment P1001 is CANCELLED.",
        actual_output="Payment P1001 is COMPLETED."
    )

    evaluate(
        test_cases=[test_case],
        metrics=[metric]
    )


if __name__ == "__main__":
    main()