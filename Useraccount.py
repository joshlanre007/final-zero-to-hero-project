"""User account model.

Manages a list of transactions and budgets for a single user.
"""

from transaction import Transaction
from budget import Budget
from collections import defaultdict
from typing import List, Dict


class UserAccount:
   """Represents a user account managing multiple transactions and budgets.

   Attributes:
      username (str): Username of the account holder.
      transactions (list[Transaction]): List of Transaction objects.
      budgets (dict[str, Budget]): Budgets keyed by category.
   """

   def __init__(self, username: str):
      self.username = str(username)
      self.transactions: List[Transaction] = []
      self.budgets: Dict[str, Budget] = {}

   # transaction methods
   def add_transaction(self, transaction: Transaction) -> None:
      if not isinstance(transaction, Transaction):
         raise TypeError("Expected a Transaction object.")
      self.transactions.append(transaction)

   def delete_transaction(self, transaction: Transaction) -> None:
      try:
         self.transactions.remove(transaction)
      except ValueError:
         raise ValueError("Transaction not found.")

   # budget methods
   def set_budget(self, budget: Budget) -> None:
      if not isinstance(budget, Budget):
         raise TypeError("Expected a Budget object.")
      self.budgets[budget.category] = budget

   def generate_report(self) -> dict:
      """Return total amounts grouped by category."""
      report = defaultdict(float)
      for transaction in self.transactions:
         report[transaction.category] += transaction.amount
      return dict(report)

   def total_spent(self) -> float:
      """Return total of all transaction amounts."""
      return sum(tx.amount for tx in self.transactions)

   def spending_by_category(self) -> dict:
      """Alias for generate_report (keeps naming clear)."""
      return self.generate_report()

