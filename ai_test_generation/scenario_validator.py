VALID_CLASSIFICATIONS = {
    "DIRECT",
    "INFERRED",
    "UNSUPPORTED"
}


def validate_scenarios(scenarios):

    errors = []

    scenario_ids = set()

    for index, scenario in enumerate(scenarios, start=1):

        prefix = f"Scenario {index}"

        # Required fields
        required_fields = [
            "scenario_id",
            "description",
            "expected_result",
            "classification",
            "evidence"
        ]

        for field in required_fields:
            if field not in scenario:
                errors.append(
                    f"{prefix}: Missing field '{field}'"
                )

        # Skip further validation if required fields are missing
        if not all(field in scenario for field in required_fields):
            continue

        # Duplicate scenario ID
        scenario_id = scenario["scenario_id"]

        if scenario_id in scenario_ids:
            errors.append(
                f"{prefix}: Duplicate scenario ID '{scenario_id}'"
            )

        scenario_ids.add(scenario_id)

        # Validate classification
        classification = scenario["classification"]

        if classification not in VALID_CLASSIFICATIONS:
            errors.append(
                f"{prefix}: Invalid classification "
                f"'{classification}'"
            )

        # Unsupported scenarios should explain why
        if classification == "UNSUPPORTED":

            if not scenario["evidence"].strip():
                errors.append(
                    f"{prefix}: UNSUPPORTED scenario "
                    f"must provide evidence/explanation"
                )

    return errors