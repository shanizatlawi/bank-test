import datetime

# Dictionary containing bank account details
bank_accounts = {
    1001: {
        "first_name": "Alice",
        "last_name": "Smith",
        "id_number": "123456789",
        "balance": 2500.50,
        "transactions_to_execute": [
            ("2024-08-17 14:00:00", 1001, 1002, 300), ("2024-08-17 15:00:00", 1001, 1003, 200)],
        "transaction_history": [
            ("2024-08-15 09:00:00", 1001, 1002, 500, "2024-08-15 09:30:00")]
    },
    1002: {
        "first_name": "Bob",
        "last_name": "Johnson",
        "id_number": "987654321",
        "balance": 3900.75,
        "transactions_to_execute": [],
        "transaction_history": []
    },
    1003: {
        "first_name": "Bob2",
        "last_name": "Johnson2",
        "id_number": "987654320",
        "balance": 3100.75,
        "transactions_to_execute": [],
        "transaction_history": []
    }
}


# Create a new transaction
def create_trx(source_account_no: int, destination_account_no: int, amount: int) -> None:
    source_account = bank_accounts.get(source_account_no)
    trx_tuple = (str(datetime.datetime.now()), source_account_no, destination_account_no, amount)
    source_account["transactions_to_execute"].append(trx_tuple)


# Perform pending transactions
def perform_trx(account_no: int) -> None:
    source_account = bank_accounts.get(account_no)
    transactions_to_execute = source_account["transactions_to_execute"]

    for trx in transactions_to_execute:
        dest_account_no = trx[2]
        amount = trx[3]

        # Check if source account has enough balance
        if source_account["balance"] >= amount:
            bank_accounts[dest_account_no]["balance"] += amount
            source_account["balance"] -= amount

            # Add the transaction to history with the current execution time
            executed_time = str(datetime.datetime.now())
            source_account["transaction_history"].append(trx + (executed_time,))
            print(f"Transferred {amount} from account {account_no} to account {dest_account_no}.")
        else:
            print(f"Insufficient balance in account {account_no}.")

    # Clear the pending transactions list
    transactions_to_execute.clear()


# Add a new transaction through user input
def add_trx():
    while True:
        try:
            source_account_no = int(input("Enter source account number: "))
            if bank_accounts.get(source_account_no) is None:
                print(f"Account {source_account_no} does not exist in the system.")
                continue

            destination_account_no = int(input("Enter destination account number: "))
            if bank_accounts.get(destination_account_no) is None:
                print(f"Account {destination_account_no} does not exist in the system.")
                continue

            amount = int(input("Enter the amount to transfer: "))
            if amount <= 50:
                print('The amount must be at least 50.')
                continue

            # Create the transaction
            create_trx(source_account_no, destination_account_no, amount)
            print(
                f"Transaction successfully added from account {source_account_no} to account {destination_account_no}.")
            break

        except ValueError:
            print('Invalid input, please try again.')


# Execute all pending transactions
def execute_trx():
    account_no = int(input("Enter account number to execute transactions: "))
    if bank_accounts.get(account_no) is None:
        print(f"Account {account_no} does not exist in the system.")
        return

    perform_trx(account_no)


# Reports menu
def reports():
    print("Reports:")
    for account_no, details in bank_accounts.items():
        print(f"Account {account_no}: {details['first_name']} {details['last_name']} - Balance: {details['balance']}")


# Main menu
def show_main_menu():
    while True:
        print('1. Create transaction')
        print('2. Execute pending transactions')
        print('3. Reports')
        print('4. Exit')

        choice = input("What is your choice? ")
        if choice == "4":
            print("Goodbye!")
            break
        match choice:
            case "1":
                add_trx()
            case "2":
                execute_trx()
            case "3":
                reports()
            case _:
                print("Invalid choice, please try again.")


# Start the program
show_main_menu()
