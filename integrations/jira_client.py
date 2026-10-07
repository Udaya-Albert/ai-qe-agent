import os
import requests
from dotenv import load_dotenv

load_dotenv()

JIRA_BASE_URL = os.getenv("JIRA_BASE_URL")
JIRA_EMAIL = os.getenv("JIRA_EMAIL")
JIRA_API_TOKEN = os.getenv("JIRA_API_TOKEN")


def get_issue(issue_key: str):
    url = f"{JIRA_BASE_URL}/rest/api/3/issue/{issue_key}"

    response = requests.get(
        url,
        auth=(JIRA_EMAIL, JIRA_API_TOKEN),
        headers={
            "Accept": "application/json"
        },
        timeout=10
    )

    response.raise_for_status()

    return response.json()
def extract_text_from_adf(node):
    """
    Recursively extracts human-readable text from Jira's
    Atlassian Document Format (ADF).
    """

    if isinstance(node, dict):

        if node.get("type") == "text":
            return node.get("text", "")

        text_parts = []

        for child in node.get("content", []):
            text_parts.append(extract_text_from_adf(child))

        return "\n".join(
            part for part in text_parts if part
        )

    if isinstance(node, list):
        return "\n".join(
            extract_text_from_adf(item)
            for item in node
        )

    return ""

if __name__ == "__main__":
    issue = get_issue("SCRUM-5")

    summary = issue["fields"]["summary"]
    description = issue["fields"]["description"]

    requirement_text = extract_text_from_adf(description)

    print("Issue Key:", issue["key"])
    print("Summary:", summary)
    print("\nRequirement:")
    print(requirement_text)