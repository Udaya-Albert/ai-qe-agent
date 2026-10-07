from deepeval.metrics import BaseMetric
from deepeval.test_case import LLMTestCase
from deepeval import evaluate


class PaymentStatusCorrectnessMetric(BaseMetric):

    def __init__(self, expected_status: str, threshold: float = 0.5):
        self.expected_status = expected_status.upper()
        self.threshold = threshold
        self.score = 0.0
        self.reason = ""

    def measure(self, test_case: LLMTestCase) -> float:

        actual = test_case.actual_output.upper()

        if self.expected_status in actual:
            self.score = 1.0
            self.reason = (
                f"Expected payment status '{self.expected_status}' "
                f"was found in the actual output."
            )
        else:
            self.score = 0.0
            self.reason = (
                f"Expected payment status '{self.expected_status}' "
                f"was not found in the actual output."
            )

        return self.score

    async def a_measure(self, test_case: LLMTestCase) -> float:
        return self.measure(test_case)

    @property
    def __name__(self):
        return "Payment Status Correctness"

def main():

        metric = PaymentStatusCorrectnessMetric(
            expected_status="CANCELLED"
        )

        test_case = LLMTestCase(
            input="What is the status of payment P1001?",
            actual_output="Payment P1001 is COMPLETED."
        )
        score = metric.measure(test_case)

        print("Metric name:", metric.__name__)
        print("Score:", score)
        print("Reason:", metric.reason)
        print("Passed:", metric.is_successful())

        evaluate(
         test_cases=[test_case],
         metrics=[metric]
        )


if __name__ == "__main__":
        main()