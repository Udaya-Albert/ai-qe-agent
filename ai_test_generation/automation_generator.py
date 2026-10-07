from ollama import chat


def generate_automation(scenario: dict, framework_context: str,api_contract: str):

    prompt = f"""
You are a senior SDET generating automation code.

Generate a RestAssured Java test for the approved test scenario.

APPROVED TEST SCENARIO:
{scenario}

API CONTRACT:
{api_contract}

EXISTING FRAMEWORK CONTEXT:
{framework_context}

Rules:

1. Generate only the test method.
2. Use the existing framework abstractions when provided.
3. Use the API contract as the authoritative source for:
   - HTTP method
   - endpoint
   - request structure
   - response fields
   - HTTP status codes
4. Use the approved scenario as the authoritative source
   for business behavior and expected outcomes.
5. Do not invent APIs, endpoints, response fields,
   status codes, database fields, or business rules.
6. Assertions must correspond directly to the expected result
   and API contract.
7. Reuse existing framework clients and utilities.
8. Do not create new framework or utility classes.
9. Do not include markdown fences.
10. Return only valid Java code.
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

    return response["message"]["content"]

if __name__ == "__main__":

    scenario = {
        "scenario_id": "cancel_pending_payment",
        "description": "A PENDING payment can be cancelled.",
        "expected_result":
            "Payment status changes from PENDING to CANCELLED "
            "and the cancellation reason is stored."
    }

    framework_context = """
Existing API client:

public Response cancelPayment(
        String paymentId,
        String reason) {

    return given()
        .body(Map.of(
            "reason", reason
        ))
        .when()
        .post("/payments/" + paymentId + "/cancel");
}

Framework:
- Java
- RestAssured
- TestNG
- Existing PaymentClient
- Tests should reuse PaymentClient
"""

    api_contract = """
POST /payments/{paymentId}/cancel

Path parameter:
- paymentId

Request body:
{
    "reason": "string"
}

Response:
HTTP 200

{
    "status": "COMPLETED",
    "cancellationReason": "string"
}
"""

    generated_code = generate_automation(
        scenario,
        framework_context,
        api_contract
    )

    print("\nGenerated Automation:\n")
    print(generated_code)