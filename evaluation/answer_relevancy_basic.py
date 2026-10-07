from deepeval import evaluate
from deepeval.metrics import AnswerRelevancyMetric
from deepeval.models import OllamaModel
from deepeval.test_case import LLMTestCase


def main():

    evaluator_model = OllamaModel(
        model="llama3.2:3b",
        base_url="http://localhost:11434",
        temperature=0
    )

    metric = AnswerRelevancyMetric(
        model=evaluator_model,
        threshold=0.5
    )

    test_case = LLMTestCase(
        input="What is the status of payment P1001?",
        actual_output="Payment systems support cancellations and refunds."
    )

    evaluate(
        test_cases=[test_case],
        metrics=[metric]
    )


if __name__ == "__main__":
    main()