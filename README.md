# Personal Finance Tracker

This is a minimal Personal Finance Tracker desktop app implemented in Python with a PyQt5 GUI. It stores transactions and budgets in an SQLite database and can export transactions to CSV.

Getting started

1. Create a virtual environment (recommended) and install dependencies:

   python -m venv venv
   venv\Scripts\activate
   pip install -r requirements.txt

2. Run the app:

   python main.py

Files

- `transaction.py` — Transaction model with validation.
- `budget.py` — Budget model.
- `Useraccount.py` — Simple in-memory user account manager.
- `db.py` — SQLite helpers (init, CRUD, CSV export).
- `main.py` — Minimal PyQt5 GUI demo.

Notes

- The GUI is intentionally small and demonstrates adding/listing/deleting transactions and exporting CSV.
- Date format for input is `YYYY-MM-DD`.
- Amounts are numeric (use negative for expenses, positive for income).

Next steps (suggested)

- Improve GUI (editing transactions, budget UI, charts).
- Add tests and better error reporting.
- Add user management and authentication if desired.
