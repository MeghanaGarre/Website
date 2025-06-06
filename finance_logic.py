import json
import os

def get_user_data_file(username):
    return f'data/{username}.json'

def get_all_transactions_user(username):
    user_file = get_user_data_file(username)
    if not os.path.exists(user_file):
        with open(user_file, 'w') as f:
            json.dump([], f)
    with open(user_file, 'r') as f:
        return json.load(f)

def add_transaction(username, t_type, amount, description):
    transaction = {
        'type': t_type,
        'amount': amount,
        'description': description
    }
    transactions = get_all_transactions_user(username)
    transactions.append(transaction)
    with open(get_user_data_file(username), 'w') as f:
        json.dump(transactions, f, indent=4)

def calculate_summary(username):
    transactions = get_all_transactions_user(username)
    income = sum(t['amount'] for t in transactions if t['type'] == 'income')
    expenses = sum(t['amount'] for t in transactions if t['type'] == 'expense')
    balance = income - expenses
    return {
        'income': income,
        'expenses': expenses,
        'balance': balance
    }
