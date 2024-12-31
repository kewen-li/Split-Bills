# Bill Splitter
#### Video Demo:  https://youtu.be/0z9DN6cQ_TA
#### Description: My project aims to record the transaction that was shared by users and have basic management of each one

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