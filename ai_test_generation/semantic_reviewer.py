from ollama import chat
import json


def review_scenarios(requirement: str, scenarios: list):
    prompt = f"""
You are a senior QE architect reviewing AI-generated test scenarios.

Your job is to identify semantic problems in the generated scenarios.

SOURCE REQUIREMENT:
{requirement}

GENERATED SCENARIOS:
{json.dumps(scenarios, indent=2)}

For EACH scenario, evaluate:

1. GROUNDED
   Is the scenario directly supported by the source requirement?

2. CONTRADICTION
   Does the scenario contradict any rule in the source requirement?

3. DUPLICATE_OR_OVERLAP
   Does the scenario duplicate or substantially overlap another scenario?

4. UNSUPPORTED_BEHAVIOR
   Does the scenario introduce behavior that the requirement does not define?
   Examples:
   - specific error codes
   - retry counts
   - timeout behavior
   - validation rules
   - database fields not mentioned
   - additional payment states
   - repeated-attempt behavior

5. EXPECTED_RESULT_SUPPORTED
   Is the expected result actually supported by the requirement?

Return ONLY valid JSON.

Use this exact structure:

[
  {{
    "scenario_id": "string",
    "grounded": true,
    "contradiction": false,
    "duplicate_or_overlap": false,
    "unsupported_behavior": false,
    "expected_result_supported": true,
    "issues": [
      "string"
    ]
  }}
]

Do not rewrite the scenarios.
Do not invent requirements.
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