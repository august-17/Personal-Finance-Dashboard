import csv
import tkinter as tk
from tkinter import messagebox
from datetime import datetime

from constants import (
    CSV_FILE,
    CSV_HEADERS,
    CATEGORIES,
    CUSTOM_CATEGORY
)

from core.storage import (
    create_backup, 
    get_next_id, 
    read_transactions
)

from core.validation import (
    validate_amount, 
    validate_description, 
    get_category
)

from core.budgets import (
    check_budget_warning, 
    check_category_budget_warning
)

from gui.ui_helpers import (
    insert_transaction_row
)

from gui.gui_actions import (
    update_summary, 
    sort_treeview, 
    clear_inputs,
    refresh_category_combobox
)

import app_state



def add_transaction():

    transaction_type = app_state.type_combobox.get()

    category = get_category(app_state.category_combobox, app_state.custom_category_entry)

    if category is None:

        return

    amount = validate_amount(app_state.amount_entry)

    if amount is None:

        return
    
    if not check_budget_warning(transaction_type, amount):

        return
    
    if not check_category_budget_warning(transaction_type, category, amount):

        return
    
    description = validate_description(app_state.description_entry)

    if description is None:

        return
    
    transaction_id = get_next_id()

    date = app_state.date_entry.get()

    create_backup()

    with open(CSV_FILE, "a", newline="", encoding="utf-8") as file:

        writer = csv.writer(file)

        writer.writerow([transaction_id, date, transaction_type, category, amount, description])

    refresh_category_combobox()

    clear_inputs()

    update_summary()

    apply_filter()


def load_transactions():

    try:

        transactions = read_transactions()

        transactions.sort(
            key=lambda row: (
                datetime.strptime(row["Date"], "%Y-%m-%d"), 
                int(row["ID"])
            ),
            reverse=True
        )

        for row in transactions:

            insert_transaction_row(app_state.tree, row)

    except Exception as e:

        messagebox.showerror(
            "CSV Error",
            f"Unable to load transactions.\n\n{e}"
        )


def apply_filter():

    for item in app_state.tree.get_children():

        app_state.tree.delete(item)

    search_text = app_state.search_entry.get().lower().strip()

    selected_type = app_state.filter_combobox.get()

    transactions = read_transactions()

    for row in transactions:

        searchable_text = " ".join([
            row["Date"],
            row["Type"],
            row["Category"],
            row["Amount"],
            row["Description"]
        ]).lower()

        matches_search = search_text in searchable_text

        matches_type = (selected_type == "All" or row["Type"] == selected_type)

        if matches_search and matches_type:

            insert_transaction_row(app_state.tree, row)

    if app_state.sort_column is not None:

        sort_treeview(app_state.sort_column, toggle=False)


def reset_filter():

    app_state.search_entry.delete(0, tk.END)

    app_state.filter_combobox.current(0)

    apply_filter()


def delete_transaction():

    selected_item = app_state.tree.selection()

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

    transaction_ids = set()

    current_delete = []

    for item in selected_item:

        values = app_state.tree.item(item, "values")
        transaction_ids.add(values[0])

    transactions = read_transactions()

    updated_transactions = []

    for index, transaction in enumerate(transactions):

        if transaction["ID"] in transaction_ids:
                
            current_delete.append((index, transaction.copy()))
                
            continue

        updated_transactions.append(transaction)

    create_backup()

    with open(CSV_FILE, "w", newline="", encoding="utf-8") as file:

        writer = csv.DictWriter(file, fieldnames=CSV_HEADERS)

        writer.writeheader()

        writer.writerows(updated_transactions)

    app_state.delete_history.append(current_delete)

    refresh_category_combobox()

    apply_filter()

    update_summary()

    app_state.undo_delete_button.config(state="normal")


def undo_delete():

    if not app_state.delete_history:

        messagebox.showinfo(
            "Undo Delete",
            "Nothing to undo."
        )
        return
    
    last_deleted_transactions = app_state.delete_history.pop()
    
    transactions = read_transactions()

    for index, transaction in sorted(last_deleted_transactions, key=lambda x: x[0]):

        transactions.insert(index, transaction)

    create_backup()

    with open(CSV_FILE, "w", newline="", encoding="utf-8") as file:

        writer = csv.DictWriter(file, fieldnames=CSV_HEADERS)

        writer.writeheader()

        writer.writerows(transactions)

    if not app_state.delete_history:

        app_state.undo_delete_button.config(state="disabled")

    refresh_category_combobox()

    apply_filter()

    update_summary()

    messagebox.showinfo(
        "Undo Delete",
        "Deleted transaction(s) restored successfully."
    )


def edit_transaction():

    selected_item = app_state.tree.selection()

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

    values = app_state.tree.item(selected_item[0], "values")

    app_state.editing_transaction_id = values[0]

    app_state.date_entry.set_date(values[1])

    app_state.type_combobox.set(values[2])

    category = values[3]

    if category in CATEGORIES:

        app_state.category_combobox.set(category)

        app_state.custom_category_label.grid_remove()
        app_state.custom_category_entry.grid_remove()

    else:

        app_state.category_combobox.set(CUSTOM_CATEGORY)

        app_state.custom_category_label.grid(row=5, column=0, padx=5, pady=5)
        app_state.custom_category_entry.grid(row=5, column=1, padx=5, pady=5)

        app_state.custom_category_entry.delete(0, tk.END)
        app_state.custom_category_entry.insert(0, category)

    app_state.amount_entry.delete(0, tk.END)
    app_state.amount_entry.insert(0, values[4])

    app_state.description_entry.delete(0, tk.END)
    app_state.description_entry.insert(0, values[5])


def save_changes():

    if app_state.editing_transaction_id is None:

        messagebox.showwarning(
            "No Edit",
            "Select a transaction to edit first."
        )
        return

    transaction_type = app_state.type_combobox.get()

    date = app_state.date_entry.get()

    category = get_category(
        app_state.category_combobox, 
        app_state.custom_category_entry
    )

    if category is None:

        return

    amount = validate_amount(app_state.amount_entry)

    if amount is None:

        return
    
    description = validate_description(app_state.description_entry)

    if description is None:

        return
    
    rows = []

    with open(CSV_FILE, "r", newline="", encoding="utf-8") as file:

        reader = csv.reader(file)

        header = next(reader)

        for row in reader:

            if row[0] == str(app_state.editing_transaction_id):

                row = [row[0], date, transaction_type, category, amount, description]

            rows.append(row)

    create_backup()

    with open(CSV_FILE, "w", newline="", encoding="utf-8") as file:

        writer = csv.writer(file)

        writer.writerow(header)

        writer.writerows(rows)

    app_state.editing_transaction_id = None

    refresh_category_combobox()

    clear_inputs()

    update_summary()

    apply_filter()

    messagebox.showinfo(
        "Success",
        "Transaction updated successfully."
    )