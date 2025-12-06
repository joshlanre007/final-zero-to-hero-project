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