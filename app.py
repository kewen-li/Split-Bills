from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import locale

# Initialize the Flask app and SQLAlchemy
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bills.db'  # SQLite database file
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'your_secret_key'

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Set locale for USD currency formatting
locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

# Define the User (Splitter) model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)

# Define the Bills (BillSet) model
class Bills(db.Model):
    __tablename__ = 'bills'  # Renaming table to 'bills'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    transactions = db.relationship('Transactions', backref='set', lazy=True)

# Define the Transactions model
class Transactions(db.Model):
    __tablename__ = 'transactions'  # Renaming table to 'transactions'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    bill_set_id = db.Column(db.Integer, db.ForeignKey('bills.id'))
    splitters = db.relationship('User', secondary='transaction_splitter', backref='transactions')

# Association table between Transactions and Splitters (Users)
class TransactionSplitter(db.Model):
    __tablename__ = 'transaction_splitter'
    transaction_id = db.Column(db.Integer, db.ForeignKey('transactions.id'), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)

# Initialize the database and create all tables
with app.app_context():
    db.create_all()

# Routes

# Home page - bill entry form
@app.route('/')
def index():
    bill_sets = Bills.query.all()  # Get all Bills (formerly BillSets)
    users = User.query.all()  # Get all users (splitters)
    return render_template('index.html', bill_sets=bill_sets, users=users)

# Route to create a new bill (POST request from the form in index.html)
@app.route('/create_bill', methods=['POST'])
def create_bill():
    bill_name = request.form.get('bill_name')

    # Create a new bill entry
    new_bill = Bills(name=bill_name)
    db.session.add(new_bill)
    db.session.commit()

    # Redirect to the View Bills page
    return redirect(url_for('viewbills'))

# Route to create a new transaction (POST request from the form in index.html)
@app.route('/add_transaction', methods=['POST'])
def add_transaction():
    transaction_name = request.form.get('transaction_name')
    transaction_amount = float(request.form.get('transaction_amount'))
    bill_set_id = request.form.get('bill_set')
    splitters = request.form.getlist('splitters')

    # Create a new transaction
    new_transaction = Transactions(name=transaction_name, amount=transaction_amount, bill_set_id=bill_set_id)
    db.session.add(new_transaction)
    db.session.commit()

    # Add splitters (users) to the transaction
    for splitter_id in splitters:
        user = User.query.get(splitter_id)
        new_transaction.splitters.append(user)

    db.session.commit()

    # Redirect to the View Bills page after adding the transaction
    return redirect(url_for('viewbills'))

# View Bills page with operations (view, edit, delete)
@app.route('/viewbills', methods=['GET', 'POST'])
def viewbills():
    bill_sets = Bills.query.all()  # Get all bills
    return render_template('viewbills.html', bill_sets=bill_sets)

# View Transactions page for a specific bill
@app.route('/view_transactions/<int:bill_id>', methods=['GET'])
def view_transactions(bill_id):
    bill = Bills.query.get_or_404(bill_id)
    transactions = Transactions.query.filter_by(bill_set_id=bill_id).all()
    return render_template('view_transactions.html', bill=bill, transactions=transactions)

# Delete a Bill
@app.route('/delete_bill/<int:id>', methods=['GET'])
def delete_bill(id):
    bill = Bills.query.get(id)
    db.session.delete(bill)
    db.session.commit()
    return redirect(url_for('viewbills'))

# Edit Bill (Rename)
@app.route('/edit_bill/<int:id>', methods=['GET', 'POST'])
def edit_bill(id):
    bill = Bills.query.get(id)
    if request.method == 'POST':
        bill.name = request.form['name']
        db.session.commit()
        return redirect(url_for('viewbills'))
    return render_template('edit_bill.html', bill=bill)

# Delete a transaction
@app.route('/delete_transaction/<int:id>', methods=['GET'])
def delete_transaction(id):
    transaction = Transactions.query.get(id)
    db.session.delete(transaction)
    db.session.commit()
    return redirect(url_for('view_transactions', bill_id=transaction.bill_set_id))

# View, Edit, and Delete Splitters
@app.route('/splitters', methods=['GET', 'POST'])
def splitters():
    if request.method == 'POST':
        name = request.form.get('name')
        new_user = User(name=name)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('splitters'))
    users = User.query.all()
    return render_template('splitters.html', users=users)

# Delete splitter
@app.route('/delete_splitter/<int:id>', methods=['GET'])
def delete_splitter(id):
    user = User.query.get(id)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('splitters'))

if __name__ == '__main__':
    app.run(debug=True)
