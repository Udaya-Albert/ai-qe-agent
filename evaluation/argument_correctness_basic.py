from deepeval import evaluate
from deepeval.metrics import ArgumentCorrectnessMetric
from deepeval.models import OllamaModel
from deepeval.test_case import LLMTestCase, ToolCall


def main():

    evaluator_model = OllamaModel(
        model="llama3.2:3b",
        base_url="http://localhost:11434",
        temperature=0
    )

    metric = ArgumentCorrectnessMetric(
        model=evaluator_model,
        threshold=0.5,
        include_reason=True
    )

    test_case = LLMTestCase(
        input="What is the status of payment P1001?",

        actual_output="Payment P1001 is CANCELLED.",

        tools_called=[
            ToolCall(
                name="query_payment_database",
                input_parameters={
                    "payment_id": "P9999"
                },
                output={
                    "status": "CANCELLED"
                }
            )
        ]
    )

    evaluate(
        test_cases=[test_case],
        metrics=[metric]
    )


if __name__ == "__main__":
    main()