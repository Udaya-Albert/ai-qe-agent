
from ollama import chat

from agents.tools import (
    get_payment_status,
    query_payment_database,
    get_payment_logs,
    check_downstream_service
)


MAX_ITERATIONS = 6


def execute_tool(tool_name, arguments):

    if tool_name == "get_payment_status":
        return get_payment_status(
            arguments["payment_id"]
        )

    elif tool_name == "query_payment_database":
        return query_payment_database(
            arguments["payment_id"]
        )

    elif tool_name == "get_payment_logs":
        return get_payment_logs(
            arguments["payment_id"]
        )

    elif tool_name == "check_downstream_service":
        return check_downstream_service()

    else:
        return f"Unknown tool: {tool_name}"


def run_agent(user_request: str):

    execution_trace = []

    tools = [
        get_payment_status,
        query_payment_database,
        get_payment_logs,
        check_downstream_service
    ]

    messages = [
        {
            "role": "system",
            "content": """
You are an AI QE investigation agent.

Your goal is to investigate the user's problem and determine
what evidence is required to reach a reliable conclusion.

Available tools:

- get_payment_status
- query_payment_database
- get_payment_logs
- check_downstream_service

Important:

You are NOT given a predefined investigation sequence.

You must reason about which evidence is useful based on the
information you observe.

After each tool result:

1. Analyze the evidence.
2. Identify what is still unknown.
3. Decide whether another tool is necessary.
4. Select the next tool based on the evidence.

You may stop when you have enough evidence to answer the
user's question.

Rules:

- Never invent factual information.
- Use tools when factual evidence is required.
- Do not claim that a tool was executed unless it actually was.
- Do not assume the result of a tool before calling it.
- Prefer evidence over assumptions.
- If evidence is insufficient, explicitly say so.
"""
        },
        {
            "role": "user",
            "content": user_request
        }
    ]

    for iteration in range(MAX_ITERATIONS):

        print(f"\n--- Agent iteration {iteration + 1} ---")

        response = chat(
            model="llama3.2:3b",
            messages=messages,
            tools=tools
        )

        message = response["message"]

        messages.append(message)

        if not message.tool_calls:

            final_prompt = f"""
Generate the final investigation result.

User request:

{user_request}

Verified execution trace:

{execution_trace}

Use ONLY information contained in the execution trace.

Do not invent:
- database values
- timestamps
- error codes
- reasons
- tool results

Clearly separate:
- verified facts
- reasonable interpretation
- remaining uncertainty
"""

            messages.append(
                {
                    "role": "user",
                    "content": final_prompt
                }
            )

            final_response = chat(
                model="llama3.2:3b",
                messages=messages
            )

            print("\nVerified execution trace:")

            for item in execution_trace:
                print(item)

            print(
                "\nFinal answer:",
                final_response["message"]["content"]
            )

            return

        for tool_call in message.tool_calls:

            tool_name = tool_call.function.name
            arguments = tool_call.function.arguments

            print("Tool selected:", tool_name)
            print("Arguments:", arguments)

            result = execute_tool(
                tool_name,
                arguments
            )

            print("Tool result:", result)

            execution_trace.append(
                {
                    "tool": tool_name,
                    "arguments": arguments,
                    "result": result
                }
            )

            messages.append(
                {
                    "role": "tool",
                    "tool_name": tool_name,
                    "content": result
                }
            )

    print("\nAgent stopped: maximum iterations reached.")

    print("\nVerified execution trace:")

    for item in execution_trace:
        print(item)


if __name__ == "__main__":

    run_agent(
        "Investigate why payment P1001 cancellation is inconsistent "
        "and determine what additional evidence you need."
    )

