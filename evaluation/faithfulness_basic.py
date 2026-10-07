from deepeval import evaluate
from deepeval.metrics import FaithfulnessMetric
from deepeval.models import OllamaModel
from deepeval.test_case import LLMTestCase


def main():

    evaluator_model = OllamaModel(
        model="llama3.2:3b",
        base_url="http://localhost:11434",
        temperature=0
    )

    metric = FaithfulnessMetric(
        model=evaluator_model,
        threshold=0.5
    )

    test_case = LLMTestCase(
        input="What is the status of payment P1001?",
        actual_output="Payment P1001 is COMPLETED.",
        retrieval_context=[
            "Payment P1001 has status CANCELLED.",
            "Transaction type is FX."
        ]
    )

    evaluate(
        test_cases=[test_case],
        metrics=[metric]
    )


if __name__ == "__main__":
    main()