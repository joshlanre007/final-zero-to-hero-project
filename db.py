"""SQLite database helpers for the Personal Finance Tracker.

Provides simple CRUD operations for transactions and budgets.
"""
import sqlite3
from sqlite3 import Connection
from typing import List, Dict, Optional
from transaction import Transaction
from budget import Budget
import csv
import os

DEFAULT_DB = os.path.join(os.path.dirname(__file__), "finance.db")


def get_connection(db_path: str = DEFAULT_DB) -> Connection:
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


def init_db(db_path: str = DEFAULT_DB) -> None:
    """Create tables if they don't exist."""
    conn = get_connection(db_path)
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            description TEXT
        )
        """
    )
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS budgets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT UNIQUE NOT NULL,
            limit_amount REAL NOT NULL
        )
        """
    )
    conn.commit()
    conn.close()


def add_transaction(tx: Transaction, db_path: str = DEFAULT_DB) -> int:
    conn = get_connection(db_path)
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO transactions (date, amount, category, description) VALUES (?, ?, ?, ?)",
        (tx.date.isoformat(), tx.amount, tx.category, tx.description),
    )
    conn.commit()
    tx_id = cur.lastrowid
    conn.close()
    return tx_id


def update_transaction(tx_id: int, tx: Transaction, db_path: str = DEFAULT_DB) -> None:
    conn = get_connection(db_path)
    cur = conn.cursor()
    cur.execute(
        "UPDATE transactions SET date = ?, amount = ?, category = ?, description = ? WHERE id = ?",
        (tx.date.isoformat(), tx.amount, tx.category, tx.description, tx_id),
    )
    conn.commit()
    conn.close()


def delete_transaction(tx_id: int, db_path: str = DEFAULT_DB) -> None:
    conn = get_connection(db_path)
    cur = conn.cursor()
    cur.execute("DELETE FROM transactions WHERE id = ?", (tx_id,))
    conn.commit()
    conn.close()


def get_all_transactions(db_path: str = DEFAULT_DB) -> List[Dict]:
    conn = get_connection(db_path)
    cur = conn.cursor()
    cur.execute("SELECT id, date, amount, category, description FROM transactions ORDER BY date DESC")
    rows = cur.fetchall()
    conn.close()
    return [dict(r) for r in rows]


def add_budget(budget: Budget, db_path: str = DEFAULT_DB) -> None:
    conn = get_connection(db_path)
    cur = conn.cursor()
    cur.execute(
        "INSERT OR REPLACE INTO budgets (category, limit_amount) VALUES (?, ?)",
        (budget.category, budget.limit),
    )
    conn.commit()
    conn.close()


def get_budgets(db_path: str = DEFAULT_DB) -> List[Dict]:
    conn = get_connection(db_path)
    cur = conn.cursor()
    cur.execute("SELECT id, category, limit_amount FROM budgets")
    rows = cur.fetchall()
    conn.close()
    # map sqlite row keys to match earlier Budget.to_dict naming
    out = []
    for r in rows:
        d = dict(r)
        d["limit"] = d.pop("limit_amount")
        out.append(d)
    return out


def summary_by_category(db_path: str = DEFAULT_DB) -> Dict[str, float]:
    conn = get_connection(db_path)
    cur = conn.cursor()
    cur.execute("SELECT category, SUM(amount) as total FROM transactions GROUP BY category")
    rows = cur.fetchall()
    conn.close()
    return {r["category"]: r["total"] for r in rows}


def export_transactions_csv(file_path: str, db_path: str = DEFAULT_DB) -> None:
    """Export all transactions to a CSV file. Raises exceptions on file write errors."""
    rows = get_all_transactions(db_path)
    with open(file_path, "w", newline='', encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["id", "date", "amount", "category", "description"])
        for r in rows:
            writer.writerow([r["id"], r["date"], r["amount"], r["category"], r["description"]])
