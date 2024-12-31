from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import desc

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bills.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# User model (splitters)
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)

# Bill model (bill set)
class Bills(db.Model):
    __tablename__ = 'bills'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    transactions = db.relationship('Transactions', backref='set', lazy=True)

# Transactions model
class Transactions(db.Model):
    __tablename__ = 'transactions'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    bill_set_id = db.Column(db.Integer, db.ForeignKey('bills.id'))
    payer_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # Payer
    splitters = db.relationship('User', secondary='transaction_splitter', backref='transactions')
    payer = db.relationship('User', foreign_keys=[payer_id])

# Association table between Transactions and Splitters (Users)
class TransactionSplitter(db.Model):
    __tablename__ = 'transaction_splitter'
    transaction_id = db.Column(db.Integer, db.ForeignKey('transactions.id'), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    # No need for amount_owed in the database since it will be calculated at runtime
    # amount_owed = db.Column(db.Float, nullable=False)

# Route for the index page (GET request to show the form)
@app.route('/')
def index():
    bill_sets = Bills.query.order_by(desc(Bills.created_at)).all()  # Get all Bill Sets (bills)
    users = User.query.all()  # Get all users (splitters)
    return render_template('index.html', bill_sets=bill_sets, users=users)

# Route to create a new transaction (POST request from the form in index.html)
@app.route('/add_transaction', methods=['POST'])
def add_transaction():
    transaction_name = request.form.get('transaction_name')
    transaction_amount = float(request.form.get('transaction_amount'))
    bill_set_id = request.form.get('bill_set')
    payer_id = request.form.get('payer')
    splitters = request.form.getlist('splitters')

    # Create a new transaction and add it to the session
    new_transaction = Transactions(
        name=transaction_name,
        amount=transaction_amount,
        bill_set_id=bill_set_id,
        payer_id=payer_id
    )
    db.session.add(new_transaction)
    db.session.commit()

    # Get the payer user object
    payer = User.query.get(payer_id)

    # Add payer as the default splitter
    new_transaction.splitters.append(payer)

    # Add the other splitters to the transaction
    for splitter_id in splitters:
        user = User.query.get(splitter_id)
        new_transaction.splitters.append(user)

    db.session.commit()

    return redirect(url_for('view_bills'))

# Route for viewing bills
@app.route('/view_bills', methods=['GET'])
def view_bills():
    bill_sets = Bills.query.all()
    return render_template('view_bills.html', bill_sets=bill_sets)

# Route to view transactions for a bill
@app.route('/view_transactions/<int:bill_id>', methods=['GET'])
def view_transactions(bill_id):
    bill = Bills.query.get_or_404(bill_id)
    transactions = Transactions.query.filter_by(bill_set_id=bill_id).all()
    return render_template('view_transactions.html', bill=bill, transactions=transactions)

# Route to delete a bill
@app.route('/delete_bill/<int:id>', methods=['GET'])
def delete_bill(id):
    bill = Bills.query.get(id)
    db.session.delete(bill)
    db.session.commit()
    return redirect(url_for('view_bills'))

# Route to delete a transaction
@app.route('/delete_transaction/<int:id>', methods=['GET'])
def delete_transaction(id):
    transaction = Transactions.query.get(id)
    db.session.delete(transaction)
    db.session.commit()
    return redirect(url_for('view_transactions', bill_id=transaction.bill_set_id))

# Route to view, edit, and delete splitters
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

# Route to create a new bill (POST request from the form in index.html)
@app.route('/create_bill', methods=['POST'])
def create_bill():
    bill_name = request.form.get('bill_name')

    # Create a new bill entry
    new_bill = Bills(name=bill_name)
    db.session.add(new_bill)
    db.session.commit()

    # Redirect to the View Bills page
    return redirect(url_for('view_bills'))

# Start the application
if __name__ == '__main__':
    app.run(debug=True)
