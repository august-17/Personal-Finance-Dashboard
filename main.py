import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.title("Personal Finance Dashboard")
root.geometry("900x600")

# Title
title_label = tk.Label(
    root,
    text="Personal Finance Dashboard",
    font=("Arial", 18, "bold")
)
title_label.pack(pady=10)

# Input Frame
input_frame = tk.Frame(root)
input_frame.pack(pady=10)

# Type
tk.Label(input_frame, text="Type").grid(row=0, column=0, padx=5, pady=5)

type_combobox = ttk.Combobox(
    input_frame,
    values=["Income", "Expense"],
    state="readonly"
)
type_combobox.grid(row=0, column=1, padx=5, pady=5)
type_combobox.current(0)

# Category
tk.Label(input_frame, text="Category").grid(row=1, column=0, padx=5, pady=5)

category_entry = tk.Entry(input_frame)
category_entry.grid(row=1, column=1, padx=5, pady=5)

# Amount
tk.Label(input_frame, text="Amount").grid(row=2, column=0, padx=5, pady=5)

amount_entry = tk.Entry(input_frame)
amount_entry.grid(row=2, column=1, padx=5, pady=5)

# Description
tk.Label(input_frame, text="Description").grid(row=3, column=0, padx=5, pady=5)

description_entry = tk.Entry(input_frame)
description_entry.grid(row=3, column=1, padx=5, pady=5)

# Button
add_button = tk.Button(
    input_frame,
    text="Add Transaction"
)
add_button.grid(row=4, column=0, columnspan=2, pady=10)

# Table
columns = (
    "Date",
    "Type",
    "Category",
    "Amount",
    "Description"
)

tree = ttk.Treeview(
    root,
    columns=columns,
    show="headings"
)

for column in columns:
    tree.heading(column, text=column)
    tree.column(column, width=150)

tree.pack(fill="both", expand=True, padx=20, pady=20)

root.mainloop()