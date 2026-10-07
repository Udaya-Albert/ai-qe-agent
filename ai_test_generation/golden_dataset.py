golden_cases = [
    {
        "test_id": "TC01",
        "question": "What is the status of payment P1001?",
        "ground_truth": {
            "payment_id": "P1001",
            "status": "CANCELLED"
        },
        "expected_answer": "Payment P1001 is CANCELLED."
    },
    {
        "test_id": "TC02",
        "question": "What is the status of payment P1002?",
        "ground_truth": {
            "payment_id": "P1002",
            "status": "COMPLETED"
        },
        "expected_answer": "Payment P1002 is COMPLETED."
    },
    {
        "test_id": "TC03",
        "question": "What is the status of payment P9999?",
        "ground_truth": {
            "payment_id": "P9999",
            "status": "NOT_FOUND"
        },
        "expected_answer": "Payment P9999 was not found."
    },
    {
        "test_id": "TC04",
        "question": "Can payment P1002 be cancelled?",
        "ground_truth": {
            "payment_id": "P1002",
            "status": "COMPLETED",
            "can_cancel": False
        },
        "expected_answer": "A completed payment cannot be cancelled."
    }
]