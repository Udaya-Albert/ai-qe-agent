
from ollama import chat
import json


def find_candidate_with_ai(
    original_locator,
    available_elements,
    test_intent
):

    prompt = f"""
You are helping a UI test automation system find a replacement
for a broken locator.

TEST INTENT:
{test_intent}

ORIGINAL LOCATOR:
{original_locator}

CURRENTLY AVAILABLE ELEMENTS:
{json.dumps(available_elements)}

Rules:

1. Identify an element that represents the SAME UI element.
2. The replacement must preserve the exact test intent.
3. Do not select an element merely because it is related
   to the same business domain.
4. "Cancel specific payment" is NOT the same as
   "Refund payment" or "Cancel all payments".
5. Do not invent an element.
6. If no safe candidate exists, return null.
7. Return ONLY valid JSON.
8. Do not use Markdown.
9. Do not add any explanation outside the JSON.

Return exactly:

{{
    "candidate": "element or null",
    "reason": "short explanation"
}}
"""

    response = chat(
        model="llama3.2:3b",
        messages=[{"role": "user", "content": prompt}]
    )

    content = response["message"]["content"]

    return json.loads(content)


def validate_candidate_exists(candidate, available_elements):

    if candidate is None:
        return False

    return candidate in available_elements


def validate_business_intent(candidate, test_intent):

    """
    Deterministic safety policy.

    The candidate must not perform a different business action
    from the original test intent.
    """

    if candidate is None:
        return False

    intent = test_intent.lower()
    candidate_name = candidate.lower()

    # Specific payment cancellation
    if "cancel the specific payment" in intent:

        if "refund" in candidate_name:
            return False

        if "cancelall" in candidate_name:
            return False

        if "cancel" not in candidate_name:
            return False

    return True


if __name__ == "__main__":

    original_locator = "#cancel-payment"

    test_intent = "Cancel the specific payment"

    available_elements = [
       "#cancelPaymentBtn",
        "#refund-payment",
        "#cancelAllPayments"
    ]

    result = find_candidate_with_ai(
        original_locator,
        available_elements,
        test_intent
    )

    print("\nAI Result:\n")
    print(json.dumps(result, indent=2))

    candidate = result["candidate"]

    element_valid = validate_candidate_exists(
        candidate,
        available_elements
    )

    intent_valid = validate_business_intent(
        candidate,
        test_intent
    )

    print("\nValidation:")
    print("Element exists:", element_valid)
    print("Intent preserved:", intent_valid)

    if element_valid and intent_valid:
        print("\n✅ Safe to heal:", candidate)
    else:
        print("\n❌ Healing rejected")

