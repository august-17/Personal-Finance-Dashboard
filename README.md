# Personal Finance Dashboard

A desktop-based Personal Finance Dashboard built with **Python, Tkinter, CSV, Matplotlib, and tkcalendar** that helps users manage income and expenses, track spending patterns, visualize financial data, and maintain transaction records through an intuitive graphical interface.

---

## Features

### Transaction Management
- Add income and expense transactions
- Edit existing transactions
- Delete single or multiple transactions at once
- Automatic transaction ID generation
- Custom transaction descriptions
- Persistent storage using CSV files

### Date Management
- User-selectable transaction dates using a calendar picker
- Supports recording past and future transactions
- Date stored in `YYYY-MM-DD` format

### Categories
- Predefined categories:
  - Food
  - Travel
  - Shopping
  - Bills
  - Education
  - Healthcare
  - Entertainment
- Custom category support through the **Other** option

### Financial Summary
- Total Income
- Total Expenses
- Current Balance

All values are automatically updated whenever transactions are added, edited, or deleted.

### Search and Filtering
- Search transactions by:
  - Date
  - Type
  - Category
  - Amount
  - Description
- Filter transactions by:
  - All
  - Income
  - Expense
- Reset filters instantly

### Data Visualization

#### Expense Breakdown
Interactive pie chart displaying:
- Category-wise expense distribution
- Percentage contribution of each category

#### Monthly Expense Trend
Line chart displaying:
- Monthly expense trends
- Expense growth and spending patterns over time

### Validation and Error Handling
- Prevents empty amount fields
- Validates numeric amounts
- Minimum amount validation
- Maximum amount validation
- Custom category validation
- CSV loading error handling
- CSV summary calculation error handling
- Edit operation validation
- Multi-selection protection during editing

---

## Technologies Used

- Python 3
- Tkinter
- ttk
- tkcalendar
- CSV
- Matplotlib
- OS Module
- Datetime Module

---

## Project Structure

```text
Personal-Finance-Dashboard/
│
├── main.py
├── transactions.csv
├── README.md
└── requirements.txt
```

---

## Installation

### Clone the Repository

```bash
git clone https://github.com/your-username/personal-finance-dashboard.git
cd personal-finance-dashboard
```

### Install Dependencies

```bash
pip install matplotlib
pip install tkcalendar
```

Or:

```bash
pip install -r requirements.txt
```

### Run the Application

```bash
python main.py
```

---

## Usage

### Adding a Transaction

1. Select a date.
2. Choose Income or Expense.
3. Select a category.
4. Enter amount.
5. Add an optional description.
6. Click **Add Transaction**.

### Editing a Transaction

1. Select a single transaction.
2. Click **Edit Selected Transaction**.
3. Modify the details.
4. Click **Save Changes**.

### Deleting Transactions

1. Select one or multiple transactions.
2. Click **Delete Selected Transaction(s)**.
3. Confirm deletion.

### Viewing Analytics

- Click **Show Expense Breakdown** for category-wise spending visualization.
- Click **Show Monthly Trend** to analyze monthly expenses.

---

## Data Storage

All transaction data is stored locally in:

```text
transactions.csv
```

The file is automatically created on first launch if it does not already exist.

CSV format:

```csv
ID,Date,Type,Category,Amount,Description
1,2026-06-22,Expense,Food,250,Lunch
2,2026-06-22,Income,Salary,50000,Monthly Salary
```

---

## Key Highlights

- User-friendly GUI built with Tkinter
- Calendar-based date selection
- Multi-transaction deletion support
- Real-time financial summaries
- Dynamic expense analytics
- Search and filtering functionality
- Strong input validation
- Persistent local storage
- Lightweight and easy to use

---

## Future Enhancements

- Export Financial Reports
- Excel Report Generation
- Advanced Financial Analytics
- Dashboard UI Redesign
- Dark Mode Support
- Budget Planning and Alerts
- Savings Goal Tracking
- Database Integration (SQLite/MySQL)

---

## Author

**August Kumar Sasmal**

B.Tech Computer Science & Engineering  
Manipal Institute of Technology, Manipal

