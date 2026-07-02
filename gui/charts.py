import matplotlib.pyplot as plt
from datetime import datetime
from tkinter import messagebox

from gui.dialogs import get_selected_month

from core.finance import (
    calculate_monthly_trend, 
    calculate_expense_breakdown
)



def show_monthly_trend():

    all_months, expenses = calculate_monthly_trend()

    if not all_months:

        messagebox.showinfo(
            "No Data",
            "No expense data available."
        )
        return

    plt.figure(figsize=(8, 5))

    display_months = [
        datetime.strptime(month, "%Y-%m").strftime("%b %Y")
        for month in all_months
    ]

    plt.plot(
        display_months,
        expenses,
        marker="o",
        linewidth=2
    )

    plt.title("Monthly Expense Trend")
    plt.xlabel("Month")
    plt.ylabel("Amount (₹)")

    plt.grid(True)

    plt.show()

    plt.close()


def show_monthly_expense_breakdown(selected_month):

    chart_data, total_expense = calculate_expense_breakdown(selected_month)

    if not chart_data:

        messagebox.showinfo(
            "No Data",
            "No expense data available."
        )
        return

    labels = list(chart_data.keys())

    amounts = list(chart_data.values())

    display_month = datetime.strptime(selected_month, "%Y-%m").strftime("%B %Y")    

    plt.figure(figsize=(10, 7))

    wedges, _, _ = plt.pie(
        amounts,
        autopct="%1.1f%%",
        startangle=90
    )

    plt.legend(
        wedges,
        labels,
        title="Categories",
        loc="center left",
        bbox_to_anchor=(1, 0.5)
    )

    plt.title(
        f"Expense Breakdown by Category ({display_month})\n"
        f"Total Expenses: ₹{total_expense:,.2f}"  
    )

    plt.axis("equal")

    plt.tight_layout()

    plt.show()

    plt.close()


def generate_expense_breakdown(selector, month_name, year):

    selected_month = get_selected_month(month_name, year)

    selector.destroy()

    show_monthly_expense_breakdown(selected_month)