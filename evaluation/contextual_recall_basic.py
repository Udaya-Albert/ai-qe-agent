from deepeval import evaluate
from deepeval.metrics import ContextualRecallMetric
from deepeval.models import OllamaModel
from deepeval.test_case import LLMTestCase


def main():

    evaluator_model = OllamaModel(
        model="llama3.2:3b",
        base_url="http://localhost:11434",
        temperature=0
    )

    metric = ContextualRecallMetric(
        model=evaluator_model,
        threshold=0.5
    )

    test_case = LLMTestCase(
        input="What is the status and transaction type of payment P1001?",

        actual_output=(
            "Payment P1001 is CANCELLED."
        ),

        expected_output=(
            "Payment P1001 is CANCELLED and the transaction type is FX."
        ),

        retrieval_context=[
            "Payment P1001 has status CANCELLED.",
        
        ]
    )

    evaluate(
        test_cases=[test_case],
        metrics=[metric]
    )


if __name__ == "__main__":
    main()