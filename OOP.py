# Implement OOP p principles where possible : Define classes like Transaction (with attributes for date, amount, category, description), Budget (to set limits per category), and UserAccount (to manage multiple users
# and their transactions). Use methods within these classes to add transactions, set budgets, and generate reports.
from datetime import datetime

# Define the Transaction class
class Transaction:

     """
    Represents a single financial transaction.
    Attributes:
        date (datetime): Date of the transaction.
        amount (float): Amount spent or received.
        category (str): Category (e.g., Food, Transport, Salary).
        description (str): Optional short note.
   
     """
     def __init__(self, date, amount, category, description=""):
        self.date = self._validate_date(date)
        self.amount = self._validate_amount(amount) 
        self.category = category
        self.description = description

     def _validate_date(self, date): #ensure the date is a datetime object
            if isinstance(date, str):
                return datetime.strptime(date)
            elif isinstance(date, datetime):
                return date
            else:
                raise ValueError("Date must be a string in 'YYYY-MM-DD' format or a datetime object.")
            
     def _validate_amount(self, amount): #ensure the amount is a valid
             try:
               amount = float(amount)
               return amount
             except ValueError:
               raise ValueError("Amount must be numeric.")


        
     def __repr__(self):
            return f"Transactiondate: {self.date}, Amount: {self.amount}, Category: {self.category}, Description: {self.description}"
# Define the Budget class
class Budget :
     """
    Represents a budget for a specific category.
    Attributes:
        category (str): Category for the budget.
        limit (float): Spending limit for the category.
    """
     def __init__(self, category, limit):
        self.category = category
        self.limit_amount = float(limit)
    
     def variance(self, spent):  # Returns how much is left or exceedwd
        return self.limit - spent

     def __repr__(self):
         return f"Budget Category: {self.category}, Limit: {self.limit}"
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

            
    



     
      