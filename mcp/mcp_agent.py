
import asyncio
import json
import ollama

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


MODEL = "llama3.2:3b"

HIGH_RISK_TOOLS = {
    "restart_payment_service"
}


def extract_tool_text(result):
    """
    Extract the actual text returned by the MCP tool.
    Removes MCP SDK wrapper information.
    """

    if result.content:
        return result.content[0].text

    return "{}"


def build_context(tool_name, arguments, result):
    """
    Convert raw MCP tool output into structured evidence
    that is easier for the LLM to understand.
    """

    raw_text = extract_tool_text(result)

    try:
        data = json.loads(raw_text)
    except json.JSONDecodeError:
        data = {
            "raw_result": raw_text
        }

    context = {
        "source": tool_name,
        "arguments": arguments,
        "evidence": data
    }

    return context


async def main():

    # --------------------------------------------------
    # 1. Start MCP Server
    # --------------------------------------------------

    server_params = StdioServerParameters(
        command="python",
        args=["mcp/qe_server.py"]
    )

    async with stdio_client(server_params) as (read, write):

        async with ClientSession(read, write) as session:

            # --------------------------------------------------
            # 2. Initialize MCP connection
            # --------------------------------------------------

            await session.initialize()

            # --------------------------------------------------
            # 3. Discover MCP tools
            # --------------------------------------------------

            tools = await session.list_tools()

            print("\nMCP tools discovered:")

            for tool in tools.tools:
                print(f"- {tool.name}")

            # --------------------------------------------------
            # 4. Agent State
            # --------------------------------------------------

            state = {
                "task": "Investigate payment cancellation",
                "payment_id": "P1001",
                "tools_called": [],
                "evidence": [],
                "iteration": 0
            }

            # --------------------------------------------------
            # 5. Convert MCP tools to Ollama definitions
            # --------------------------------------------------

            ollama_tools = []

            for tool in tools.tools:

                ollama_tools.append({
                    "type": "function",
                    "function": {
                        "name": tool.name,
                        "description": tool.description or "",
                        "parameters": tool.input_schema
                    }
                })

            # --------------------------------------------------
            # 6. Initial user request
            # --------------------------------------------------

            messages = [
                {
                    "role": "user",
                    "content": (
                        "Investigate payment P1001. "
                        "Determine whether the cancellation is reflected "
                        "correctly across the database, API, UI and logs. "
                        "Use the available tools and base your conclusion "
                        "only on the evidence returned by those tools."
                    )
                }
            ]

            # --------------------------------------------------
            # 7. Agent loop
            # --------------------------------------------------

            for iteration in range(5):

                state["iteration"] = iteration + 1

                print(f"\n--- Agent iteration {iteration + 1} ---")

                response = ollama.chat(
                    model=MODEL,
                    messages=messages,
                    tools=ollama_tools
                )

                # --------------------------------------------------
                # 8. No more tools → final response
                # --------------------------------------------------

                if not response.message.tool_calls:

                    print("\nAgent state:")
                    print(json.dumps(state, indent=2))

                    print("\nFinal agent response:")
                    print(response.message.content)

                    break

                # --------------------------------------------------
                # 9. Add LLM response to conversation
                # --------------------------------------------------

                messages.append(response.message)

                # --------------------------------------------------
                # 10. Execute selected MCP tools
                # --------------------------------------------------

                for call in response.message.tool_calls:

                    tool_name = call.function.name
                    arguments = call.function.arguments

                    print(f"Tool selected: {tool_name}")
                    print(f"Arguments: {arguments}")

                    if tool_name in HIGH_RISK_TOOLS:
                        print(f"\n⚠️  Approval required for: {tool_name}")
                        approval = input("Approve this action? (yes/no): ").strip().lower()

                        if approval != "yes":
                            print("❌ Action rejected by human.")
                            break

                        print("✅ Action approved.")

                    result = await session.call_tool(
                        tool_name,
                        arguments=arguments
                    )

                    print("MCP tool result:")
                    print(result)

                    # --------------------------------------------------
                    # 11. Build structured context
                    # --------------------------------------------------

                    context = build_context(
                        tool_name,
                        arguments,
                        result
                    )

                    print("\nStructured context:")
                    print(json.dumps(context, indent=2))

                    # --------------------------------------------------
                    # 12. Update Agent State
                    # --------------------------------------------------

                    state["tools_called"].append(tool_name)

                    state["evidence"].append(context)

                    # --------------------------------------------------
                    # 13. Send engineered context to the LLM
                    # --------------------------------------------------

                    messages.append({
                        "role": "tool",
                        "content": json.dumps(context)
                    })


if __name__ == "__main__":
    asyncio.run(main())

