import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from tkcalendar import DateEntry
import csv
import os
from tkinter import filedialog
import shutil
import matplotlib.pyplot as plt

CATEGORIES = ["Food", "Travel", "Shopping", "Bills", "Education", "Healthcare", "Entertainment", "Other"]

CSV_FILE = os.path.join(os.path.dirname(__file__),"transactions.csv")

MIN_AMOUNT = 1
MAX_AMOUNT = 10000000

editing_transaction_id = None



def handle_category_change(event):

    if category_combobox.get() == "Other":

        custom_category_label.grid(row=5, column=0, padx=5, pady=5)

        custom_category_entry.grid(row=5, column=1, padx=5, pady=5)

    else:

        custom_category_label.grid_remove()
        custom_category_entry.grid_remove()



def create_csv_file():

    if not os.path.exists(CSV_FILE):

        with open(CSV_FILE, "w", newline="", encoding="utf-8") as file:

            writer = csv.writer(file)

            writer.writerow(["ID", "Date", "Type", "Category", "Amount", "Description"])



def get_next_id():

    highest_id = 0

    with open(CSV_FILE, "r", newline="", encoding="utf-8") as file:

        reader = csv.DictReader(file)

        for row in reader:

            current_id = int(row["ID"])

            if current_id > highest_id:
                highest_id = current_id

    return highest_id + 1



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

    if amount < MIN_AMOUNT:

        messagebox.showerror(
            "Error",
            f"Amount must be at least ₹{MIN_AMOUNT}."
        )
        return


    if amount > MAX_AMOUNT:

        messagebox.showerror(
            "Error",
            f"Amount cannot exceed ₹{MAX_AMOUNT:,}."
        )
        return
    
    transaction_id = get_next_id()

    date = date_entry.get()

    with open(CSV_FILE, "a", newline="", encoding="utf-8") as file:

        writer = csv.writer(file)

        writer.writerow([transaction_id, date, transaction_type, category, amount, description])

    tree.insert(
        "",
        "end",
        values=(transaction_id, date, transaction_type, category, amount, description)
    )

    amount_entry.delete(0, tk.END)

    description_entry.delete(0, tk.END)

    custom_category_entry.delete(0, tk.END)

    update_summary()

    apply_filter()

    category_combobox.current(0)

    custom_category_label.grid_remove()
    custom_category_entry.grid_remove()

    date_entry.set_date(datetime.now())



def load_transactions():

    try:

        with open(CSV_FILE, "r", newline="", encoding="utf-8") as file:

            reader = csv.reader(file)

            next(reader, None)

            for row in reader:

                tree.insert("", "end", values=row)

    except Exception as e:

        messagebox.showerror(
            "CSV Error",
            f"Unable to load transactions.\n\n{e}"
        )



def update_summary():

    total_income = 0
    total_expenses = 0

    try:

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

    except Exception as e:

        messagebox.showerror(
            "CSV Error",
            f"Unable to calculate summary.\n\n{e}"
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
                search_text in row["Date"].lower()
                or search_text in row["Type"].lower()
                or search_text in row["Category"].lower()
                or search_text in row["Amount"].lower()
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
                    values=(row["ID"],row["Date"], row["Type"], row["Category"], row["Amount"], row["Description"])
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
        f"Delete {len(selected_item)} selected transaction(s)?"
    )

    if not confirm:
        return

    transaction_ids = []

    for item in selected_item:

        values = tree.item(item, "values")
        transaction_ids.append(values[0])

    rows = []


    with open(CSV_FILE, "r", newline="", encoding="utf-8") as file:

        reader = csv.reader(file)

        header = next(reader)

        for row in reader:

            if row[0] in transaction_ids:
                continue

            rows.append(row)

    with open(CSV_FILE, "w", newline="", encoding="utf-8") as file:

        writer = csv.writer(file)

        writer.writerow(header)

        writer.writerows(rows)

    apply_filter()

    update_summary()



def edit_transaction():

    global editing_transaction_id

    selected_item = tree.selection()

    if len(selected_item) > 1:

        messagebox.showwarning(
            "Multiple Selection",
            "Please select only one transaction to edit."
        )
        return

    if not selected_item:

        messagebox.showwarning(
            "No Selection",
            "Please select a transaction to edit."
        )
        return

    values = tree.item(selected_item[0], "values")

    editing_transaction_id = values[0]

    date_entry.set_date(values[1])

    type_combobox.set(values[2])

    category = values[3]

    if category in CATEGORIES:

        category_combobox.set(category)

        custom_category_label.grid_remove()
        custom_category_entry.grid_remove()

    else:

        category_combobox.set("Other")

        custom_category_label.grid(row=5, column=0, padx=5, pady=5)

        custom_category_entry.grid(row=5, column=1, padx=5,pady=5)

        custom_category_entry.delete(0, tk.END)
        custom_category_entry.insert(0, category)

    amount_entry.delete(0, tk.END)
    amount_entry.insert(0, values[4])

    description_entry.delete(0, tk.END)
    description_entry.insert(0, values[5])



def save_changes():

    global editing_transaction_id

    if editing_transaction_id is None:

        messagebox.showwarning(
            "No Edit",
            "Select a transaction to edit first."
        )
        return

    transaction_type = type_combobox.get()

    date = date_entry.get()

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

    try:
        amount = float(amount)

    except ValueError:

        messagebox.showerror(
            "Error",
            "Amount must be a number."
        )
        return
    
    if amount < MIN_AMOUNT:

        messagebox.showerror(
            "Error",
            f"Amount must be at least ₹{MIN_AMOUNT}."
        )
        return


    if amount > MAX_AMOUNT:

        messagebox.showerror(
            "Error",
            f"Amount cannot exceed ₹{MAX_AMOUNT:,}."
        )
        return
    
    rows = []

    with open(CSV_FILE, "r", newline="", encoding="utf-8") as file:

        reader = csv.reader(file)

        header = next(reader)

        for row in reader:

            if row[0] == str(editing_transaction_id):

                row = [row[0], date, transaction_type, category, amount, description]

            rows.append(row)

    with open(CSV_FILE, "w", newline="", encoding="utf-8") as file:

        writer = csv.writer(file)

        writer.writerow(header)

        writer.writerows(rows)

    editing_transaction_id = None

    apply_filter()

    update_summary()

    amount_entry.delete(0, tk.END)
    description_entry.delete(0, tk.END)
    custom_category_entry.delete(0, tk.END)

    category_combobox.current(0)

    custom_category_label.grid_remove()
    custom_category_entry.grid_remove()

    date_entry.set_date(datetime.now())

    type_combobox.current(0)

    messagebox.showinfo(
        "Success",
        "Transaction updated successfully."
    )



def export_report():

    file_path = filedialog.asksaveasfilename(
        defaultextension=".csv",
        filetypes=[("CSV Files", "*.csv")],
        title="Save Financial Report"
    )

    if not file_path:
        return

    try:

        shutil.copy(
            CSV_FILE,
            file_path
        )

        messagebox.showinfo(
            "Success",
            "Financial report exported successfully."
        )

    except Exception as e:

        messagebox.showerror(
            "Export Error",
            f"Unable to export report.\n\n{e}"
        )



create_csv_file()

root = tk.Tk()
root.title("Personal Finance Dashboard")
root.geometry("1300x850")
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

# Date
tk.Label(input_frame, text="Date").grid(row=0, column=0, padx=5, pady=5)

date_entry = DateEntry(
    input_frame,
    width=20,
    date_pattern="yyyy-mm-dd"
)

date_entry.grid(row=0, column=1, padx=5, pady=5)

# Type
tk.Label(input_frame, text="Type").grid(row=1, column=0, padx=5, pady=5)

type_combobox = ttk.Combobox(
    input_frame,
    values=["Expense", "Income"],
    state="readonly",
    width=20
)
type_combobox.grid(row=1, column=1, padx=5, pady=5)
type_combobox.current(0)

# Category
tk.Label(input_frame, text="Category").grid(row=2, column=0, padx=5, pady=5)

category_combobox = ttk.Combobox(
    input_frame,
    values=CATEGORIES,
    state="readonly",
    width=20
)
category_combobox.grid(row=2, column=1, padx=5, pady=5)
category_combobox.current(0)

#Custom category
custom_category_label = tk.Label(input_frame, text="Custom Category")
custom_category_entry = tk.Entry(input_frame, width=23)

custom_category_label.grid(row=5, column=0, padx=5, pady=5)
custom_category_entry.grid(row=5, column=1, padx=5, pady=5)

custom_category_label.grid_remove()
custom_category_entry.grid_remove()

# Amount
tk.Label(input_frame, text="Amount").grid(row=3, column=0, padx=5, pady=5)

amount_entry = tk.Entry(input_frame, width=23)
amount_entry.grid(row=3, column=1, padx=5, pady=5)

# Description
tk.Label(input_frame, text="Description").grid(row=4, column=0, padx=5, pady=5)

description_entry = tk.Entry(input_frame, width=23)
description_entry.grid(row=4, column=1, padx=5, pady=5)

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

add_button.grid(row=6, column=0, columnspan=2, pady=10)

# Search Frame
search_frame = tk.Frame(root)
search_frame.pack(pady=10)

tk.Label(search_frame, text="Search").grid(row=0, column=0, padx=5)

search_entry = tk.Entry(search_frame, width=30)

search_entry.grid(row=0, column=1, padx=5)

# Action Frame
action_frame = tk.Frame(root)

action_frame.pack(pady=10)

# Edit Transaction Button
edit_button = tk.Button(
    action_frame,
    text="Edit Selected Transaction",
    command=edit_transaction
)

edit_button.grid(row=0, column=0, padx=5, pady=5)

# Save Changes Button
save_button = tk.Button(
    action_frame,
    text="Save Changes",
    command=save_changes
)

save_button.grid(row=0, column=1, padx=5, pady=5)

# Delete Transaction Button
delete_button = tk.Button(
    action_frame,
    text="Delete Selected Transaction(s)",
    command=delete_transaction
)

delete_button.grid(row=0, column=2, padx=5, pady=5)

# Expense Breakdown Button
chart_button = tk.Button(
    action_frame,
    text="Show Expense Breakdown",
    command=show_expense_breakdown
)

chart_button.grid(row=1, column=0, padx=5, pady=5)

# Monthly Trend Button
trend_button = tk.Button(
    action_frame,
    text="Show Monthly Trend",
    command=show_monthly_trend
)

trend_button.grid(row=1, column=1, padx=5, pady=5)

# Export button
export_button = tk.Button(
    action_frame,
    text="Export Financial Report",
    command=export_report
)

export_button.grid(row=1, column=2, padx=5, pady=5)

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
columns = ("ID", "Date", "Type", "Category", "Amount", "Description")

tree = ttk.Treeview(
    root,
    columns=columns,
    show="headings",
    selectmode="extended"
)

for column in columns:
    tree.heading(column, text=column)

    if column == "ID":

        tree.column(column, width=0, stretch=False)

    else:

        tree.column(column, width=150)

tree.pack(fill="both", expand=True, padx=20, pady=20)

load_transactions()

update_summary()

root.mainloop()
