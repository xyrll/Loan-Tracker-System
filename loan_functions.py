import os

BASE_DIR = os.path.dirname(__file__)
loantracker = os.path.join(BASE_DIR, "loans.txt")

# separator
def print_line():
    print("  " + "=" * 91)

# clear screen
def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def is_valid_decimal(text):
    text = text.strip()
    if text == "":
        return False
    if text.count(".") > 1:
        return False
    if text == ".":
        return False

    if "." in text:
        left, right = text.split(".")
        # allow ".5" and "5."
        if left != "" and not left.isdigit():
            return False
        if right != "" and not right.isdigit():
            return False
        return (left != "" and left.isdigit()) or (right != "" and right.isdigit())

    return text.isdigit()

def is_valid_int(text):
    text = text.strip()
    return text.isdigit()

def load_loans():
    loans = []

    if not os.path.exists(loantracker):
        return loans

    file = open(loantracker, "r")
    lines = file.read().split("\n")
    file.close()

    for line in lines:
        line = line.strip()
        if line == "":
            continue

        fields = line.split(",")

        if len(fields) == 6:
            loan_id       = fields[0].strip()
            borrower      = fields[1].strip()
            loan_amount   = float(fields[2].strip())
            interest_rate = float(fields[3].strip())
            months        = int(fields[4].strip())
            amount_paid   = float(fields[5].strip())

            record = [loan_id, borrower, loan_amount, interest_rate, months, amount_paid]
            loans.append(record)

    return loans

def save_loans(loans):
    file = open(loantracker, "w")

    for record in loans:
        line = f"{record[0]},{record[1]},{record[2]},{record[3]},{record[4]},{record[5]}\n"
        file.write(line)

    file.close()

def generate_id(loans):
    if len(loans) == 0:
        return "L001"

    last_id = loans[len(loans) - 1][0]
    number  = int(last_id.replace("L", "")) + 1

    if number < 10:
        return "L00" + str(number)
    elif number < 100:
        return "L0" + str(number)
    else:
        return "L" + str(number)

def compute_balance(record):
    loan_amount   = record[2]
    interest_rate = record[3]
    months        = record[4]
    amount_paid   = record[5]

    if months <= 0:
        months = 1

    interest = loan_amount * (interest_rate / 100) * months
    total_payable = loan_amount + interest
    payable_per_month = total_payable / months
    remaining = total_payable - amount_paid

    if remaining < 0:
        remaining = 0.0

    return total_payable, payable_per_month, remaining

def display_loan_details(record, detail_level="full"):
    loan_id, borrower, loan_amount, interest_rate, months, amount_paid = record

    if detail_level == "minimal":
        print(f"  Loan ID:   {loan_id}")
        print(f"  Borrower:  {borrower}")
        print(f"  Amount:    PHP {loan_amount:,.2f}")
        print(f"  Rate:      {interest_rate}%")
        print(f"  Duration:  {months} months")
        return

    total_payable, payable_per_month, remaining = compute_balance(record)

    if detail_level == "summary":
        print(f"  Borrower          : {borrower}")
        print(f"  Loan Amount       : PHP {loan_amount:,.2f}")
        print(f"  Total Payable     : PHP {total_payable:,.2f}")
        print(f"  Payable Per Month : PHP {payable_per_month:,.2f}")
        print(f"  Amount Paid       : PHP {amount_paid:,.2f}")
        print(f"  Remaining Balance : PHP {remaining:,.2f}")
        return

    if detail_level == "full":
        print(f"  Loan ID           : {loan_id}")
        print(f"  Borrower          : {borrower}")
        print(f"  Loan Amount       : PHP {loan_amount:,.2f}")
        print(f"  Interest Rate     : {interest_rate}%")
        print(f"  Duration          : {months} months")
        print(f"  Amount Paid       : PHP {amount_paid:,.2f}")
        print(f"  Total Payable     : PHP {total_payable:,.2f}")
        print(f"  Payable Per Month : PHP {payable_per_month:,.2f}")
        print(f"  Remaining Balance : PHP {remaining:,.2f}")
        return

    print_line()

def display_loans_table(loans):
    if len(loans) == 0:
        print("No loan records found.".center(90))
        return

    print(
        f"  {'ID':<8} "
        f"{'Borrower':<18} "
        f"{'Amount':>12} "
        f"{'Rate':>6} "
        f"{'Mo':>4} "
        f"{'Monthly':>12} "
        f"{'Paid':>12} "
        f"{'Balance':>12}"
    )
    print_line()

    for record in loans:
        total_payable, payable_per_month, remaining = compute_balance(record)
        status = "PAID" if remaining == 0 else f"{remaining:,.2f}"

        print(
            f"  {record[0]:<8} "
            f"{record[1]:<18} "
            f"{record[2]:>12,.2f} "
            f"{record[3]:>5.1f}% "
            f"{record[4]:>4} "
            f"{payable_per_month:>12,.2f} "
            f"{record[5]:>12,.2f} "
            f"{status:>12}"
        )

def add_loan(loans):
    while True:
        clear_screen()
        print_line()
        print("ADD NEW LOAN".center(90))
        print_line()

        borrower = input("  Borrower Name            : ").strip()
        if borrower == "":
            print_line()
            print("Name cannot be empty.".center(90))
            print_line()
            input("  Press Enter to continue...")
            continue

        loan_amount_input = input("  Loan Amount (PHP)        : ").strip()
        if not is_valid_decimal(loan_amount_input):
            print_line()
            print("Invalid loan amount.".center(90))
            print_line()
            input("  Press Enter to continue...")
            continue
        loan_amount = float(loan_amount_input)
        if loan_amount <= 0:
            print_line()
            print("Amount must be greater than zero.".center(90))
            print_line()
            input("  Press Enter to continue...")
            continue

        interest_input = input("  Interest Rate (%)        : ").strip()
        if not is_valid_decimal(interest_input):
            print_line()
            print("Invalid interest rate.".center(90))
            print_line()
            input("  Press Enter to continue...")
            continue
        interest_rate = float(interest_input)
        if interest_rate < 0:
            print_line()
            print("Interest rate cannot be negative.".center(90))
            print_line()
            input("  Press Enter to continue...")
            continue

        months_input = input("  Loan Duration (mo)       : ").strip()
        if not is_valid_int(months_input):
            print_line()
            print("Invalid loan duration.".center(90))
            print_line()
            input("  Press Enter to continue...")
            continue
        months = int(months_input)
        if months <= 0:
            print_line()
            print("Duration must be greater than zero.".center(90))
            print_line()
            input("  Press Enter to continue...")
            continue

        break

    clear_screen()
    print_line()
    print("ADD NEW LOAN".center(90))
    print_line()

    loan_id = generate_id(loans)
    record  = [loan_id, borrower, loan_amount, interest_rate, months, 0.0]

    total_payable, payable_per_month, remaining = compute_balance(record)

    print(f"  Loan ID           : {loan_id}")
    print(f"  Borrower          : {borrower}")
    print(f"  Loan Amount       : PHP {loan_amount:,.2f}")
    print(f"  Interest Rate     : {interest_rate}%")
    print(f"  Loan Duration     : {months} month/s")
    print(f"  Total Payable     : PHP {total_payable:,.2f}")
    print(f"  Payable Per Month : PHP {payable_per_month:,.2f}")
    print_line()

    confirm = input("  Confirm? (y/n)    : ").strip().lower()

    if confirm == "y":
        loans.append(record)
        save_loans(loans)
        print_line()
        print("Loan saved".center(90))
    else:
        print("Loan not saved.".center(90))

    print_line()
    input("  Press Enter to continue...")

def view_loans(loans):
    clear_screen()
    print_line()
    print("ALL LOAN RECORDS".center(91))
    print_line()

    if len(loans) == 0:
        print("No loan records found.".center(90))
        print_line()
        input("  Press Enter to continue...")
        return

    display_loans_table(loans)

    total_loans      = len(loans)
    total_loaned     = 0.0
    total_monthly    = 0.0
    total_collected  = 0.0
    total_remaining  = 0.0
    fully_paid_count = 0

    for record in loans:
        total_payable, payable_per_month, remaining = compute_balance(record)
        total_loaned    += record[2]
        total_monthly   += payable_per_month
        total_collected += record[5]
        total_remaining += remaining
        if remaining == 0:
            fully_paid_count += 1

    print_line()
    print(f"  Total Loan Records  : {total_loans}")
    print(f"  Fully Paid          : {fully_paid_count}")
    print(f"  Outstanding Loans   : {total_loans - fully_paid_count}")
    print_line()
    print(f"  Total Amount Loaned : PHP {total_loaned:,.2f}")
    print(f"  Total Monthly       : PHP {total_monthly:,.2f}")
    print(f"  Total Collected     : PHP {total_collected:,.2f}")
    print(f"  Total Remaining     : PHP {total_remaining:,.2f}")
    print_line()

    input("  Press Enter to continue...")
    print_line()

def edit_loan(loans):
    clear_screen()
    print_line()
    print("EDIT LOAN".center(91))
    print_line()

    if not loans:
        print("  No loans to edit.")
        input("  Press Enter to continue...")
        return

    print("  [1] Modify Loan")
    print("  [2] Record Payment")
    print_line()

    choice = input("  Select option: ").strip()
    
    if choice == "1":
        modify_loan(loans)
    elif choice == "2":
        pay_loans(loans)
    else:
        print("Invalid option.".center(91))
        input("  Press Enter to continue...")

def modify_loan(loans):
    clear_screen()
    print_line()
    print("MODIFY LOAN".center(90))
    print_line()
    
    display_loans_table(loans)
    print_line()
    
    loan_id = input("  Enter Loan ID to modify: ").strip().upper()
    found_index = -1
    
    for i in range(len(loans)):
        if loans[i][0] == loan_id:
            found_index = i
            break
    
    if found_index == -1:
        print(f"Loan ID '{loan_id}' not found.".center(91))
        input("  Press Enter to continue...")
        return
    
    record = loans[found_index]
    
    print_line()
    display_loan_details(record, detail_level="full")
    print_line()
    
    print("  [1] Edit Borrower Name")
    print("  [2] Edit Interest Rate")
    print("  [3] Edit Loan Amount")
    print("  [4] Edit Duration")
    print_line()
    
    choice = input("  Select option: ").strip()

    if choice == "1":
        edit_borrower_name(loans, found_index)
    elif choice == "2":
        edit_interest_rate(loans, found_index)
    elif choice == "3":
        edit_loan_amount(loans, found_index)
    elif choice == "4":
        edit_duration(loans, found_index)
    else:
        print("Invalid option.".center(91))
        input("  Press Enter to continue...")

def edit_borrower_name(loans, found_index):
    print_line()
    
    new_name = input("  New Borrower Name: ").strip()
    
    if not new_name:
        print("Name cannot be empty.".center(91))
        print_line()
        input("  Press Enter to continue...")
        return
    
    old_name = loans[found_index][1]
    loans[found_index][1] = new_name
    save_loans(loans)

    print_line()
    print(f"  Borrower name updated from '{old_name}' to '{new_name}'.")
    print_line()
    input("  Press Enter to continue...")

def edit_interest_rate(loans, found_index):
    print_line()
    
    rate_input = input("  New Interest Rate (%): ").strip()
    print_line()

    if not is_valid_decimal(rate_input):
        print("Invalid interest rate.".center(91))
        print_line()
        input("  Press Enter to continue...")
        return

    new_rate = float(rate_input)

    if new_rate < 0:
        print("Interest rate cannot be negative.".center(91))
        print_line()
        input("  Press Enter to continue...")
        return

    old_rate = loans[found_index][3]
    loans[found_index][3] = new_rate
    save_loans(loans)

    print(f"  Interest rate updated from {old_rate}% to {new_rate}%.")
    print_line()
    input("  Press Enter to continue...")

def edit_loan_amount(loans, found_index):
    print_line()
    
    amount_input = input("  New Loan Amount (PHP): ").strip()
    
    if not is_valid_decimal(amount_input):
        print("Invalid loan amount.".center(91))
        input("  Press Enter to continue...")
        return

    new_amount = float(amount_input)
    
    if new_amount <= 0:
        print("Loan amount must be greater than zero.".center(91))
        print_line()
        input("  Press Enter to continue...")
        return
    
    old_amount = loans[found_index][2]
    loans[found_index][2] = new_amount
    save_loans(loans)
    
    print(f"  Loan amount updated from PHP {old_amount:,.2f} to PHP {new_amount:,.2f}.")
    print_line()
    input("  Press Enter to continue...")

def edit_duration(loans, found_index):
    print_line()
    
    duration_input = input("  New Duration (months): ").strip()
    
    if not is_valid_int(duration_input):
        print("Invalid duration.".center(91))
        print_line()
        input("  Press Enter to continue...")
        return
    
    new_duration = int(duration_input)
    
    if new_duration <= 0:
        print("Duration must be greater than zero.".center(91))
        print_line()
        input("  Press Enter to continue...")
        return
    
    old_duration = loans[found_index][4]
    loans[found_index][4] = new_duration
    save_loans(loans)

    print_line()
    print(f"  Duration updated from {old_duration} months to {new_duration} months.")
    print_line()
    input("  Press Enter to continue...")

def get_loan_by_id(loans):
    while True:
        clear_screen()
        print_line()
        print("RECORD PAYMENT".center(90))
        print_line()
        
        display_loans_table(loans)
        print_line()
        
        loan_id_input = input("  Enter Loan ID      : ").strip().upper()
        
        for i in range(len(loans)):
            if loans[i][0] == loan_id_input:
                return i
        
        print_line()
        print(f"Loan ID '{loan_id_input}' not found.".center(91))
        print_line()
        input("  Press Enter to continue...")

def show_record_payment_header():
    clear_screen()
    print_line()
    print("RECORD PAYMENT".center(91))
    print_line()

def validate_payment_input(payment_input, remaining):
    if not is_valid_decimal(payment_input):
        return None

    payment = float(payment_input)

    if payment <= 0:
        return None

    if payment > remaining:
        return None

    return payment


def get_valid_payment(remaining):
    while True:
        show_record_payment_header()
        print(f"  Remaining Balance : PHP {remaining:,.2f}")
        print_line()

        payment_input = input("  Payment Amount    : PHP ").strip()
        payment = validate_payment_input(payment_input, remaining)

        if payment is not None:
            return payment

        print_line()
        if not is_valid_decimal(payment_input):
            print("Invalid payment amount.".center(90))
        else:
            payment_value = float(payment_input)
            if payment_value <= 0:
                print("Payment must be greater than zero.".center(90))
            else:
                print(f"Payment exceeds remaining balance of PHP {remaining:,.2f}.".center(90))
        print_line()
        input("  Press Enter to continue...")

def pay_loans(loans):
    
    found_index = get_loan_by_id(loans)
    record = loans[found_index]
    total_payable, payable_per_month, remaining = compute_balance(record)
    
    show_record_payment_header()
    display_loan_details(record, detail_level="summary")
    
    if remaining == 0:
        print("This loan is FULLY PAID.".center(91))
        print_line()
        input("  Press Enter to go back...")
        return
    
    payment = get_valid_payment(remaining)
    
    loans[found_index][5] = record[5] + payment
    save_loans(loans)
    
    updated_total, updated_payable_per_month, updated_remaining = compute_balance(loans[found_index])
    
    show_record_payment_header()
    print(f"  Payment of PHP {payment:,.2f} recorded.")
    print(f"  New Remaining Balance: PHP {updated_remaining:,.2f}")
    print_line()
    
    if updated_remaining == 0:
        print("LOAN FULLY PAID".center(91))
        print_line()
    
    input("  Press Enter to continue...")

def delete_loans(loans):
    clear_screen()
    print_line()
    print("DELETE LOANS".center(90))
    print_line()

    if not loans:
        print("No loans to delete.".center(90))
        print_line()
        input("  Press Enter to continue...")
        return

    print("  [1] Delete a loan")
    print("  [2] Delete all loans")
    print_line()

    choice = input("  choice: ").strip()

    if choice == "1":
        delete_loan(loans)
    elif choice == "2":
        delete_all_loans(loans)
    else:
        print_line()
        print("  Invalid option.")
        print_line()
        input("  Press Enter to continue...")

def delete_loan(loans):
    clear_screen()
    print_line()
    print("DELETE SINGLE LOAN".center(91))
    print_line()
    
    display_loans_table(loans)
    print_line()

    loan_id = input("  Enter Loan ID to delete: ").strip().upper()
    found_index = -1
    
    for i in range(len(loans)):
        if loans[i][0] == loan_id:
            found_index = i
            break
    
    if found_index == -1:
        print_line()
        print(f"Loan ID '{loan_id}' not found.".center(91))
        print_line()
        input("  Press Enter to continue...")
        return
    
    record = loans[found_index]
    print_line()
    display_loan_details(record, detail_level="minimal")
    print_line()
    
    confirm = input("  Delete this record? (y/n): ").strip().lower()
    print_line()
    if confirm == "y":
        loans.pop(found_index)
        
        save_loans(loans)
        print("Loan record deleted successfully.".center(91))
    else:
        print("Deletion cancelled.".center(91))
    print_line()
    input("  Press Enter to continue...")

def delete_all_loans(loans):
    clear_screen()
    print_line()
    print("DELETE ALL LOANS".center(91))
    print_line()
    
    display_loans_table(loans)
    print_line()
    
    confirm = input("  Delete ALL loan records? (y/n): ").strip().lower()
    
    if confirm == "y":
        print_line()
        loans.clear()
        save_loans(loans)
        print("All loan records deleted successfully.".center(91))
    else:
        print_line()
        print("Deletion cancelled.".center(91))

    print_line()
    input("  Press Enter to continue...")