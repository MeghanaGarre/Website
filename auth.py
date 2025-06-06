import json
import os
from werkzeug.security import generate_password_hash, check_password_hash

USERS_FILE = 'data/users.json'

# Load users from file
def load_users():
    if not os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'w') as f:
            json.dump([], f)
    with open(USERS_FILE, 'r') as f:
        return json.load(f)

# Save users to file
def save_users(users):
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f, indent=4)

# Register a new user
def register_user(username, password):
    users = load_users()
    # Check if username already exists
    if any(u['username'] == username for u in users):
        return False  # Username taken
    # Hash the password
    hashed_password = generate_password_hash(password)
    users.append({'username': username, 'password': hashed_password})
    save_users(users)
    # Create user's transaction file
    user_data_file = f'data/{username}.json'
    if not os.path.exists(user_data_file):
        with open(user_data_file, 'w') as f:
            json.dump([], f)
    return True

# Verify user login
def verify_user(username, password):
    users = load_users()
    for user in users:
        if user['username'] == username and check_password_hash(user['password'], password):
            return True
    return False
