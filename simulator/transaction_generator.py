import csv
import random
import uuid
from datetime import datetime, timedelta


ACCOUNTS = [f"ACC{number:03d}" for number in range(1, 101)]

OUTPUT_FILE = "data/raw/transactions.csv"


def generate_transaction(sender, receiver, amount, transaction_type="NORMAL"):
    timestamp = datetime.now() - timedelta(
        seconds=random.randint(0, 3600)
    )

    return {
        "transaction_id": str(uuid.uuid4()),
        "timestamp": timestamp.isoformat(),
        "sender": sender,
        "receiver": receiver,
        "amount": round(amount, 2),
        "transaction_type": transaction_type,
        "sender_ip": f"192.168.1.{random.randint(1, 254)}",
        "receiver_country": random.choice(
            ["India", "USA", "UK", "Singapore", "UAE"]
        )
    }


def generate_normal_transactions(number=500):
    transactions = []

    for _ in range(number):
        sender, receiver = random.sample(ACCOUNTS, 2)

        amount = random.uniform(100, 5000)

        transaction = generate_transaction(
            sender,
            receiver,
            amount,
            "NORMAL"
        )

        transactions.append(transaction)

    return transactions


def generate_starburst_transactions():
    transactions = []

    shell_account = "SHELL001"

    suspicious_accounts = random.sample(ACCOUNTS, 50)

    for account in suspicious_accounts:

        transaction = generate_transaction(
            account,
            shell_account,
            9900,
            "STARBURST"
        )

        transactions.append(transaction)

    return transactions


def save_transactions(transactions):
    fieldnames = [
        "transaction_id",
        "timestamp",
        "sender",
        "receiver",
        "amount",
        "transaction_type",
        "sender_ip",
        "receiver_country"
    ]

    with open(
        OUTPUT_FILE,
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames
        )

        writer.writeheader()
        writer.writerows(transactions)


def main():

    print("Generating FinGraph transaction data...")

    normal_transactions = generate_normal_transactions(500)

    starburst_transactions = generate_starburst_transactions()

    transactions = normal_transactions + starburst_transactions

    random.shuffle(transactions)

    save_transactions(transactions)

    print(f"Generated {len(transactions)} transactions.")
    print(f"Saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()