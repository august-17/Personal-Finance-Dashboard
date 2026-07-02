import tkinter as tk
from tkinter import messagebox
from datetime import datetime

from constants import (
    CUSTOM_CATEGORY,
    COLUMNS, 
    SORTABLE_COLUMNS
)

from storage import get_all_categories

from finance import calculate_dashboard_summary

import app_state



# ========================================
# Treeview Sorting
# ========================================

def update_sort_headers():

    for column in COLUMNS:

        heading = column

        if column == app_state.sort_column:

            if app_state.sort_reverse.get(column, False):

                heading = f"{column} ▼"

            else:

                heading = f"{column} ▲"

        if column in SORTABLE_COLUMNS:

            app_state.tree.heading(
                column,
                text=heading,
                command=lambda c=column: sort_treeview(c)
            )

        else:

            app_state.tree.heading(
                column,
                text=heading
            )


def sort_treeview(column, toggle=True):

    if toggle:

        if app_state.sort_column == column:

            app_state.sort_reverse[column] = not app_state.sort_reverse.get(column, False)

        else:

            app_state.sort_column = column

            app_state.sort_reverse.setdefault(column, False)

    else:

        app_state.sort_column = column

    data = []

    for item in app_state.tree.get_children():

        values = app_state.tree.item(item)["values"]

        data.append((values, item))

    if column == "Amount":

        data.sort(
            key=lambda x: float(x[0][4]),
            reverse=app_state.sort_reverse.get(column, False)
        )

    elif column == "Date":

        data.sort(
            key=lambda x: (
                datetime.strptime(x[0][1], "%Y-%m-%d"),
                int(x[0][0])
            ),
            reverse=app_state.sort_reverse.get(column, False)
        )

    elif column == "Category":

        data.sort(
            key=lambda x: x[0][3].lower(),
            reverse=app_state.sort_reverse.get(column, False)
        )

    else:

        return

    for index, (_, item) in enumerate(data):

        app_state.tree.move(item, "", index)

    update_sort_headers()

# ========================================
# Input Helpers
# ========================================

def clear_inputs():

    app_state.amount_entry.delete(0, tk.END)

    app_state.description_entry.delete(0, tk.END)

    app_state.custom_category_entry.delete(0, tk.END)

    app_state.category_combobox.current(0)

    app_state.custom_category_label.grid_remove()
    app_state.custom_category_entry.grid_remove()

    app_state.date_entry.set_date(datetime.now())

    app_state.type_combobox.current(0)


# ========================================
# Category List Refresher
# ========================================

def refresh_category_combobox():

    app_state.category_combobox["values"] = get_all_categories() + [CUSTOM_CATEGORY]


# ========================================
# Dashboard Summary
# ========================================

def update_summary():

    try:

        summary = calculate_dashboard_summary()

        app_state.income_label.config(
            text=f"Monthly Income: ₹{summary['monthly_income']:,.2f}"
        )

        app_state.expense_label.config(
            text=f"Monthly Expenses: ₹{summary['monthly_expenses']:,.2f}"
        )

        app_state.budget_label.config(
            text=f"Monthly Budget: ₹{summary['budget']:,.2f}"
        )

        balance = summary["balance"]
        budget = summary["budget"]
        remaining_budget = summary["remaining_budget"]

        if balance >= 0:

            app_state.balance_label.config(
                text=f"Current Balance: ₹{balance:,.2f}",
                fg="green"
            )

        else:

            app_state.balance_label.config(
                text=f"Current Deficit: ₹{abs(balance):,.2f}",
                fg="red"
            )

        if budget == 0:

            app_state.status_label.config(
                text="Budget Status: Not Set",
                fg="black"
            )

        elif remaining_budget >= 0:

            app_state.status_label.config(
                text=f"Budget Status: ₹{remaining_budget:,.2f} Remaining",
                fg="green"
            )

        else:

            app_state.status_label.config(
                text=f"Budget Status: ₹{abs(remaining_budget):,.2f} Exceeded",
                fg="red"
            )

    except Exception as e:

        messagebox.showerror(
            "CSV Error",
            f"Unable to calculate summary.\n\n{e}"
        )