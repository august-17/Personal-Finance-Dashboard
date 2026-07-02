# Personal Finance Dashboard

A desktop application built with **Python** and **Tkinter** for managing personal finances through transaction tracking, budgeting, financial reporting, data visualization, and report exporting.

The application follows a modular architecture with a clear separation between business logic, user interface, data management, and validation, making it scalable, maintainable, and easy to extend.

---

## Features

### Transaction Management

- Add income and expense transactions
- Edit existing transactions
- Delete single or multiple transactions
- Undo deleted transactions
- Automatic transaction ID generation
- Calendar-based date selection
- Automatic backup before every data modification

### Category Management

- Built-in expense categories
- Support for unlimited custom categories
- Automatic addition of custom categories to the category list
- Automatic removal of unused custom categories
- Dynamic category list updates without restarting the application

### Budget Management

- Monthly budget management
- Category-wise budget management
- Budget warning before exceeding the monthly limit
- Category budget warning before exceeding category limits
- Budget reset functionality
- Remaining budget tracking
- Budget status monitoring

### Dashboard

The dashboard updates automatically after every transaction and displays:

- Monthly Income
- Monthly Expenses
- Monthly Budget
- Current Balance
- Remaining Budget
- Budget Status

### Search and Filtering

- Instant transaction search
- Search by:
  - Date
  - Transaction Type
  - Category
  - Amount
  - Description
- Filter transactions by type
- One-click filter reset
- Debounced search for improved performance

### Transaction Table

- Sort by Date
- Sort by Amount
- Sort by Category
- Ascending and descending sorting
- Visual sort indicators
- Recent transactions displayed first for identical dates
- Alternating row colors for improved readability

### Reports

Generate detailed monthly reports including:

- Monthly Financial Summary
- Category-wise Spending Report
- Category Budget Status Report

Each report includes:

- Total Income
- Total Expenses
- Net Savings
- Transaction Counts
- Budget Utilization
- Category-wise Spending
- Remaining Budget

### Data Visualization

#### Monthly Expense Trend

- Monthly expense trend using a line chart
- Automatically handles months with no transactions

#### Expense Breakdown

- Category-wise expense distribution using a pie chart
- Small categories are automatically grouped into **Others**

### Report Export

Export monthly reports in:

- CSV
- PDF
- Microsoft Excel (.xlsx)

### Input Validation

- Numeric amount validation
- Minimum and maximum transaction limits
- Description length validation
- Custom category validation
- Empty field validation
- Invalid character validation

### Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| Enter | Add Transaction |
| Ctrl + S | Save Changes |
| Ctrl + E | Edit Transaction |
| Delete | Delete Transaction |
| Ctrl + Z | Undo Delete |
| Ctrl + F | Focus Search |
| Esc | Clear Input Fields |

---

## Project Structure

```text
Personal-Finance-Dashboard/
│
├── main.py
├── constants.py
├── app_state.py
│
├── core/
│   ├── budgets.py
│   ├── finance.py
│   ├── operations.py
│   ├── storage.py
│   └── validation.py
│
├── gui/
│   ├── charts.py
│   ├── dialogs.py
│   ├── export.py
│   ├── gui.py
│   ├── gui_actions.py
│   ├── reports.py
│   └── ui_helpers.py
│
├── data/
│   ├── transactions.csv
│   ├── backup_transactions.csv
│   ├── budget.txt
│   └── category_budget.json
│
├── requirements.txt
└── README.md
```

---

## Requirements

- Python 3.10 or later

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/august-17/Personal-Finance-Dashboard.git
```

### 2. Navigate to the project directory

```bash
cd Personal-Finance-Dashboard
```

### 3. Install the required dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the application

```bash
python main.py
```

---

## Usage

1. Launch the application.
2. Add income and expense transactions.
3. Set monthly and category-wise budgets.
4. Monitor the dashboard for real-time financial insights.
5. Search, filter, edit, or delete transactions.
6. Generate reports and visualizations.
7. Export monthly reports in CSV, PDF, or Excel format.

---

## Dependencies

- Python
- Tkinter
- tkcalendar
- Matplotlib
- OpenPyXL
- ReportLab

---

## Data Storage

The application stores all information locally.

| File | Purpose |
|------|---------|
| transactions.csv | Stores transaction records |
| backup_transactions.csv | Automatic backup of transaction data |
| budget.txt | Stores the monthly budget |
| category_budget.json | Stores category-wise budgets |

---

## Design Highlights

- Modular architecture with clear separation of business logic and user interface
- Automatic transaction backup before every data modification
- Dynamic custom category management
- Monthly and category-wise budgeting
- Real-time dashboard updates
- Interactive reports and charts
- Multiple export formats
- Keyboard shortcuts for improved productivity
- Clean, scalable, and maintainable codebase

---

## Future Enhancements

- SQLite database integration
- User authentication
- Multiple user profiles
- Recurring transactions
- Savings goals
- Expense forecasting
- Cloud synchronization
- Dark mode
- Dashboard customization
- Import transactions from CSV and Excel

---

## Author

**August Kumar Sasmal**

B.Tech Computer Science & Engineering
Manipal Institute of Technology