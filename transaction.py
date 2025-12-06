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

            
    



     
      