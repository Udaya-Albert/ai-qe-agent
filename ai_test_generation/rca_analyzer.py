from ollama import chat
import json


def analyze_failure(failure_evidence: dict):

    prompt = f"""
You are an AI-assisted QE failure analysis system.

Analyze the supplied failure evidence.

IMPORTANT RULES:

1. Use ONLY the supplied evidence.
2. Do not invent logs, database records, API behavior,
   infrastructure events, or application behavior.
3. Separate observed facts from hypotheses.
4. If evidence conflicts, explicitly report the conflict.
5. If evidence is insufficient, use INSUFFICIENT_EVIDENCE.
6. Do not claim a hypothesis is proven unless the evidence
   directly proves it.
7. Confidence must be HIGH, MEDIUM, or LOW.
8. Return ONLY valid JSON.

Allowed classifications:

TEST_DEFECT
APPLICATION_DEFECT
DATA_ISSUE
INFRASTRUCTURE_ISSUE
SYNC_OR_PROPAGATION_ISSUE
INSUFFICIENT_EVIDENCE

FAILURE EVIDENCE:

{json.dumps(failure_evidence, indent=2)}

Return exactly:

{{
    "classification": "string",
    "confidence": "HIGH | MEDIUM | LOW",
    "observed_facts": [],
    "hypothesis": "string",
    "supporting_evidence": [],
    "missing_evidence": [],
    "recommended_next_check": "string"
}}
"""

    response = chat(
        model="llama3.2:3b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return json.loads(response["message"]["content"])


if __name__ == "__main__":

    failure_evidence = {
    "test_name": "cancelPendingPayment",
    "expected": "CANCELLED",
    "actual": "PENDING",

    "api_response": {
        "paymentId": "P1001",
        "status": "PENDING"
    },

    "database_result": {
        "paymentId": "P1001",
        "status": "PENDING"
    },

    "application_logs": """
    paymentId=P1001
    correlationId=CORR-1001
    Cancellation request rejected:
    Payment is not in cancellable state
    """
}

    result = analyze_failure(failure_evidence)

    print("\nRCA Result:\n")
    print(json.dumps(result, indent=2))