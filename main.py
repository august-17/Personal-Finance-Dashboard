from constants import *
from storage import *
from validation import *
from dialogs import *

editing_transaction_id = None

sort_reverse = {"Date": True}
sort_column = "Date"

delete_history = []

search_after_id = None



def add_transaction():

    transaction_type = type_combobox.get()

    category = get_category(category_combobox, custom_category_entry)

    if category is None:

        return

    amount = validate_amount(amount_entry)

    if amount is None:

        return
    
    if not check_budget_warning(amount):

        return
    
    if not check_category_budget_warning(category, amount):

        return
    
    description = validate_description(description_entry)

    if description is None:

        return
    
    transaction_id = get_next_id()

    date = date_entry.get()

    create_backup()

    with open(CSV_FILE, "a", newline="", encoding="utf-8") as file:

        writer = csv.writer(file)

        writer.writerow([transaction_id, date, transaction_type, category, amount, description])

    clear_inputs()

    update_summary()

    apply_filter()

    







def load_transactions():

    try:

        transactions = read_transactions()

        transactions.sort(key=lambda row: row["Date"], reverse=True)

        for row in transactions:

            insert_row((
                row["ID"],
                row["Date"],
                row["Type"],
                row["Category"],
                row["Amount"],
                row["Description"]
            ))

    except Exception as e:

        messagebox.showerror(
            "CSV Error",
            f"Unable to load transactions.\n\n{e}"
        )



def update_summary():

    try:

        summary = calculate_summary()

        income_label.config(text=f"Monthly Income: ₹{summary['monthly_income']:,.2f}")

        expense_label.config(text=f"Monthly Expenses: ₹{summary['monthly_expenses']:,.2f}")

        budget_label.config(text=f"Monthly Budget: ₹{summary['budget']:,.2f}")

        balance = summary["balance"]

        if balance >= 0:

            balance_label.config(text=f"Current Balance: ₹{balance:,.2f}", fg="green")

        else:

            balance_label.config(text=f"Current Deficit: ₹{abs(balance):,.2f}", fg="red")

        budget = summary["budget"]
        remaining_budget = summary["remaining_budget"]

        if budget == 0:

            status_label.config(text="Budget Status: Not Set", fg="black")

        elif remaining_budget >= 0:

            status_label.config(text=f"Budget Status: ₹{remaining_budget:,.2f} Remaining", fg="green")

        else:

            status_label.config(text=f"Budget Status: ₹{abs(remaining_budget):,.2f} Exceeded", fg="red")

    except Exception as e:

        messagebox.showerror(
            "CSV Error",
            f"Unable to calculate summary.\n\n{e}"
        )



def apply_filter():

    for item in tree.get_children():

        tree.delete(item)

    search_text = " ".join(search_entry.get().lower().strip())

    selected_type = filter_combobox.get()

    transactions = read_transactions()

    for row in transactions:

        date = " ".join(row["Date"].lower().split())
        transaction_type = " ".join(row["Type"].lower().split())
        category = " ".join(row["Category"].lower().split())
        amount = " ".join(row["Amount"].lower().split())
        description = " ".join(row["Description"].lower().split())

        matches_search = (
            search_text in date
            or search_text in transaction_type
            or search_text in category
            or search_text in amount
            or search_text in description
        )

        matches_type = (selected_type == "All" or row["Type"] == selected_type)

        if matches_search and matches_type:
                
            insert_row((
                row["ID"],
                row["Date"],
                row["Type"],
                row["Category"],
                row["Amount"],
                row["Description"]
            ))

    if sort_column is not None:

        sort_treeview(sort_column,toggle=False)







def reset_filter():

    search_entry.delete(0, tk.END)

    filter_combobox.current(0)

    apply_filter()







def delete_transaction():

    global delete_history

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

    transaction_ids = set()

    current_delete = []

    for item in selected_item:

        values = tree.item(item, "values")
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

    delete_history.append(current_delete)

    apply_filter()

    update_summary()

    undo_delete_button.config(state="normal")



def undo_delete():

    global delete_history

    if not delete_history:

        messagebox.showinfo(
            "Undo Delete",
            "Nothing to undo."
        )

        return
    
    last_deleted_transactions = delete_history.pop()
    
    transactions = read_transactions()

    for index, transaction in sorted(last_deleted_transactions, key=lambda x: x[0]):

        transactions.insert(index, transaction)

    create_backup()

    with open(CSV_FILE, "w", newline="", encoding="utf-8") as file:

        writer = csv.DictWriter(file, fieldnames=CSV_HEADERS)

        writer.writeheader()

        writer.writerows(transactions)

    if not delete_history:

        undo_delete_button.config(state="disabled")

    apply_filter()

    update_summary()

    messagebox.showinfo(
        "Undo Delete",
        "Deleted transaction(s) restored successfully."
    )



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

    category = get_category(category_combobox, custom_category_entry)

    if category is None:

        return

    amount = validate_amount(amount_entry)

    if amount is None:

        return
    
    description = validate_description(description_entry)

    if description is None:

        return
    
    rows = []

    with open(CSV_FILE, "r", newline="", encoding="utf-8") as file:

        reader = csv.reader(file)

        header = next(reader)

        for row in reader:

            if row[0] == str(editing_transaction_id):

                row = [row[0], date, transaction_type, category, amount, description]

            rows.append(row)

    create_backup()

    with open(CSV_FILE, "w", newline="", encoding="utf-8") as file:

        writer = csv.writer(file)

        writer.writerow(header)

        writer.writerows(rows)

    editing_transaction_id = None

    apply_filter()

    update_summary()

    clear_inputs()

    messagebox.showinfo(
        "Success",
        "Transaction updated successfully."
    )



























create_csv_file()


