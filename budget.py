"""Budget model.

Represents a budget for a specific category.
"""

class Budget:
   """Represents a budget for a specific category.

   Attributes:
      category (str): Category for the budget.
      limit (float): Spending limit for the category.
   """

   def __init__(self, category: str, limit: float):
      self.category = str(category)
      # store limit as float and use attribute name `limit`
      self.limit = float(limit)

   def variance(self, spent: float) -> float:
      """Return remaining budget (positive if under budget, negative if exceeded)."""
      try:
         spent = float(spent)
      except (TypeError, ValueError):
         raise ValueError("Spent must be numeric")
      return self.limit - spent

   def to_dict(self) -> dict:
      return {"category": self.category, "limit": self.limit}

   def __repr__(self) -> str:
      return f"Budget(category={self.category!r}, limit={self.limit})"