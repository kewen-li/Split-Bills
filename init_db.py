# init_db.py
from app import app, db
from app import User, Bills, Transactions
from datetime import datetime,timezone

# Function to initialize the database
def init_db():
    with app.app_context():
        # Drop all existing tables
        db.drop_all()

        # Create new tables based on the updated models
        db.create_all()

        # Add initial users (splitters)
        if not User.query.first():  # Check if there's any user
            users = ['Alice', 'Bob', 'Charlie']
            for name in users:
                user = User(name=name)
                db.session.add(user)
            db.session.commit()
            print("Initial users created.")

        # Add an initial Bill (Transaction) and BillSet
        if not Bills.query.first():
            bills = Bills(name='Default Bill', created_at= datetime.now(timezone.utc))
            db.session.add(bills)
            db.session.commit()
            print("Initial Bills created.")

        print("Database and tables initialized successfully.")

if __name__ == '__main__':
    init_db()
