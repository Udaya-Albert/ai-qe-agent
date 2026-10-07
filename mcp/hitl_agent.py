import asyncio
import json
import ollama

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


MODEL = "llama3.2:3b"

HIGH_RISK_TOOLS = {
    "restart_payment_service"
}


async def main():

    server_params = StdioServerParameters(
        command="python",
        args=["mcp/qe_server.py"]
    )

    async with stdio_client(server_params) as (read, write):

        async with ClientSession(read, write) as session:

            await session.initialize()

            tools_result = await session.list_tools()

            print("MCP tools discovered:")
            for tool in tools_result.tools:
                print(f"- {tool.name}")

            ollama_tools = []

            for tool in tools_result.tools:
                ollama_tools.append({
                    "type": "function",
                    "function": {
                        "name": tool.name,
                        "description": tool.description or "",
                        "parameters": tool.input_schema
                    }
                })

            user_prompt = (
                "Restart the payment service for payment P1001. "
                "Use the available tools to perform this action."
            )

            messages = [
                {
                    "role": "user",
                    "content": user_prompt
                }
            ]

            response = ollama.chat(
                model=MODEL,
                messages=messages,
                tools=ollama_tools
            )

            if not response.message.tool_calls:
                print("\nAgent response:")
                print(response.message.content)
                return

            for call in response.message.tool_calls:

                tool_name = call.function.name
                arguments = call.function.arguments

                print(f"\nAgent selected tool: {tool_name}")
                print(f"Arguments: {arguments}")

                # Human-in-the-loop gate
                if tool_name in HIGH_RISK_TOOLS:

                    print(
                        f"\n⚠️  Approval required for: {tool_name}"
                    )

                    approval = input(
                        "Approve this action? (yes/no): "
                    ).strip().lower()

                    if approval != "yes":
                        print("\n❌ Action rejected by human.")
                        return

                    print("\n✅ Action approved.")

                result = await session.call_tool(
                    tool_name,
                    arguments=arguments
                )

                print("\nMCP tool result:")
                print(result)


if __name__ == "__main__":
    asyncio.run(main())