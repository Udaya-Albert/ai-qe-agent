from mcp.server.mcpserver import MCPServer

mcp = MCPServer("Payment QE Server")


@mcp.tool()
def query_payment_database(payment_id: str) -> dict:
    """
    Query payment information from the database.
    """

    payments = {
        "P1001": {
            "status": "CANCELLED",
            "transaction_type": "FX",
            "cancellation_reason": "FRAUD_CHECK"
        },
        "P1002": {
            "status": "SETTLED",
            "transaction_type": "EQUITY"
        }
    }

    return payments.get(
        payment_id,
        {"error": f"Payment {payment_id} not found"}
    )


if __name__ == "__main__":
    mcp.run()