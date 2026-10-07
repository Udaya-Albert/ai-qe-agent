# evaluation/manual_agent_eval.py

import json


REQUIRED_TOOLS = {
    "api",
    "db"
}


def evaluate_trace(trace):
    results = {}

    # 1. Check required tools
    tools_called = set(trace["tools_called"])

    missing_tools = REQUIRED_TOOLS - tools_called

    results["required_tools_present"] = len(missing_tools) == 0
    results["missing_tools"] = list(missing_tools)

    # 2. Check duplicate executions
    duplicates = []

    for tool in trace["tools_called"]:
        if trace["tools_called"].count(tool) > 1:
            if tool not in duplicates:
                duplicates.append(tool)

    results["no_duplicate_tools"] = len(duplicates) == 0
    results["duplicate_tools"] = duplicates

    # 3. Check termination
    results["terminated"] = trace["final_action"] == "done"

    # 4. Overall behavioral evaluation
    results["overall_pass"] = (
        results["required_tools_present"]
        and results["no_duplicate_tools"]
        and results["terminated"]
    )

    return results


def evaluate_evidence(trace):
    evidence = trace["evidence"]

    db_status = evidence.get("db", {}).get("status")
    api_status = evidence.get("api", {}).get("status")

    evidence_sufficient = (
        db_status is not None
        and api_status is not None
    )

    evidence_consistent = (
        evidence_sufficient
        and db_status == api_status
    )

    return {
        "db_status": db_status,
        "api_status": api_status,
        "evidence_sufficient": evidence_sufficient,
        "evidence_consistent": evidence_consistent
    }


def evaluate_decisions(trace):
    proposed_actions = trace["proposed_actions"]

    duplicate_proposals = []

    for action in proposed_actions:
        if proposed_actions.count(action) > 1:
            if action not in duplicate_proposals:
                duplicate_proposals.append(action)

    return {
        "duplicate_proposals": duplicate_proposals,
        "no_repeated_proposals": len(duplicate_proposals) == 0
    }


def main():

    real_agent_trace = {
        "proposed_actions": [
            "db",
            "db",
            "db",
            "db",
            "db"
        ],
        "tools_called": [
            "db"
        ],
        "final_action": None,
        "evidence": {
            "db": {
                "status": "CANCELLED"
            }
        }
    }

    evaluation = evaluate_trace(real_agent_trace)

    evidence_evaluation = evaluate_evidence(real_agent_trace)

    decision_evaluation = evaluate_decisions(real_agent_trace)

    final_pass = (
        evaluation["overall_pass"]
        and evidence_evaluation["evidence_sufficient"]
        and evidence_evaluation["evidence_consistent"]
    )

    print("Agent Trace:")
    print(json.dumps(real_agent_trace, indent=2))

    print("\nEvaluation:")
    print(json.dumps(evaluation, indent=2))

    print("\nEvidence Evaluation:")
    print(json.dumps(evidence_evaluation, indent=2))

    print("\nDecision Evaluation:")
    print(json.dumps(decision_evaluation, indent=2))

    print("\nFinal Agent Evaluation:")
    print(f"Overall PASS: {final_pass}")


if __name__ == "__main__":
    main()