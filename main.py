"""Minimal PyQt5 GUI for the Personal Finance Tracker.

Features:
- Add transaction (date, amount, category, description)
- List transactions
- Delete selected transaction
- Export transactions to CSV
- Show summary by category

This file is intentionally small to provide a working demo GUI.
"""
import sys
import traceback
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QFormLayout,
    QLineEdit,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QMessageBox,
    QFileDialog,
)

from db import init_db, add_transaction, get_all_transactions, delete_transaction, export_transactions_csv, summary_by_category
from transaction import Transaction


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Personal Finance Tracker")
        self.resize(800, 600)

        init_db()

        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout()
        central.setLayout(layout)

        # form to add transaction
        form = QFormLayout()
        self.date_input = QLineEdit()
        self.date_input.setPlaceholderText("YYYY-MM-DD")
        self.amount_input = QLineEdit()
        self.amount_input.setPlaceholderText("e.g. -12.50 for expense, 1000 for income")
        self.category_input = QLineEdit()
        self.description_input = QLineEdit()

        form.addRow("Date:", self.date_input)
        form.addRow("Amount:", self.amount_input)
        form.addRow("Category:", self.category_input)
        form.addRow("Description:", self.description_input)

        add_btn = QPushButton("Add Transaction")
        add_btn.clicked.connect(self.on_add_transaction)
        form.addRow(add_btn)

        layout.addLayout(form)

        # table
        self.table = QTableWidget(0, 5)
        self.table.setHorizontalHeaderLabels(["ID", "Date", "Amount", "Category", "Description"])
        layout.addWidget(self.table)

        # actions
        btn_layout = QVBoxLayout()
        export_btn = QPushButton("Export CSV")
        export_btn.clicked.connect(self.on_export_csv)
        delete_btn = QPushButton("Delete Selected")
        delete_btn.clicked.connect(self.on_delete_selected)
        summary_btn = QPushButton("Show Summary")
        summary_btn.clicked.connect(self.on_show_summary)

        btn_layout.addWidget(export_btn)
        btn_layout.addWidget(delete_btn)
        btn_layout.addWidget(summary_btn)
        layout.addLayout(btn_layout)

        self.refresh_table()

    def refresh_table(self):
        try:
            rows = get_all_transactions()
            self.table.setRowCount(0)
            for r in rows:
                row = self.table.rowCount()
                self.table.insertRow(row)
                self.table.setItem(row, 0, QTableWidgetItem(str(r["id"])))
                self.table.setItem(row, 1, QTableWidgetItem(r["date"]))
                self.table.setItem(row, 2, QTableWidgetItem(str(r["amount"])))
                self.table.setItem(row, 3, QTableWidgetItem(r["category"]))
                self.table.setItem(row, 4, QTableWidgetItem(r["description"] or ""))
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load transactions:\n{e}")

    def on_add_transaction(self):
        date = self.date_input.text().strip()
        amount = self.amount_input.text().strip()
        category = self.category_input.text().strip()
        description = self.description_input.text().strip()
        try:
            tx = Transaction(date, amount, category, description)
            add_transaction(tx)
            self.date_input.clear()
            self.amount_input.clear()
            self.category_input.clear()
            self.description_input.clear()
            self.refresh_table()
        except Exception as e:
            QMessageBox.warning(self, "Validation error", str(e))

    def on_delete_selected(self):
        selected = self.table.selectionModel().selectedRows()
        if not selected:
            QMessageBox.information(self, "No selection", "Please select a row to delete.")
            return
        try:
            for idx in selected:
                row = idx.row()
                tx_id = int(self.table.item(row, 0).text())
                delete_transaction(tx_id)
            self.refresh_table()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to delete transaction:\n{e}")

    def on_export_csv(self):
        path, _ = QFileDialog.getSaveFileName(self, "Export Transactions", "transactions.csv", "CSV Files (*.csv)")
        if not path:
            return
        try:
            export_transactions_csv(path)
            QMessageBox.information(self, "Exported", f"Transactions exported to {path}")
        except Exception as e:
            traceback.print_exc()
            QMessageBox.critical(self, "Error", f"Failed to export CSV:\n{e}")

    def on_show_summary(self):
        try:
            summ = summary_by_category()
            if not summ:
                QMessageBox.information(self, "Summary", "No transactions yet.")
                return
            lines = [f"{cat}: {amount}" for cat, amount in summ.items()]
            QMessageBox.information(self, "Summary by category", "\n".join(lines))
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to compute summary:\n{e}")


def main():
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
