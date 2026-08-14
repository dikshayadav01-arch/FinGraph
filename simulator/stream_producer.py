import json
import time


def stream_transactions(transactions, delay=0.5):

    print()
    print("Starting FinGraph transaction stream...")
    print("Press Ctrl+C to stop.")
    print()

    try:

        for transaction in transactions:

            message = json.dumps(transaction)

            print(
                f"STREAM → "
                f"{transaction['sender']} → "
                f"{transaction['receiver']} | "
                f"₹{transaction['amount']}"
            )

            print(message)

            time.sleep(delay)

    except KeyboardInterrupt:

        print()
        print("Transaction stream stopped.")


if __name__ == "__main__":

    print(
        "Stream producer module created successfully."
    )

    print(
        "Kafka integration will be added in a later stage."
    )