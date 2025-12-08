# Implement OOP p principles where possible : Define classes like Transaction (with attributes for date, amount, category, description), Budget (to set limits per category), and UserAccount (to manage multiple users
# and their transactions). Use methods within these classes to add transactions, set budgets, and generate reports.
from datetime import datetime, date


class Transaction:
  """Represents a single financial transaction.

  Attributes:
    date (datetime.date): Date of the transaction (stored as date object).
    amount (float): Amount spent (negative for expenses) or received (positive).
    category (str): Category (e.g., Food, Transport, Salary).
    description (str): Optional short note.
  """

  def __init__(self, date_value, amount, category, description=""):
    self.date = self._validate_date(date_value)
    self.amount = self._validate_amount(amount)
    self.category = str(category)
    self.description = str(description)

  def _validate_date(self, value):
    """Validate and return a date object. Accepts date/datetime or 'YYYY-MM-DD' string."""
    if isinstance(value, date):
      return value
    if isinstance(value, datetime):
      return value.date()
    if isinstance(value, str):
      try:
        return datetime.strptime(value, "%Y-%m-%d").date()
      except ValueError:
        raise ValueError("Date string must be in 'YYYY-MM-DD' format")
    raise ValueError("Date must be a date, datetime, or 'YYYY-MM-DD' string")

  def _validate_amount(self, amount):
    try:
      return float(amount)
    except (TypeError, ValueError):
      raise ValueError("Amount must be numeric")

  def to_dict(self) -> dict:
    return {
      "date": self.date.isoformat(),
      "amount": self.amount,
      "category": self.category,
      "description": self.description,
    }

  def __repr__(self):
    return (
      f"Transaction(date={self.date.isoformat()}, amount={self.amount}, "
      f"category={self.category!r}, description={self.description!r})"
    )

            
    



     
      