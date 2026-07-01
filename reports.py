import tkinter as tk
from tkinter import messagebox
from datetime import datetime

from constants import *
from finance import calculate_monthly_summary, calculate_category_totals, calculate_category_budget_status
from ui_helpers import enable_mousewheel_scrolling



def show_monthly_summary(root, selected_month):

    summary = calculate_monthly_summary(selected_month)

    monthly_income = summary["monthly_income"]
    monthly_expenses = summary["monthly_expenses"]
    net_savings = summary["net_savings"]

    income_count = summary["income_count"]
    expense_count = summary["expense_count"]

    budget = summary["budget"]
    remaining_budget = summary["remaining_budget"]

    display_month = datetime.strptime(selected_month, "%Y-%m").strftime("%B %Y")

    report_window = tk.Toplevel(root)

    report_window.title("Monthly Summary")

    report_window.geometry(f"{REPORT_WIDTH}x{REPORT_HEIGHT}")

    report_window.resizable(False, False)

    scrollbar = tk.Scrollbar(report_window)

    scrollbar.pack(side="right", fill="y")

    text = tk.Text(report_window, font=REPORT_FONT, yscrollcommand=scrollbar.set)

    text.pack(fill="both", expand=True, padx=10, pady=10)

    scrollbar.config(command=text.yview)

    enable_mousewheel_scrolling(text)

    report = ""

    report += f"Monthly Summary ({display_month})\n"

    report += "=" * 45 + "\n\n"

    report += f"{'Total Income':<25}₹{monthly_income:,.2f}\n"

    report += f"{'Total Expenses':<25}₹{monthly_expenses:,.2f}\n"

    report += f"{'Net Savings':<25}₹{net_savings:,.2f}\n"

    report += "\n"

    report += f"{'Income Transactions':<25}{income_count}\n"

    report += f"{'Expense Transactions':<25}{expense_count}\n"

    report += "\n"

    report += f"{'Budget':<25}₹{budget:,.2f}\n"

    if budget == 0:

        report += f"{'Budget Status':<25}Not Set\n"

    elif remaining_budget >= 0:

        report += (
            f"{'Budget Status':<25}"
            f"₹{remaining_budget:,.2f} Remaining\n"
        )

    else:

        report += (
            f"{'Budget Status':<25}"
            f"₹{abs(remaining_budget):,.2f} Exceeded\n"
        )

    text.insert("1.0", report)

    text.config(state="disabled")


def generate_monthly_summary(root, selector, month_name, year):

    month_number = datetime.strptime(month_name, "%B").month

    selected_month = f"{year}-{month_number:02d}"

    selector.destroy()

    show_monthly_summary(root,selected_month)


def show_monthly_category_report(root, selected_month): 

    category_totals = calculate_category_totals(selected_month)

    if not category_totals:

        messagebox.showinfo(
            "No Data",
            "No expense data available."
        )
        return
    
    display_month = datetime.strptime(selected_month, "%Y-%m").strftime("%B %Y")

    report_window = tk.Toplevel(root)

    report_window.title("Category-Wise Spending Report")

    report_window.geometry(f"{REPORT_WIDTH}x{REPORT_HEIGHT}")

    report_window.resizable(False, False)

    scrollbar = tk.Scrollbar(report_window)

    scrollbar.pack(side="right", fill="y")

    text = tk.Text(report_window, font=REPORT_FONT, yscrollcommand=scrollbar.set)

    text.pack(fill="both", expand=True, padx=10, pady=10)

    scrollbar.config(command=text.yview)

    enable_mousewheel_scrolling(text)

    report = f"Category Report ({display_month})\n"

    report += "=" * 40 + "\n\n"

    report += f"{'Category':<25}{'Amount'}\n"

    report += "-" * 40 + "\n"

    total_expenses = 0

    for category, amount in category_totals.items():

        report += (
            f"{category:<25}"
            f"₹{amount:,.2f}\n"
        )

        total_expenses += amount

    report += "-" * 40 + "\n"

    report += (
        f"{'Total Expenses':<25}"
        f"₹{total_expenses:,.2f}"
    )

    text.insert("1.0", report)

    text.config(state="disabled")


def generate_category_report(root, selector, month_name, year):

    month_number = datetime.strptime(month_name,"%B").month

    selected_month = f"{year}-{month_number:02d}"

    selector.destroy()

    show_monthly_category_report(root, selected_month)


def show_monthly_category_budget_status(root, selected_month):

    budget_status = calculate_category_budget_status(selected_month)

    if not budget_status:

        messagebox.showinfo(
            "No Budgets",
            "No category budgets have been set."
        )
        return

    display_month = datetime.strptime(selected_month, "%Y-%m").strftime("%B %Y")

    report_window = tk.Toplevel(root)

    report_window.title(f"Category Budget Status ({display_month})")

    report_window.geometry(f"{REPORT_WIDTH}x{REPORT_HEIGHT}")

    scrollbar = tk.Scrollbar(report_window)

    scrollbar.pack(side="right", fill="y")

    text = tk.Text(report_window, wrap="none", font=REPORT_FONT, yscrollcommand=scrollbar.set)

    text.pack(fill="both", expand=True, padx=10, pady=10)

    scrollbar.config(command=text.yview)

    enable_mousewheel_scrolling(text)

    report = f"Category Budget Status ({display_month})\n"

    report += "=" * 75 + "\n\n"

    report += (
        f"{'Category':<20}"
        f"{'Budget':>15}"
        f"{'Spent':>15}"
        f"{'Status':>25}\n"
    )

    report += "-" * 75 + "\n\n"

    for item in budget_status:

        category = item["category"]

        budget = item["budget"]

        spent = item["spent"]

        remaining = item["remaining"]

        if budget == 0:

            budget_text = "Not Set"
            status = "Not Set"

        else:

            budget_text = f"₹{budget:,.2f}"

            if remaining > 0:

                status = f"₹{remaining:,.2f} Remaining"

            elif remaining < 0:

                status = f"₹{abs(remaining):,.2f} Exceeded"

            else:

                status = "Limit Reached"

        if spent == 0:

            spent_text = "No Spending"

        else:

            spent_text = f"₹{spent:,.2f}"

        report += (
            f"{category:<20}"
            f"{budget_text:>15}"
            f"{spent_text:>15}"
            f"{status:>25}\n"
        )


    text.insert(tk.END, report)

    text.config(state="disabled")


def generate_category_budget_status(root, selector, month_name, year):

    month_number = datetime.strptime(month_name, "%B").month

    selected_month = f"{year}-{month_number:02d}"

    selector.destroy()

    show_monthly_category_budget_status(root, selected_month)