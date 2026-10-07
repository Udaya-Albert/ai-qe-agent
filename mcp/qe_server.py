from mcp.server.mcpserver import MCPServer

mcp = MCPServer("QE MCP Server")


@mcp.tool()
def query_database(payment_id: str) -> dict:
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


@mcp.tool()
def run_api_test(payment_id: str) -> dict:
    """
    Execute an API test for a payment.
    """

    return {
        "test": "Payment API validation",
        "payment_id": payment_id,
        "status_code": 200,
        "result": "PASS"
    }


@mcp.tool()
def run_ui_test(payment_id: str) -> dict:
    """
    Execute a UI test for a payment.
    """

    return {
        "test": "Payment UI validation",
        "payment_id": payment_id,
        "result": "PASS"
    }


@mcp.tool()
def search_logs(payment_id: str) -> dict:
    """
    Search application logs for a payment.
    """

    return {
        "payment_id": payment_id,
        "logs_found": True,
        "message": "Payment cancellation processed successfully",
        "correlation_id": "CORR-1001"
    }

@mcp.tool()
def restart_payment_service() -> dict:
    return {
        "action": "restart_payment_service",
        "service": "payment-service",
        "result": "RESTARTED"
    }

if __name__ == "__main__":
    mcp.run()