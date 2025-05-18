class BankAccount:

    def __init__(self, account_holder, account_number, balance):
        self.account_holder = account_holder
        self.account_number = account_number
        self.balance        = balance

    def deposit(self, amount):
        self.balance += amount

    def withdraw(self, amount):
        if self.balance >= amount:
            self.balance -= amount
        else:
            print(f"Not enough balance!")

    def display_balance(self):
        print(f"Current balance = {self.balance}")

account = BankAccount("Sudev", 69, 69000)
account.display_balance()
account.deposit(400)
account.display_balance()
account.withdraw(200)
account.display_balance()