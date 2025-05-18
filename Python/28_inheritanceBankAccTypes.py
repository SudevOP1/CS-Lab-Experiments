class BankAccount:
    def __init__(self, account_holder, balance):
        self.account_holder = account_holder
        self.balance = balance
    def display_info(self):
        print(f"Account Holder: {self.account_holder}")
        print(f"Balance       : {self.balance}")

class SavingsAccount(BankAccount):
    def __init__(self, account_holder, balance, interest_rate):
        super().__init__(account_holder, balance)
        self.interest_rate = interest_rate
    def calc_interest(self):
        interest = self.balance * self.interest_rate / 100
        print(f"Interest = {interest}")


class CurrentAccount(BankAccount):
    def __init__(self, account_holder, balance, overdraft_limit):
        super().__init__(account_holder, balance)
        self.overdraft_limit = overdraft_limit
    def show_overdraft_limit(self):
        print(f"Overdraft limit = {self.overdraft_limit}")
