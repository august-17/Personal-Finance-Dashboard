# Personal Finance Dashboard

A desktop-based Personal Finance Dashboard built with Python and Tkinter that helps users manage income, expenses, budgets, and financial reports through an intuitive graphical interface. The application provides transaction management, financial analytics, budget tracking, data visualization, and reporting features.

---

## Features

### Transaction Management
- Add income and expense transactions
- Edit existing transactions
- Delete single or multiple transactions
- Automatic transaction ID generation
- Calendar-based date selection
- Custom transaction categories using "Other"
- Input validation for amounts and budgets
- Automatic transaction table refresh after updates

### Financial Tracking
- Real-time income tracking
- Real-time expense tracking
- Current balance calculation
- Monthly budget management
- Budget status monitoring
- Budget exceeded alerts
- Budget reset functionality
- Monthly expense monitoring

### Search & Filtering
- Search transactions by:
  - Date
  - Type
  - Category
  - Amount
  - Description
- Filter by:
  - All Transactions
  - Income
  - Expense
- Reset filters instantly

### Reports & Analytics
- Expense Breakdown Pie Chart
- Monthly Expense Trend Graph
- Category-Wise Spending Report
- CSV Financial Report Export

### Data Management
- CSV-based transaction storage
- Persistent budget storage
- Automatic data loading on startup
- Multi-transaction deletion support

### User Interface
- Interactive transaction table
- Responsive Tkinter GUI
- Organized action controls
- Calendar date picker
- Simple and user-friendly design

---

## Technologies Used

- Python
- Tkinter
- ttk
- tkcalendar
- Matplotlib
- CSV
- OS Module
- Shutil

---

## Project Structure

```text
Personal-Finance-Dashboard/
│
├── main.py
├── transactions.csv
├── budget.txt
├── README.md
└── requirements.txt
```

---

## Installation

### Clone Repository

```bash
git clone https://github.com/august-17/personal-finance-dashboard.git
cd personal-finance-dashboard
```

### Install Dependencies

```bash
pip install tkcalendar matplotlib
```

### Run Application

```bash
python main.py
```

---

## How It Works

### Adding Transactions

1. Select date
2. Choose transaction type
3. Select category
4. Enter amount
5. Add description
6. Click **Add Transaction**

### Budget Management

1. Enter monthly budget
2. Click **Set Budget**
3. Monitor budget status in real time
4. Reset budget when required

### Analytics

Users can generate:

- Expense Breakdown Pie Chart
- Monthly Expense Trend
- Category-Wise Spending Report
- Financial Report Export

---

## Current Implemented Features

### Transaction System
✔ Add Transactions  
✔ Edit Transactions  
✔ Save Edited Transactions  
✔ Multi-Transaction Delete  
✔ Custom Categories  
✔ Input Validation  

### Budget System
✔ Monthly Budget Tracking  
✔ Budget Status Monitoring  
✔ Budget Exceeded Detection  
✔ Budget Reset Functionality  

### Reports
✔ Expense Breakdown Chart  
✔ Monthly Expense Trend  
✔ Category-Wise Spending Report  
✔ CSV Report Export  

### Search & Filter
✔ Search Transactions  
✔ Filter by Type  
✔ Reset Filters  
✔ Auto Refresh After Updates  

---

## Upcoming Features

### Analytics
- Monthly Summary Popup
- Income vs Expense Pie Chart
- Income vs Expense Bar Chart
- Dashboard Insights
- Advanced Analytics

### Exporting
- Export Filtered Results
- Excel Report Export
- PDF Report Export

### Transaction Enhancements
- Sort Transactions (Date, Amount, Category)
- Undo Delete

### Budget Improvements
- Category Budgeting

### UI Improvements
- Dashboard Cards
- Dark Theme
- Modern UI Design
- Complete Dashboard Redesign

---

## Key Learning Outcomes

This project demonstrates:

- Object-oriented programming concepts
- GUI development using Tkinter
- Data persistence using CSV files
- File handling in Python
- Financial data processing
- Data visualization using Matplotlib
- User input validation
- Budget tracking logic
- Search and filtering implementation

---

## Future Scope

The project can be expanded into a full-featured finance management system by integrating:

- SQLite database support
- User authentication
- Cloud synchronization
- Expense forecasting
- AI-powered spending insights
- PDF and Excel reporting
- Multi-user support
- Mobile application integration

---

## Author

**August Kumar Sasmal**

B.Tech Computer Science & Engineering 
Manipal Institute of Technology, Manipal