import argparse
import json
import time

from kafka import KafkaProducer


# -----------------------------
# FinGraph Kafka Configuration
# -----------------------------

INPUT_FILE = "data/processed/transactions.jsonl"

KAFKA_BOOTSTRAP_SERVERS = "172.19.176.1:9092"
KAFKA_TOPIC = "fin_transactions"

# Producer configuration
KAFKA_ACKS = "all"
KAFKA_RETRIES = 5
KAFKA_REQUEST_TIMEOUT_MS = 10000


def create_kafka_producer():

    producer = KafkaProducer(
    bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
    acks=KAFKA_ACKS,
    retries=KAFKA_RETRIES,
    request_timeout_ms=KAFKA_REQUEST_TIMEOUT_MS,
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

    successful = 0
    failed = 0

    try:

        for transaction in transactions:

            future = producer.send(
                KAFKA_TOPIC,
                value=transaction
            )

            try:

                metadata = future.get(timeout=10)

                successful += 1

                print(
                    f"KAFKA ✓ "
                    f"{transaction['sender']} → "
                    f"{transaction['receiver']} | "
                    f"partition={metadata.partition} "
                    f"offset={metadata.offset}"
                )

            except Exception as error:

                failed += 1

                print(
                    f"KAFKA ✗ Failed to send "
                    f"{transaction['transaction_id']}"
                )

                print(f"Error: {error}")

            time.sleep(delay)

        producer.flush()

        print()
        print("------------------------------")
        print("Kafka Stream Summary")
        print("------------------------------")
        print(f"Successful: {successful}")
        print(f"Failed:     {failed}")
        print(f"Total:      {successful + failed}")
        print("------------------------------")

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

    print("--------------------------------")
    print("FinGraph Kafka Producer")
    print("--------------------------------")
    print(f"Kafka server: {KAFKA_BOOTSTRAP_SERVERS}")
    print(f"Kafka topic:  {KAFKA_TOPIC}")
    print(f"Input file:   {INPUT_FILE}")
    print("--------------------------------")

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