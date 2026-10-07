from .golden_dataset import golden_cases


def validate_business_truth(actual_result, ground_truth):

    for field, expected_value in ground_truth.items():

        actual_value = actual_result.get(field)

        if actual_value != expected_value:
            return False

    return True


def run_golden_tests():

    results = []

    simulated_results = {
        "TC01": {
            "payment_id": "P1001",
            "status": "CANCELLED"
        },
        "TC02": {
            "payment_id": "P1002",
            "status": "COMPLETED"
        },
        "TC03": {
            "payment_id": "P9999",
            "status": "NOT_FOUND"
        },
        "TC04": {
            "payment_id": "P1002",
            "status": "COMPLETED",
            "can_cancel": False
        }
    }

    for case in golden_cases:

        actual_result = simulated_results[case["test_id"]]

        passed = validate_business_truth(
            actual_result,
            case["ground_truth"]
        )

        results.append({
            "test_id": case["test_id"],
            "passed": passed
        })

    return results


if __name__ == "__main__":

    results = run_golden_tests()

    for result in results:

        print(
            f"{result['test_id']} "
            f"→ {'PASS' if result['passed'] else 'FAIL'}"
        )