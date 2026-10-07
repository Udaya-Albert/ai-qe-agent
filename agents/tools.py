def get_payment_status(payment_id: str) -> str:
    """
    Retrieve payment status for a given payment ID.
    """

    payments = {
        "P1001": "CANCELLED",
        "P1002": "SETTLED",

        "P1003": "PENDING"
    }

    return payments.get(payment_id, "NOT_FOUND")


def query_payment_database(payment_id: str) -> str:
    """Retrieve payment information from the database."""

    database = {
        "P1001": {
            "status": "CANCELLED",
            "transaction_type": "PAYMENT",
        },
        "P1002": {
            "status": "SETTLED",
            "transaction_type": "PAYMENT",
        },
        "P1003": {
            "status": "PENDING",
            "transaction_type": "PAYMENT",
        }
    }

    payment = database.get(payment_id)

    if payment is None:
        return "NOT_FOUND"

    return str(payment)


def get_payment_logs(payment_id: str) -> str:
    """Retrieve application logs related to a payment."""

    logs = {
        "P1001": (
            "Cancellation request received. "
            "Payment status update failed because "
            "downstream settlement service returned TIMEOUT."
        ),
        "P1002": (
            "Payment settled successfully. "
            "No cancellation activity found."
        ),
        "P1003": (
            "Cancellation request is still being processed."
        )
    }

    return logs.get(payment_id, "NO_LOGS_FOUND")    


def check_downstream_service() -> str:
    """Check the health of the downstream settlement service."""

    return (
        "Settlement service is currently healthy. "
        "Response time: 120 ms. "
        "No active incidents detected."
    )

