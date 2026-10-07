from deepeval.tracing import observe, update_current_trace
from deepeval.metrics import TaskCompletionMetric
from deepeval.models import OllamaModel
from deepeval.dataset import EvaluationDataset, Golden


@observe()
def my_agent(query: str) -> str:

    answer = "Payment P1001 is COMPLETED."

    update_current_trace(
        input=query,
        output=answer
    )

    return answer


def main():

    evaluator_model = OllamaModel(
        model="llama3.2:3b",
        base_url="http://localhost:11434",
        temperature=0
    )

    metric = TaskCompletionMetric(
        model=evaluator_model
    )

    golden = Golden(
        input="What is the status of payment P1001?"
    )

    dataset = EvaluationDataset(
        goldens=[golden]
    )

    for golden in dataset.evals_iterator(
        metrics=[metric]
    ):
        result = my_agent(golden.input)

        print("\nAgent response:")
        print(result)


if __name__ == "__main__":
    main()