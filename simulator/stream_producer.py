import argparse
import json
import time


INPUT_FILE = "data/processed/transactions.jsonl"


def load_transactions():

    transactions = []

    with open(
        INPUT_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        for line in file:

            line = line.strip()

            if line:

                transaction = json.loads(line)

                transactions.append(transaction)

    return transactions


def stream_transactions(
    transactions,
    limit=None,
    delay=0.5
):

    if limit is not None:

        transactions = transactions[:limit]

    print()
    print("Starting FinGraph transaction stream...")
    print(f"Transactions to stream: {len(transactions)}")
    print(f"Delay between transactions: {delay} seconds")
    print("Press Ctrl+C to stop.")
    print()

    try:

        for transaction in transactions:

            message = json.dumps(transaction)

            print(
                f"STREAM → "
                f"{transaction['sender']} → "
                f"{transaction['receiver']} | "
                f"₹{transaction['amount']:.2f}"
            )

            print(message)

            time.sleep(delay)

    except KeyboardInterrupt:

        print()
        print("Transaction stream stopped.")


def parse_arguments():

    parser = argparse.ArgumentParser(
        description="FinGraph transaction stream producer"
    )

    parser.add_argument(
        "--limit",
        type=int,
        default=20,
        help="Number of transactions to stream"
    )

    parser.add_argument(
        "--delay",
        type=float,
        default=0.5,
        help="Delay between transactions in seconds"
    )

    return parser.parse_args()


def main():

    args = parse_arguments()

    transactions = load_transactions()

    print(
        f"Loaded {len(transactions)} transactions "
        f"from {INPUT_FILE}"
    )

    stream_transactions(
        transactions,
        limit=args.limit,
        delay=args.delay
    )


if __name__ == "__main__":
    main()