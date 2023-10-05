class Transaction:
    def __init__(self, amount, transaction_type):
        self.amount = amount
        self.transaction_type = transaction_type


class TransactionHistory:
    def __init__(self):
        self.history = []

    def add_transaction(self, transaction):
        self.history.append(transaction)

    def display_history(self):
        for transaction in self.history:
            print(f"{transaction.transaction_type}: ${transaction.amount}")


class User:
    def __init__(self, user_id, pin, balance=0):
        self.user_id = user_id
        self.pin = pin
        self.balance = balance
        self.transaction_history = TransactionHistory()

    def deposit(self, amount):
        self.balance += amount
        transaction = Transaction(amount, "Deposit")
        self.transaction_history.add_transaction(transaction)

    def withdraw(self, amount):
        if amount <= self.balance:
            self.balance -= amount
            transaction = Transaction(amount, "Withdrawal")
            self.transaction_history.add_transaction(transaction)
        else:
            print("Insufficient funds!")

    def transfer(self, amount, recipient):
        if amount <= self.balance:
            self.balance -= amount
            recipient.balance += amount
            transaction = Transaction(amount, "Transfer to " + recipient.user_id)
            self.transaction_history.add_transaction(transaction)
        else:
            print("Insufficient funds!")

    def get_balance(self):
        return self.balance


class ATM:
    def __init__(self):
        self.users = {}  # User ID to User object mapping
        self.current_user = None

    def add_user(self, user):
        self.users[user.user_id] = user

    def authenticate_user(self, user_id, pin):
        user = self.users.get(user_id)
        if user and user.pin == pin:
            return user
        return None


class Menu:
    def __init__(self, atm):
        self.atm = atm

    def display_menu(self):
        print("\n1. Transaction History")
        print("2. Deposit")
        print("3. Withdraw")
        print("4. Transfer")
        print("5. Quit")

    def process_choice(self, choice):
        if choice == '1':
            self.atm.current_user.transaction_history.display_history()
        elif choice == '2':
            amount = float(input("Enter the deposit amount: "))
            self.atm.current_user.deposit(amount)
            print(f"Deposit successful. Current balance: ${self.atm.current_user.get_balance()}")
        elif choice == '3':
            amount = float(input("Enter the withdrawal amount: "))
            self.atm.current_user.withdraw(amount)
            print(f"Withdrawal successful. Current balance: ${self.atm.current_user.get_balance()}")
        elif choice == '4':
            recipient_id = input("Enter recipient's User ID: ")
            recipient = self.atm.users.get(recipient_id)
            if recipient:
                amount = float(input("Enter the transfer amount: "))
                self.atm.current_user.transfer(amount, recipient)
                print(f"Transfer successful. Current balance: ${self.atm.current_user.get_balance()}")
            else:
                print("Recipient not found.")
        elif choice == '5':
            print("Exiting...")
            exit()
        else:
            print("Invalid choice. Please enter a valid option.")


def main():
    atm = ATM()

    # Creating sample users
    user1 = User("709011", "402977", 1000)
    user2 = User("983412", "341260", 500)
    user3 = User("641039","459002",5000)
    
    atm.add_user(user1)
    atm.add_user(user2)
    atm.add_user(user3)

    # User authentication
    user_id = input("Enter User ID: ")
    pin = input("Enter PIN: ")

    authenticated_user = atm.authenticate_user(user_id, pin)

    if authenticated_user:
        atm.current_user = authenticated_user
        menu = Menu(atm)

        while True:
            menu.display_menu()
            choice = input("Enter your choice: ")
            menu.process_choice(choice)

    else:
        print("Authentication failed. Invalid User ID or PIN.")


if __name__ == "__main__":
    main()
