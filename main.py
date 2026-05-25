from loan_functions import (
    print_line,
    clear_screen,
    load_loans,
    add_loan,
    view_loans,
    edit_loan,
    delete_loans
)

def main_menu():
    """
    Display the main menu and handle user navigation.
    """
    loans = load_loans()

    while True:
        clear_screen()
        print_line()
        print(f"{'Records on file: ' + str(len(loans)):^90}")
        print_line()
        print(f"{'LOAN TRACKER SYSTEM':^90}")
        print_line()
        print(f"{'[1] Add New Loan':^50}" + f"{'[2] Summary':^20}")
        print(f"{'[3] Edit Loan':^47}" + f"{'[4] Delete Loans':^31}")
        print(f"{'[5] Exit':^90}")
        print_line()

        choice = input("  Select option: ").strip()

        if choice == "1":
            add_loan(loans)
            loans = load_loans()
        elif choice == "2":
            view_loans(loans)
        elif choice == "3":
            edit_loan(loans)
            loans = load_loans()
        elif choice == "4":
            delete_loans(loans)
            loans = load_loans()
        elif choice == "5":
            clear_screen()
            print_line()
            print("Exiting...".center(91))
            print_line()
            break
        else:
            print_line()
            print("Invalid option. Please enter 1-5.".center(91))
            print_line()
            input("  Press Enter to try again...")

if __name__ == "__main__":
    main_menu()
