import csv
import random
import uuid
from datetime import datetime, timedelta

# Configuration

ACCOUNTS = [f"ACC{number:03d}" for number in range(1, 101)]

SHELL_ACCOUNT = "SHELL001"

OUTPUT_FILE = "data/raw/transactions.csv"

# Transaction Generator

def generate_transaction(
    sender,
    receiver,
    amount,
    transaction_type="NORMAL"
):
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

# 1. Normal Transactions

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

# 2. Starburst Pattern

def generate_starburst_transactions(number=50):

    transactions = []

    suspicious_accounts = random.sample(
        ACCOUNTS,
        number
    )

    for account in suspicious_accounts:

        transaction = generate_transaction(
            account,
            SHELL_ACCOUNT,
            9900,
            "STARBURST"
        )

        transactions.append(transaction)

    return transactions

# 3. Circular Money Flow

def generate_circular_transactions():

    transactions = []

    # A → B → C → A

    accounts = random.sample(ACCOUNTS, 3)

    account_a = accounts[0]
    account_b = accounts[1]
    account_c = accounts[2]

    transactions.append(
        generate_transaction(
            account_a,
            account_b,
            8500,
            "CIRCULAR"
        )
    )

    transactions.append(
        generate_transaction(
            account_b,
            account_c,
            8200,
            "CIRCULAR"
        )
    )

    transactions.append(
        generate_transaction(
            account_c,
            account_a,
            7900,
            "CIRCULAR"
        )
    )

    return transactions

# 4. Smurfing Pattern

def generate_smurfing_transactions(
    number=30
):

    transactions = []

    target_account = "SMURF_TARGET"

    suspicious_accounts = random.sample(
        ACCOUNTS,
        number
    )

    for account in suspicious_accounts:

        amount = random.uniform(
            8000,
            9900
        )

        transaction = generate_transaction(
            account,
            target_account,
            amount,
            "SMURFING"
        )

        transactions.append(transaction)

    return transactions

# Save Transactions

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

# Main Program

def main():

    print("Generating FinGraph transaction data...")

    normal_transactions = (
        generate_normal_transactions(500)
    )

    starburst_transactions = (
        generate_starburst_transactions(50)
    )

    circular_transactions = (
        generate_circular_transactions()
    )

    smurfing_transactions = (
        generate_smurfing_transactions(30)
    )

    transactions = (
        normal_transactions
        + starburst_transactions
        + circular_transactions
        + smurfing_transactions
    )

    random.shuffle(transactions)

    save_transactions(transactions)

    print()
    print("FinGraph dataset generated successfully!")
    print()
    print(f"Total transactions: {len(transactions)}")
    print()
    print("Transaction breakdown:")
    print(f"Normal: {len(normal_transactions)}")
    print(f"Starburst: {len(starburst_transactions)}")
    print(f"Circular: {len(circular_transactions)}")
    print(f"Smurfing: {len(smurfing_transactions)}")
    print()
    print(f"Saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()