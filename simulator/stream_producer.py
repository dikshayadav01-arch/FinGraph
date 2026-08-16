import argparse
import json
import time

from kafka import KafkaProducer


INPUT_FILE = "data/processed/transactions.jsonl"

KAFKA_BOOTSTRAP_SERVERS = "localhost:9092"
KAFKA_TOPIC = "fin_transactions"


def create_kafka_producer():

    producer = KafkaProducer(
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        value_serializer=lambda value: json.dumps(value).encode("utf-8")
    )

    return producer


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
    producer,
    transactions,
    limit=None,
    delay=0.5
):

    if limit is not None:

        transactions = transactions[:limit]

    print()
    print("Starting FinGraph Kafka transaction stream...")
    print(f"Kafka topic: {KAFKA_TOPIC}")
    print(f"Transactions to stream: {len(transactions)}")
    print(f"Delay between transactions: {delay} seconds")
    print("Press Ctrl+C to stop.")
    print()

    try:

        for transaction in transactions:

            producer.send(
                KAFKA_TOPIC,
                value=transaction
            )

            print(
                f"STREAM → "
                f"{transaction['sender']} → "
                f"{transaction['receiver']} | "
                f"₹{transaction['amount']:.2f}"
            )

            time.sleep(delay)

        producer.flush()

        print()
        print("All transactions sent to Kafka.")

    except KeyboardInterrupt:

        producer.flush()

        print()
        print("Transaction stream stopped.")


def parse_arguments():

    parser = argparse.ArgumentParser(
        description="FinGraph Kafka transaction producer"
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

    print("Connecting to Kafka...")

    producer = create_kafka_producer()

    print("Connected to Kafka successfully.")

    transactions = load_transactions()

    print(
        f"Loaded {len(transactions)} transactions "
        f"from {INPUT_FILE}"
    )

    stream_transactions(
        producer,
        transactions,
        limit=args.limit,
        delay=args.delay
    )

    producer.close()


if __name__ == "__main__":
    main()