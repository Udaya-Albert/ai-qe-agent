from ollama import chat
import json

from ai_test_generation.scenario_validator import validate_scenarios
from ai_test_generation.semantic_reviewer import review_scenarios


def generate_test_scenarios(requirement: str):

    prompt = f"""
You are a senior QE architect generating candidate test scenarios
from a software requirement.

Requirement:

{requirement}

Generate DISTINCT candidate test scenarios.

IMPORTANT:

Generate test scenarios, NOT individual requirement statements.

A single test scenario may validate multiple related requirements.

For example, if a requirement states:

- PENDING payment can be cancelled
- payment status becomes CANCELLED
- cancellation reason is stored

these should normally be combined into ONE end-to-end scenario
rather than creating three separate scenarios.

Do not create separate scenarios merely by splitting one requirement
into individual assertions.

For each scenario provide:

1. Scenario ID
2. Scenario description
3. Expected result
4. Classification:
   - DIRECT
   - INFERRED
   - UNSUPPORTED
5. Evidence from the requirement explaining the classification

Classification rules:

DIRECT:
The requirement explicitly states or clearly requires this behavior.

INFERRED:
The scenario is a reasonable interpretation of the requirement,
but the behavior is not explicitly specified.

UNSUPPORTED:
The scenario requires assumptions about functionality, validation,
error codes, retry policies, timeouts, fields, or business rules
that are not present in the requirement.

Important rules:

- Do not invent APIs, database fields, error codes, retry counts,
  timeout values, validation rules, or business rules.
- Do not assume that a failure scenario has a particular outcome
  unless the requirement specifies it.
- Do not invent HTTP status codes.
- Do not invent error messages.
- Do not invent retry behavior.
- Do not invent validation rules.
- Do not invent additional payment states.
- Avoid duplicate scenarios.
- If two scenarios test the same business behavior, merge them.
- Prefer meaningful end-to-end scenarios over splitting one business
  requirement into multiple trivial scenarios.
- Include positive, negative, state-transition and consistency
  scenarios where they are supported by the requirement.
- These are candidate scenarios and must be reviewed by QE.
- Do not treat UNSUPPORTED scenarios as approved tests.

EXPECTED RESULT RULES:

The expected_result must describe the actual observable outcome.

Do NOT use boolean values such as:
"true"
"false"

Do NOT use vague results such as:
"test passes"
"test fails"
"error occurs"

Instead describe the expected business/system behavior.

For example:

"Payment status changes from PENDING to CANCELLED and the
cancellation reason is stored."

For a negative scenario:

"The payment is not cancelled and its status does not transition
to CANCELLED."

Before returning the scenarios, internally check:

1. Are scenarios grounded in the requirement?
2. Are any scenarios duplicates?
3. Are any scenarios simply individual assertions from another
   scenario?
4. Does every expected result describe an observable outcome?
5. Did the scenario introduce behavior not present in the requirement?

Return ONLY valid JSON.

Return a JSON array using exactly this structure:

[
  {{
    "scenario_id": "string",
    "description": "string",
    "expected_result": "string",
    "classification": "DIRECT | INFERRED | UNSUPPORTED",
    "evidence": "string"
  }}
]

Do not include markdown.
Do not include ```json.
Do not include any explanation before or after the JSON.
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

    requirement = """
A payment can be cancelled only when its current status is PENDING.
Once cancelled, the payment status must become CANCELLED
and the cancellation reason must be stored.
A completed payment cannot be cancelled.

Acceptance Criteria:
A PENDING payment can be cancelled.
The payment status becomes CANCELLED.
A cancellation reason is stored.
A COMPLETED payment cannot be cancelled.
The API and database must reflect the same final state.
"""

    scenarios = generate_test_scenarios(requirement)

    print("\nGenerated Test Scenarios:\n")
    print(json.dumps(scenarios, indent=2))

    validation_errors = validate_scenarios(scenarios)

    print("\nValidation Result:")

    if validation_errors:
        print("FAILED")

        for error in validation_errors:
            print("-", error)

    else:
        print("PASSED")

    print("\nSemantic Review:\n")

    review_result = review_scenarios(
        requirement,
        scenarios
    )

    print(json.dumps(review_result, indent=2))