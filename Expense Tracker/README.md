# Expense Tracker

A simple Python GUI application for tracking daily expenses, built using `tkinter`.

## Features

- **Add Expenses**: Record expenses with an amount, category, and date.
- **Delete Expenses**: Select an expense from the list to remove it.
- **Date Picker**: Convenient built-in calendar to select the expense date.
- **Summary Reports**: 
  - View total expenses per category.
  - View total expenses per month.
- **Data Persistence**: Expenses are automatically saved to and loaded from a local `expenses.json` file.

## Requirements

- Python 3.x
- `tkinter` (usually comes pre-installed with Python)

## How to Run

1. Navigate to the project directory in your terminal.
2. Run the following command:

   ```bash
   python tracker.py
   ```

## Usage

1. Enter the amount in the "Amount" field.
2. Enter the category (e.g., Food, Transport, Entertainment) in the "Category" field.
3. Use the "Choose Date" button to select a date, or manually enter it in `YYYY-MM-DD` format.
4. Click "Add Expense" to record it.
5. You can view all records in the list at the bottom.
6. Use "Category Totals" and "Monthly Totals" buttons to see summaries of your expenses.
