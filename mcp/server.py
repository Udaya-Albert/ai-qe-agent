from mcp.server.fastmcp import FastMCP

mcp = FastMCP("AI QE Tools")


@mcp.tool()
def get_payment_status(payment_id: str) -> str:
    """Retrieve the current status of a payment."""

    payments = {
        "P1001": "CANCELLED",
        "P1002": "SETTLED",
        "P1003": "PENDING"
    }

    return payments.get(payment_id, "NOT_FOUND")


if __name__ == "__main__":
    mcp.run()