import csv
import random
import uuid
from datetime import datetime, timedelta

# Configuration

NUM_ACCOUNTS = 100

NORMAL_TRANSACTION_COUNT = 500
STARBURST_ACCOUNT_COUNT = 50
SMURFING_ACCOUNT_COUNT = 30

OUTPUT_FILE = "data/raw/transactions.csv"

COUNTRIES = [
    "India",
    "USA",
    "UK",
    "Singapore",
    "UAE"
]

# Account Profiles

def create_account_profiles():

    accounts = {}

    for number in range(1, NUM_ACCOUNTS + 1):

        account_id = f"ACC{number:03d}"

        accounts[account_id] = {
            "account_id": account_id,
            "ip": f"192.168.1.{number}",
            "country": random.choice(COUNTRIES)
        }

    return accounts

# Generate Timestamp

def generate_timestamp():

    start_time = datetime.now() - timedelta(days=1)

    random_seconds = random.randint(
        0,
        24 * 60 * 60
    )

    timestamp = start_time + timedelta(
        seconds=random_seconds
    )

    return timestamp.isoformat()

# Transaction Generator

def generate_transaction(
    sender,
    receiver,
    amount,
    transaction_type,
    accounts
):

    return {
        "transaction_id": str(uuid.uuid4()),

        "timestamp": generate_timestamp(),

        "sender": sender,

        "receiver": receiver,

        "amount": round(amount, 2),

        "transaction_type": transaction_type,

        "sender_ip": accounts[sender]["ip"],

        "sender_country": accounts[sender]["country"],

        "receiver_country": (
            accounts.get(
                receiver,
                {"country": random.choice(COUNTRIES)}
            )["country"]
        )
    }

# Normal Transactions

def generate_normal_transactions(
    accounts,
    number=NORMAL_TRANSACTION_COUNT
):

    transactions = []

    account_ids = list(accounts.keys())

    for _ in range(number):

        sender, receiver = random.sample(
            account_ids,
            2
        )

        amount = random.uniform(
            100,
            5000
        )

        transaction = generate_transaction(
            sender,
            receiver,
            amount,
            "NORMAL",
            accounts
        )

        transactions.append(transaction)

    return transactions

# Starburst Pattern

def generate_starburst_transactions(
    accounts,
    number=STARBURST_ACCOUNT_COUNT
):

    transactions = []

    shell_account = "SHELL001"

    suspicious_accounts = random.sample(
        list(accounts.keys()),
        number
    )

    for account in suspicious_accounts:

        amount = random.uniform(
            9500,
            9900
        )

        transaction = generate_transaction(
            account,
            shell_account,
            amount,
            "STARBURST",
            accounts
        )

        transactions.append(transaction)

    return transactions

# Circular Money Flow

def generate_circular_transactions(accounts):

    transactions = []

    account_a, account_b, account_c = random.sample(
        list(accounts.keys()),
        3
    )

    transactions.append(
        generate_transaction(
            account_a,
            account_b,
            random.uniform(7000, 9000),
            "CIRCULAR",
            accounts
        )
    )

    transactions.append(
        generate_transaction(
            account_b,
            account_c,
            random.uniform(7000, 9000),
            "CIRCULAR",
            accounts
        )
    )

    transactions.append(
        generate_transaction(
            account_c,
            account_a,
            random.uniform(7000, 9000),
            "CIRCULAR",
            accounts
        )
    )

    return transactions

# Smurfing Pattern

def generate_smurfing_transactions(
    accounts,
    number=SMURFING_ACCOUNT_COUNT
):

    transactions = []

    target_account = "SMURF_TARGET"

    suspicious_accounts = random.sample(
        list(accounts.keys()),
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
            "SMURFING",
            accounts
        )

        transactions.append(transaction)

    return transactions

# Save Dataset

def save_transactions(transactions):

    fieldnames = [
        "transaction_id",
        "timestamp",
        "sender",
        "receiver",
        "amount",
        "transaction_type",
        "sender_ip",
        "sender_country",
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

# Generate Summary

def print_summary(transactions):

    counts = {}

    total_amount = 0

    for transaction in transactions:

        transaction_type = transaction[
            "transaction_type"
        ]

        counts[transaction_type] = (
            counts.get(transaction_type, 0) + 1
        )

        total_amount += transaction["amount"]

    print()
    print("Transaction Summary")
    print("-------------------")

    for transaction_type, count in counts.items():

        print(
            f"{transaction_type}: {count}"
        )

    print(
        f"Total transactions: {len(transactions)}"
    )

    print(
        f"Total transaction value: "
        f"₹{total_amount:,.2f}"
    )

# Main

def main():

    print(
        "Generating FinGraph transaction network..."
    )

    accounts = create_account_profiles()

    normal_transactions = (
        generate_normal_transactions(accounts)
    )

    starburst_transactions = (
        generate_starburst_transactions(accounts)
    )

    circular_transactions = (
        generate_circular_transactions(accounts)
    )

    smurfing_transactions = (
        generate_smurfing_transactions(accounts)
    )

    transactions = (
        normal_transactions
        + starburst_transactions
        + circular_transactions
        + smurfing_transactions
    )

    random.shuffle(transactions)

    save_transactions(transactions)

    print_summary(transactions)

    print()
    print(
        f"Dataset saved to: {OUTPUT_FILE}"
    )

if __name__ == "__main__":
    main()