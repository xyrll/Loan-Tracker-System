# Loan Tracker

A simple **Python (CLI)** loan tracking program that lets you add, view, edit, and delete loan records. Records are saved locally to a text file.

## Features

### 1) Add New Loan
- Enter borrower name, loan amount, interest rate, and duration
- Automatically generates a unique **Loan ID**
- Shows computed **total payable** and **monthly payment**
- Calculates the **total payable amount**, the **monthly payment**, and the **remaining balance**
- Saves only after confirmation

### 2) View Loan Records
Displays all saved loans in a table format.

Shows:
- Loan ID
- Borrower
- Loan amount
- Interest rate
- Duration
- Monthly payment
- Amount paid
- Remaining balance

Summary includes:
- Total loan records
- Fully paid loans
- Outstanding loans
- Total amount loaned
- Total collected
- Total remaining

### 3) Edit Loan
Modify existing loan details:
- Borrower name
- Interest rate
- Loan amount
- Duration

Record payments and update remaining balance.

### 4) Delete Loan
- Delete a single loan
- Delete all loans
- Confirmation before deleting

## File Structure

```text
loantracker
├─ main.py
├─ loan_functions.py
└─ loans.txt
```

> `loans.txt` will be created/updated automatically when you save records.

## Requirements

- Python 3.x
- No external libraries required

## How to Run

1. Open a terminal or command prompt
2. Go to the project folder
3. Run:

```bash
python main.py
```

## Data Format (`loans.txt`)

Example:

```text
L001,Juan Dela Cruz,10000,2.5,12,3000
```

Each line represents one loan record:

```text
LoanID,Borrower,LoanAmount,InterestRate,Months,AmountPaid
```

## Computation Used

The program uses **simple interest**:

```text
interest = loan_amount * (interest_rate / 100) * months
total_payable = loan_amount + interest
payable_per_month = total_payable / months
remaining_balance = total_payable - amount_paid
```

If the remaining balance becomes negative (overpaid), the program sets it to `0.0`.

## Validation Rules

- Borrower name cannot be empty
- Loan amount must be greater than zero
- Interest rate cannot be negative
- Duration must be greater than zero

Payment amount:
- must be valid
- must be greater than zero
- must not exceed balance
