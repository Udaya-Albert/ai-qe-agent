import asyncio

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def main():

    server_params = StdioServerParameters(
        command="python",
        args=["mcp/qe_server.py"],
    )

    async with stdio_client(server_params) as (read, write):

        async with ClientSession(read, write) as session:

            await session.initialize()

            tools = await session.list_tools()

            print("\nAvailable MCP QE tools:")

            for tool in tools.tools:
                print(f"- {tool.name}")

            result = await session.call_tool(
                "query_database",
                arguments={"payment_id": "P1001"}
                )

            print("\nDatabase result:")
            print(result)


            result = await session.call_tool(
                "run_api_test",
                arguments={"payment_id": "P1001"}
                )

            print("\nAPI test result:")
            print(result)


            result = await session.call_tool(
                "run_ui_test",
                 arguments={"payment_id": "P1001"}
                )

            print("\nUI test result:")
            print(result)


            result = await session.call_tool(
                "search_logs",
                arguments={"payment_id": "P1001"}
                )

            print("\nLog result:")
            print(result)    


if __name__ == "__main__":
    asyncio.run(main())