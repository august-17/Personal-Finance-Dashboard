# Personal Finance Dashboard

A desktop-based personal finance management application built with **Python** and **Tkinter** that enables users to efficiently track income and expenses, manage budgets, visualize spending patterns, and generate financial reports.

The application provides an intuitive graphical interface with advanced budgeting tools, reporting capabilities, data visualization, and export functionality to help users monitor and analyze their financial activities.

---

## Features

### Transaction Management

- Add income and expense transactions
- Edit existing transactions
- Delete multiple transactions
- Undo deleted transactions
- Automatic transaction ID generation
- Calendar-based date selection
- Support for custom expense categories
- Automatic CSV-based data storage

### Dashboard Overview

- Total Income
- Total Expenses
- Current Balance / Deficit
- Monthly Budget
- Remaining or Exceeded Budget Status

### Budget Management

#### Monthly Budget

- Set monthly spending limits
- Reset monthly budget
- Automatic budget tracking
- Warning before exceeding the monthly budget

#### Category Budgets

- Individual budgets for each category
- Support for dynamically created custom categories
- Category-specific overspending warnings
- Reset individual category budgets

### Search & Filtering

- Real-time transaction search
- Filter transactions by type
- Reset filters instantly
- Optimized debounced searching for improved responsiveness

### Reports

Generate reports for any selected month:

- Monthly Financial Summary
- Category-wise Spending Report
- Category Budget Status Report

### Data Visualization

#### Expense Breakdown

- Category-wise pie chart
- Automatic grouping of very small categories into **Others**
- Percentage-based expense distribution

#### Monthly Expense Trend

- Line chart showing monthly expenses
- Continuous timeline across months
- Automatic handling of months without transactions

### Export Options

Export monthly financial reports in:

- CSV
- PDF
- Microsoft Excel (.xlsx)

Generated reports include professionally formatted tables suitable for sharing and record keeping.

### Sorting

Sortable transaction table by:

- Date
- Amount
- Category

Supports both ascending and descending order.

### Data Protection

- Automatic backup before editing, deleting, or adding transactions
- Local data storage
- Undo functionality for deleted transactions

### Input Validation

Comprehensive validation for:

- Amount limits
- Numeric inputs
- Description length
- Custom category names
- Invalid characters
- Empty fields

---

## Technology Stack

| Category | Technology |
|----------|------------|
| Language | Python 3 |
| GUI Framework | Tkinter |
| Calendar Widget | tkcalendar |
| Charts | Matplotlib |
| PDF Reports | ReportLab |
| Excel Reports | OpenPyXL |
| Data Storage | CSV, JSON |

---

## Project Structure

```
Personal-Finance-Dashboard/
│
├── main.py
├── transactions.csv
├── backup_transactions.csv
├── budget.txt
├── category_budget.json
├── requirements.txt
├── README.md
└── screenshots/
```

---

## Installation

Clone the repository:

```bash
git clone https://github.com/august-17/Personal-Finance-Dashboard.git
```

Navigate to the project directory:

```bash
cd Personal-Finance-Dashboard
```

Install the required dependencies:

```bash
pip install -r requirements.txt
```

Or install manually:

```bash
pip install tkcalendar matplotlib reportlab openpyxl
```

Run the application:

```bash
python main.py
```

---

## Data Storage

The application stores all information locally.

| File | Description |
|------|-------------|
| transactions.csv | Transaction database |
| backup_transactions.csv | Automatic backup |
| budget.txt | Monthly budget |
| category_budget.json | Category-wise budgets |

---

## Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| **Enter** | Add Transaction |
| **Ctrl + S** | Save Changes |
| **Ctrl + E** | Edit Transaction |
| **Delete** | Delete Selected Transaction(s) |
| **Ctrl + Z** | Undo Delete |
| **Ctrl + F** | Focus Search |
| **Esc** | Clear Input Fields |

---

## Future Enhancements

- Recurring Transactions
- Savings Goals
- Password Protection
- SQLite Database Support
- Cloud Synchronization
- Dark Mode
- Multi-user Profiles
- Expense Forecasting using Machine Learning

---

## Author

**August Kumar Sasmal**

B.Tech Computer Science & Engineering
Manipal Institute of Technology