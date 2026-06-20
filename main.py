import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import csv
import os
import matplotlib.pyplot as plt

CATEGORIES = ["Food", "Travel", "Shopping", "Bills", "Education", "Healthcare", "Entertainment", "Other"]

CSV_FILE = "transactions.csv"



def handle_category_change(event):

    if category_combobox.get() == "Other":

        custom_category_label.grid(row=4, column=0, padx=5, pady=5)

        custom_category_entry.grid(row=4, column=1, padx=5, pady=5)

    else:

        custom_category_label.grid_remove()
        custom_category_entry.grid_remove()



def create_csv_file():

    if not os.path.exists(CSV_FILE):

        with open(CSV_FILE, "w", newline="", encoding="utf-8") as file:

            writer = csv.writer(file)

            writer.writerow(["Date", "Type", "Category", "Amount", "Description"])



def add_transaction():

    transaction_type = type_combobox.get()

    category = category_combobox.get()

    if category == "Other":

        category = custom_category_entry.get().strip()

        if not category:

            messagebox.showerror(
                "Error",
                "Please enter a custom category."
            )
            return

    amount = amount_entry.get().strip()

    description = description_entry.get().strip()

    if not amount:

        messagebox.showerror(
            "Error",
            "Please enter an amount."
        )
        return

    try:
        amount = float(amount)

    except ValueError:

        messagebox.showerror(
            "Error",
            "Amount must be a number."
        )
        return

    if amount <= 0:

        messagebox.showerror(
            "Error",
            "Amount must be greater than zero."
        )
        return

    date = datetime.now().strftime("%Y-%m-%d")

    with open(CSV_FILE, "a", newline="", encoding="utf-8") as file:

        writer = csv.writer(file)

        writer.writerow([date, transaction_type, category, amount, description])

    tree.insert(
        "",
        "end",
        values=(date, transaction_type, category, amount, description)
    )

    amount_entry.delete(0, tk.END)

    description_entry.delete(0, tk.END)

    custom_category_entry.delete(0, tk.END)

    update_summary()

    apply_filter()

    category_combobox.current(0)

    custom_category_label.grid_remove()
    custom_category_entry.grid_remove()



def load_transactions():

    with open(CSV_FILE, "r", newline="", encoding="utf-8") as file:

        reader = csv.reader(file)

        next(reader, None)

        for row in reader:

            tree.insert("", "end", values=row)



def update_summary():

    total_income = 0
    total_expenses = 0

    with open(CSV_FILE, "r", newline="", encoding="utf-8") as file:

        reader = csv.DictReader(file)

        for row in reader:

            amount = float(row["Amount"])

            if row["Type"] == "Income":
                total_income += amount

            else:
                total_expenses += amount

    balance = total_income - total_expenses

    income_label.config(
        text=f"Total Income: ₹{total_income:.2f}"
    )

    expense_label.config(
        text=f"Total Expenses: ₹{total_expenses:.2f}"
    )

    balance_label.config(
        text=f"Current Balance: ₹{balance:.2f}"
    )



def show_expense_breakdown():

    category_totals = {}

    with open(CSV_FILE, "r", newline="", encoding="utf-8") as file:

        reader = csv.DictReader(file)

        for row in reader:

            if row["Type"] == "Expense":

                category = row["Category"]
                amount = float(row["Amount"])

                if category not in category_totals:
                    category_totals[category] = 0

                category_totals[category] += amount

    if not category_totals:

        messagebox.showinfo(
            "No Data",
            "No expense data available."
        )
        return

    plt.figure(figsize=(7, 7))

    plt.pie(
        category_totals.values(),
        labels=category_totals.keys(),
        autopct="%1.1f%%"
    )

    plt.title("Expense Breakdown by Category")

    plt.show()



def show_monthly_trend():

    monthly_expenses = {}

    with open(CSV_FILE, "r", newline="", encoding="utf-8") as file:

        reader = csv.DictReader(file)

        for row in reader:

            if row["Type"] == "Expense":

                month = row["Date"][:7]      # YYYY-MM

                amount = float(row["Amount"])

                if month not in monthly_expenses:
                    monthly_expenses[month] = 0

                monthly_expenses[month] += amount

    if not monthly_expenses:

        messagebox.showinfo(
            "No Data",
            "No expense data available."
        )
        return

    months = sorted(monthly_expenses.keys())

    expenses = [
        monthly_expenses[month]
        for month in months
    ]

    plt.figure(figsize=(8, 5))

    plt.plot(
        months,
        expenses,
        marker="o"
    )

    plt.title("Monthly Expense Trend")
    plt.xlabel("Month")
    plt.ylabel("Amount (₹)")

    plt.grid(True)

    plt.show()



def apply_filter():

    for item in tree.get_children():
        tree.delete(item)

    search_text = search_entry.get().strip().lower()

    selected_type = filter_combobox.get()

    with open(CSV_FILE, "r", newline="", encoding="utf-8") as file:

        reader = csv.DictReader(file)

        for row in reader:

            matches_search = (
                search_text in row["Category"].lower()
                or search_text in row["Description"].lower()
            )

            matches_type = (
                selected_type == "All"
                or row["Type"] == selected_type
            )

            if matches_search and matches_type:

                tree.insert(
                    "",
                    "end",
                    values=(row["Date"], row["Type"], row["Category"], row["Amount"], row["Description"])
                )



def reset_filter():

    search_entry.delete(0, tk.END)

    filter_combobox.current(0)

    apply_filter()



def delete_transaction():

    selected_item = tree.selection()

    if not selected_item:

        messagebox.showwarning(
            "No Selection",
            "Please select a transaction to delete."
        )
        return

    confirm = messagebox.askyesno(
        "Confirm Delete",
        "Are you sure you want to delete this transaction?"
    )

    if not confirm:
        return

    selected_values = tree.item(selected_item[0], "values")

    rows = []

    deleted = False

    with open(CSV_FILE, "r", newline="", encoding="utf-8") as file:

        reader = csv.reader(file)

        header = next(reader)

        for row in reader:

            if (
                not deleted
                and tuple(row) == tuple(map(str, selected_values))
            ):
                deleted = True
                continue

            rows.append(row)

    with open(CSV_FILE, "w", newline="", encoding="utf-8") as file:

        writer = csv.writer(file)

        writer.writerow(header)

        writer.writerows(rows)

    apply_filter()

    update_summary()



create_csv_file()

root = tk.Tk()
root.title("Personal Finance Dashboard")
root.geometry("900x600")
root.resizable(True, True)

# Title
title_label = tk.Label(
    root,
    text="Personal Finance Dashboard",
    font=("Arial", 18, "bold")
)
title_label.pack(pady=10)

#Summary Frame
summary_frame = tk.Frame(root)

summary_frame.pack(pady=10)

income_label = tk.Label(
    summary_frame,
    text="Total Income: ₹0.00",
    font=("Arial", 12, "bold")
)

income_label.grid(row=0, column=0, padx=20)

expense_label = tk.Label(
    summary_frame,
    text="Total Expenses: ₹0.00",
    font=("Arial", 12, "bold")
)

expense_label.grid(row=0, column=1, padx=20)

balance_label = tk.Label(
    summary_frame,
    text="Current Balance: ₹0.00",
    font=("Arial", 12, "bold")
)

balance_label.grid(row=0, column=2, padx=20)

# Input Frame
input_frame = tk.Frame(root)
input_frame.pack(pady=10)

# Type
tk.Label(input_frame, text="Type").grid(row=0, column=0, padx=5, pady=5)

type_combobox = ttk.Combobox(
    input_frame,
    values=["Income", "Expense"],
    state="readonly",
    width=20
)
type_combobox.grid(row=0, column=1, padx=5, pady=5)
type_combobox.current(0)

# Category
tk.Label(input_frame, text="Category").grid(row=1, column=0, padx=5, pady=5)

category_combobox = ttk.Combobox(
    input_frame,
    values=CATEGORIES,
    state="readonly",
    width=20
)
category_combobox.grid(row=1, column=1, padx=5, pady=5)
category_combobox.current(0)

#Custom category
custom_category_label = tk.Label(input_frame, text="Custom Category")
custom_category_entry = tk.Entry(input_frame, width=23)

custom_category_label.grid(row=4, column=0, padx=5, pady=5)
custom_category_entry.grid(row=4, column=1, padx=5, pady=5)

custom_category_label.grid_remove()
custom_category_entry.grid_remove()

# Amount
tk.Label(input_frame, text="Amount").grid(row=2, column=0, padx=5, pady=5)

amount_entry = tk.Entry(input_frame, width=23)
amount_entry.grid(row=2, column=1, padx=5, pady=5)

# Description
tk.Label(input_frame, text="Description").grid(row=3, column=0, padx=5, pady=5)

description_entry = tk.Entry(input_frame, width=23)
description_entry.grid(row=3, column=1, padx=5, pady=5)

#Bind category event
category_combobox.bind(
    "<<ComboboxSelected>>",
    handle_category_change
)

# Transaction Button
add_button = tk.Button(
    input_frame,
    text="Add Transaction",
    command=add_transaction
)

add_button.grid(row=5, column=0, columnspan=2, pady=10)

# Expense Breakdown Button
chart_button = tk.Button(
    input_frame,
    text="Show Expense Breakdown",
    command=show_expense_breakdown
)

chart_button.grid(row=6, column=0, columnspan=2, pady=5)

# Monthly Trend Button
trend_button = tk.Button(
    input_frame,
    text="Show Monthly Trend",
    command=show_monthly_trend
)

trend_button.grid(row=7, column=0, columnspan=2, pady=5)

# Delete Transaction Button
delete_button = tk.Button(
    input_frame,
    text="Delete Selected Transaction",
    command=delete_transaction
)

delete_button.grid(row=8, column=0, columnspan=2, pady=5)

# Search Frame
search_frame = tk.Frame(root)
search_frame.pack(pady=10)

tk.Label(search_frame, text="Search").grid(row=0, column=0, padx=5)

search_entry = tk.Entry(search_frame, width=30)

search_entry.grid(row=0, column=1, padx=5)

# Filter Label
tk.Label(search_frame, text="Type").grid(row=0, column=2, padx=5)

filter_combobox = ttk.Combobox(
    search_frame,
    values=["All", "Income", "Expense"],
    state="readonly",
    width=15
)

filter_combobox.grid(row=0, column=3,padx=5)
filter_combobox.current(0)

# Filter Button
filter_button = tk.Button(
    search_frame,
    text="Apply Filter",
    command=apply_filter
)

filter_button.grid(row=0, column=4, padx=10)

# Reset Filter Button
reset_button = tk.Button(
    search_frame,
    text="Reset Filter",
    command=reset_filter
)

reset_button.grid(row=0, column=5, padx=5)

# Transaction Table
columns = ("Date", "Type", "Category", "Amount", "Description")

tree = ttk.Treeview(
    root,
    columns=columns,
    show="headings"
)

for column in columns:
    tree.heading(column, text=column)
    tree.column(column, width=150)

tree.pack(fill="both", expand=True, padx=20, pady=20)

load_transactions()

update_summary()

root.mainloop()
