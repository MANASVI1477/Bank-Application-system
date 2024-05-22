import sqlite3

# Function to create the database and the accounts table
def create_db():
    try:
        conn = sqlite3.connect('bank.db')
        c = conn.cursor()
        
        # Create accounts table if it doesn't exist
        c.execute('''CREATE TABLE IF NOT EXISTS accounts (
                     account_number INTEGER PRIMARY KEY AUTOINCREMENT,
                     name TEXT NOT NULL,
                     balance REAL NOT NULL DEFAULT 0.0)''')
        
        conn.commit()
        conn.close()
        print("Database and table created successfully.")
    except sqlite3.Error as e:
        print(f"Error creating database: {e}")

# Call create_db() to ensure the table is created before any operations
create_db()

class BankManagementSystem:
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()

    def create_account(self, name):
        try:
            self.cursor.execute("INSERT INTO accounts (name, balance) VALUES (?, ?)", (name, 0.0))
            self.conn.commit()
            print(f"Account created for {name}.")
            self.cursor.execute("SELECT account_number, name, balance FROM accounts WHERE name = ?", (name,))
            account = self.cursor.fetchone()
            print(f"Verified Account: {account}")
        except sqlite3.Error as e:
            print(f"Error creating account: {e}")

    def deposit(self, account_number, amount):
        try:
            self.cursor.execute("UPDATE accounts SET balance = balance + ? WHERE account_number = ?", (amount, account_number))
            self.conn.commit()
            print(f"Deposited ${amount} to account number {account_number}.")
        except sqlite3.Error as e:
            print(f"Error depositing money: {e}")

    def withdraw(self, account_number, amount):
        try:
            self.cursor.execute("SELECT balance FROM accounts WHERE account_number = ?", (account_number,))
            balance = self.cursor.fetchone()[0]
            if balance >= amount:
                self.cursor.execute("UPDATE accounts SET balance = balance - ? WHERE account_number = ?", (amount, account_number))
                self.conn.commit()
                print(f"Withdrew ${amount} from account number {account_number}.")
            else:
                print("Insufficient balance!")
        except sqlite3.Error as e:
            print(f"Error withdrawing money: {e}")

    def check_balance(self, account_number):
        try:
            self.cursor.execute("SELECT balance FROM accounts WHERE account_number = ?", (account_number,))
            balance = self.cursor.fetchone()[0]
            print(f"Account number {account_number} has a balance of ${balance}.")
        except sqlite3.Error as e:
            print(f"Error checking balance: {e}")

    def close(self):
        self.conn.close()

# Main program to interact with the system
def main():
    bms = BankManagementSystem('bank.db')
    
    while True:
        print("\nBank Management System")
        print("1. Create Account")
        print("2. Deposit")
        print("3. Withdraw")
        print("4. Check Balance")
        print("5. Exit")
        choice = int(input("Enter your choice: "))

        if choice == 1:
            name = input("Enter your name: ")
            bms.create_account(name)
        elif choice == 2:
            account_number = int(input("Enter account number: "))
            amount = float(input("Enter amount to deposit: "))
            bms.deposit(account_number, amount)
        elif choice == 3:
            account_number = int(input("Enter account number: "))
            amount = float(input("Enter amount to withdraw: "))
            bms.withdraw(account_number, amount)
        elif choice == 4:
            account_number = int(input("Enter account number: "))
            bms.check_balance(account_number)
        elif choice == 5:
            bms.close()
            print("Thank you for using the Bank Management System.")
            break
        else:
            print("Invalid choice, please try again.")

if __name__ == "__main__":
    main()



