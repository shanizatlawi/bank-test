import unittest
import datetime

# Sample bank_accounts setup for testing
bank_accounts = {
    1001: {
        "first_name": "Alice",
        "last_name": "Smith",
        "id_number": "123456789",
        "balance": 2500.50,
        "transactions_to_execute": [
            ("2024-08-17 14:00:00", 1001, 1002, 300),
            ("2024-08-17 15:00:00", 1001, 1003, 200)
        ],
        "transaction_history": []
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

# Function definitions (trx_perform, trx_create, name_by_get)
def trx_perform(bank_accounts, account_no: int):
    account = bank_accounts.get(account_no)
    transactions = account["transactions_to_execute"]

    for trx in transactions:
        _, from_account, to_account, amount = trx

        if account["balance"] >= amount:
            account["balance"] -= amount
            bank_accounts[to_account]["balance"] += amount

            executed_time = str(datetime.datetime.now())
            account["transaction_history"].append(trx + (executed_time,))
        else:
            print(f"Insufficient balance in account {from_account}.")

    account["transactions_to_execute"].clear()


def trx_create(bank_accounts, source_account_no: int, destination_account_no: int, amount: float):
    transaction = (str(datetime.datetime.now()), source_account_no, destination_account_no, amount)
    bank_accounts[source_account_no]["transactions_to_execute"].append(transaction)


def name_by_get(bank_accounts, first_name: str):
    return [acc_no for acc_no, details in bank_accounts.items() if first_name.lower() in details["first_name"].lower()]


class TestBankingSystem(unittest.TestCase):

    def setUp(self):
        # Reset the bank_accounts for each test
        self.bank_accounts = {
            1001: {
                "first_name": "Alice",
                "last_name": "Smith",
                "id_number": "123456789",
                "balance": 2500.50,
                "transactions_to_execute": [
                    ("2024-08-17 14:00:00", 1001, 1002, 300),
                    ("2024-08-17 15:00:00", 1001, 1003, 200)
                ],
                "transaction_history": []
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

    # Test trx_perform: transactions are cleared after execution
    def test_trx_perform_clears_transactions(self):
        trx_perform(self.bank_accounts, 1001)
        self.assertEqual(len(self.bank_accounts[1001]["transactions_to_execute"]), 0)

    # Test trx_perform: transactions are added to history
    def test_trx_perform_updates_history(self):
        trx_perform(self.bank_accounts, 1001)
        self.assertEqual(len(self.bank_accounts[1001]["transaction_history"]), 2)

    # Test trx_perform: balance is updated after execution
    def test_trx_perform_updates_balance(self):
        trx_perform(self.bank_accounts, 1001)
        self.assertEqual(self.bank_accounts[1001]["balance"], 2500.50 - 300 - 200)

    # Test trx_perform: destination account balance is updated
    def test_trx_perform_updates_destination_balance(self):
        trx_perform(self.bank_accounts, 1001)
        self.assertEqual(self.bank_accounts[1002]["balance"], 3900.75 + 300)
        self.assertEqual(self.bank_accounts[1003]["balance"], 3100.75 + 200)

    # Test trx_create: new transaction is added to the pending transactions list
    def test_trx_create_adds_transaction(self):
        trx_create(self.bank_accounts, 1001, 1002, 150)
        self.assertEqual(len(self.bank_accounts[1001]["transactions_to_execute"]), 3)

        # Check the details of the last transaction
        last_trx = self.bank_accounts[1001]["transactions_to_execute"][-1]
        self.assertEqual(last_trx[1], 1001)
        self.assertEqual(last_trx[2], 1002)
        self.assertEqual(last_trx[3], 150)

    # Test name_by_get: correct accounts are returned for partial name match
    def test_name_by_get_returns_correct_accounts(self):
        result = name_by_get(self.bank_accounts, "bo")
        self.assertIn(1002, result)
        self.assertIn(1003, result)
        self.assertNotIn(1001, result)


if __name__ == '__main__':
    unittest.main()
