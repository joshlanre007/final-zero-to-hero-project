from transaction import Transaction
from budget import Budget
# Define the UserAccount class
class UserAccount:
     """
     represents a user account managing multiple transactions and budgets.
        Attributes:
            username (str): Username of the account holder.
            transactions (list): List of Transaction objects.
            budgets (dict): Dictionary of Budget objects keyed by category.
        """
     def __init__(self, username):
            self.username = username
            self.transactions = []
            self.budgets = {}
          #transaction methods
     def add_transaction(self, transaction):
            if not isinstance(transaction, Transaction):
               raise TypeError("Expected a Transaction object.")
            self.transactions.append(transaction)
     def delete_transaction(self, transaction):
            if transaction in self.transactions:
               self.transactions.remove(transaction)
            else:
               raise ValueError("Transaction not found.")
            #budget methods
     def set_budget(self, budget):
            if not isinstance(budget, Budget):
               raise TypeError("Expected a Budget object.")
            self.budgets[budget.category] = budget
     def generate_report(self):
            report = {}
            for transaction in self.transactions:
                category = transaction.category
                report.setdefault(category, 0)
                report[category] += transaction.amount
            return report
