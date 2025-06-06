from flask import Flask, render_template, request, redirect, session, url_for, flash
from finance_logic import calculate_summary, add_transaction, get_all_transactions_user
from auth import register_user, verify_user
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Replace with a strong secret key in production

# Home page - requires login
@app.route('/')
def index():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    username = session['username']
    summary = calculate_summary(username)
    transactions = get_all_transactions_user(username)
    categories = ['Rent', 'Food', 'Savings', 'Entertainment', 'Other']  # For dropdown
    return render_template('index.html', summary=summary, transactions=transactions, categories=categories)

# Add transaction - POST only, requires login
@app.route('/add', methods=['POST'])
def add():
    if 'username' not in session:
        return redirect(url_for('login'))
    username = session['username']
    t_type = request.form['type']
    amount = float(request.form['amount'])
    description = request.form['description']
    add_transaction(username, t_type, amount, description)
    return redirect(url_for('index'))

# Register page
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if register_user(username, password):
            flash('Registration successful! Please login.')
            return redirect(url_for('login'))
        else:
            flash('Username already exists. Try a different one.')
    return render_template('register.html')

# Login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if verify_user(username, password):
            session['username'] = username
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password.')
    return render_template('login.html')

# Logout route
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    # Ensure the data folder exists
    if not os.path.exists('data'):
        os.mkdir('data')
    app.run(debug=True)
