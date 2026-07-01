from datetime import datetime

from constants import *
from storage import read_transactions, get_all_categories
from budget import load_budget, load_category_budgets


def calculate_dashboard_summary():

    monthly_income = 0
    monthly_expenses = 0

    budget = load_budget()

    current_month = datetime.now().strftime("%Y-%m")

    transactions = read_transactions()

    for row in transactions:

        amount = float(row["Amount"])

        if row["Date"].startswith(current_month):

            if row["Type"] == "Income":

                monthly_income += amount

            else:

                monthly_expenses += amount

    balance = monthly_income - monthly_expenses

    remaining_budget = budget - monthly_expenses
    
    return {

        "monthly_income": monthly_income,

        "monthly_expenses": monthly_expenses,

        "balance": balance,

        "budget": budget,

        "remaining_budget": remaining_budget

    }


def calculate_monthly_summary(selected_month):

    monthly_income = 0
    monthly_expenses = 0

    income_count = 0
    expense_count = 0

    transactions = read_transactions()

    for row in transactions:

        if not row["Date"].startswith(selected_month):

            continue

        amount = float(row["Amount"])

        if row["Type"] == "Income":

            monthly_income += amount
            income_count += 1

        else:

            monthly_expenses += amount
            expense_count += 1

    net_savings = monthly_income - monthly_expenses

    budget = load_budget()

    remaining_budget = budget - monthly_expenses

    return {

        "monthly_income": monthly_income,

        "monthly_expenses": monthly_expenses,

        "net_savings": net_savings,

        "income_count": income_count,

        "expense_count": expense_count,

        "budget": budget,

        "remaining_budget": remaining_budget

    }


def calculate_category_totals(selected_month):

    category_totals = {}

    transactions = read_transactions()

    for row in transactions:

        if (row["Type"] == "Expense" and row["Date"].startswith(selected_month)):

            category = row["Category"]

            amount = float(row["Amount"])

            category_totals[category] = (category_totals.get(category, 0) + amount)

    category_totals = dict(
        sorted(
            category_totals.items(),
            key=lambda item: item[1],
            reverse=True
        )
    )

    return category_totals


def calculate_category_budget_status(selected_month):

    category_budgets = load_category_budgets()

    category_totals = calculate_category_totals(selected_month)

    budget_status = []

    all_categories = sorted(set(get_all_categories()) | set(category_budgets.keys()))

    for category in all_categories:

        budget = category_budgets[category]

        spent = category_totals.get(category, 0)

        remaining = budget - spent

        budget_status.append({

            "category": category,

            "budget": budget,

            "spent": spent,

            "remaining": remaining

        })

    return budget_status


def calculate_monthly_trend():

    monthly_expenses = {}

    transactions = read_transactions()

    for row in transactions:

        if row["Type"] == "Expense":

            continue

        month = row["Date"][:7]      # YYYY-MM

        amount = float(row["Amount"])

        monthly_expenses[month] = (monthly_expenses.get(month, 0) + amount)

    if not monthly_expenses:

        return [], []
    
    months = sorted(monthly_expenses.keys())

    start_month = datetime.strptime(months[0], "%Y-%m")
    end_month = datetime.strptime(months[-1], "%Y-%m")

    all_months = []

    current = start_month

    while current <= end_month:

        all_months.append(current.strftime("%Y-%m"))

        if current.month == 12:

            current = current.replace(
                year=current.year + 1,
                month=1
            )

        else:

            current = current.replace(
                month=current.month + 1
            )

    expenses = [
        monthly_expenses.get(month, 0)
        for month in all_months
    ]

    return all_months, expenses


def calculate_expense_breakdown(selected_month):

    category_totals = calculate_category_totals(selected_month)

    if not category_totals:

        return {}, 0

    total_expense = sum(category_totals.values())

    chart_data = {}

    others_total = 0

    for category, amount in category_totals.items():

        percentage = (amount / total_expense) * 100

        if percentage < MIN_PIE_PERCENTAGE:

            others_total += amount

        else:

            chart_data[category] = amount

    if others_total > 0:

        chart_data["Others"] = others_total

    return chart_data, total_expense