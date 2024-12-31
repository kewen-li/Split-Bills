# Bill Splitter
## Video Demo:  https://youtu.be/0z9DN6cQ_TA
## Description: 
This project is a **Bill Splitting Web Application** designed to allow users to create bills, manage participants (splitters), and track transactions. The main purpose of the application is to simplify the process of splitting a shared expense among multiple individuals and calculating how much each person owes or is owed. It supports the creation of multiple bills, the addition of participants to each bill, and the assignment of transactions that define how much each participant has paid.

#### Features:
- **Bill Creation**: Users can create new bills with a unique name and amount. For each bill, users can specify the participants (splitters) who will share the cost. The amount can be evenly split among all participants, or it can be adjusted manually if needed.
  
- **User Management**: The application allows users to register as participants in the bill-splitting process. They can be selected as the **payer** (the person who pays upfront) and as **splitters** (the people sharing the cost). The payer is the primary person to whom others owe money.

- **Transaction Handling**: Each bill has associated **transactions** that record the amount paid and the splitters involved. When a transaction is created, users can select a **payer** and multiple **splitters** (other people involved in the transaction). The app will calculate and display how much each participant owes to the payer based on the transaction details.

- **User Interface**: The application uses a simple, responsive design that allows users to navigate through the different features easily. The layout uses **Bootstrap** to ensure that the pages are mobile-friendly and visually appealing. The user interface includes forms for entering transaction details and dynamically updates with user selections, such as toggling splitters using buttons.

- **Database**: The application utilizes **SQLAlchemy** to manage the data and interact with the SQLite database. The main entities in the database are **bills**, **users**, **transactions**, and **splitters**. Bills are created and associated with multiple transactions, and each transaction is linked to a payer and a list of splitters. The splitters are stored as a comma-separated list of user IDs, making it easier to retrieve the data and display the relevant information.

- **Frontend Logic**: JavaScript is used to handle the **dynamic interaction** between the user interface and the backend. For example, when selecting splitters, buttons toggle between selected and unselected states, and the form prevents submission if no splitters are selected. The selected splitters are passed to the backend via a hidden input field. Additionally, JavaScript is used to update the total amount owed by each participant and display it dynamically.

- **Error Handling**: The application includes basic validation to ensure that required fields are filled out (such as the payer and the amount). If no splitters are selected, an alert is shown, and the form submission is prevented. Proper error messages are displayed if any user-related issues arise (e.g., a user being not found).

### Technical Stack:
- **Backend**: Flask (Python web framework) is used to handle routing, form submission, and database interactions. SQLAlchemy is used for ORM (Object-Relational Mapping) to manage database models.
- **Frontend**: HTML5, CSS3 (Bootstrap), and JavaScript are used for the layout and dynamic interactions. Bootstrap is used for responsive design, ensuring that the app is usable on mobile devices.
- **Database**: SQLite with SQLAlchemy ORM is used for database management, where all the data related to bills, users, transactions, and splitters is stored.

### Conclusion:
This **Bill Splitting Web Application** provides an easy-to-use interface for managing shared expenses, making it perfect for roommates, friends, or any group of people who frequently share costs. With the ability to track who owes whom, split costs evenly or unevenly, and store historical records, this application ensures that managing bills and transactions is simple, transparent, and efficient. The app is extendable, allowing for the addition of more complex features, such as the ability to add different payment methods, handle currency exchange rates, or create reports for various time periods.

## TODO
1. Calculation on the bills
2. Display result who should pay whom how much
3. make a mobile version
4. add more user friednly functions or UI

# How to use

## First time
### 1. Create a virtual environment:
+ Window/MacOS/LInux
```bash
python3 -m venv billsplitenv
or
python -m venv billsplitenv
```
+ Anaconda
```bash
conda create -n billsplitenv python=3.11 anaconda
```

### 2. Install the packages:
```bash
pip install -r requirements.txt
```

### 3. Initialze the database if you use this for the first time
```bash
python init_db.py
```
## After Initialization
### Every Time! Activate the virtual environment:
- On Windows:
```bash
.\billsplitenv\Scripts\activate
```

- On macOS/Linux:
```bash
source billsplitenv/bin/activate
```

+ On Anaconda
```bash
source billsplitenv/bin/activate
```