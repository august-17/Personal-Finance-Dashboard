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



root = tk.Tk()
root.title("Personal Finance Dashboard")
root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
root.resizable(True, True)

# Title
title_label = tk.Label(
    root,
    text="Personal Finance Dashboard",
    font=TITLE_FONT
)
title_label.pack(pady=10)

#Summary Frame
summary_frame = tk.Frame(root)

summary_frame.pack(pady=10)

income_label = tk.Label(
    summary_frame,
    text="Total Income: ₹0.00",
    font=LABEL_FONT
)

income_label.grid(row=0, column=0, padx=20)

expense_label = tk.Label(
    summary_frame,
    text="Total Expenses: ₹0.00",
    font=LABEL_FONT
)

expense_label.grid(row=0, column=1, padx=20)

balance_label = tk.Label(
    summary_frame,
    text="Current Balance: ₹0.00",
    font=LABEL_FONT
)

balance_label.grid(row=0, column=2, padx=20)

budget_label = tk.Label(
    summary_frame,
    text="Monthly Budget: ₹0.00",
    font=LABEL_FONT
)

budget_label.grid(row=1, column=0, padx=20)

status_label = tk.Label(
    summary_frame,
    text="Budget Status: Not Set",
    font=LABEL_FONT
)

status_label.grid(row=1, column=2, padx=20)

# Budget Frame
budget_frame = tk.Frame(root)

budget_frame.pack(pady=5)

tk.Label(budget_frame, text="Monthly Budget").grid(row=0, column=0, padx=5)

budget_entry = tk.Entry(budget_frame, width=20)

budget_entry.grid(row=0, column=1, padx=5)

saved_budget = load_budget()

if saved_budget > 0:
    budget_entry.insert(0, str(saved_budget))

# Set Budget Button
budget_button = tk.Button(
    budget_frame,
    text="Set Budget",
    command=lambda: save_budget(budget_entry)
)

budget_button.grid(row=0, column=2, padx=5)

# Reset Budget Button
reset_budget_button = tk.Button(
    budget_frame,
    text="Reset Budget",
    command=lambda: reset_budget(budget_entry)
)

reset_budget_button.grid(row=0, column=3, padx=5)

# Category Budgets Button
category_budget_button = tk.Button(
    budget_frame,
    text="Category Budgets",
    command=lambda: open_category_budget_window(root)
)

category_budget_button.grid(row=0, column=4, padx=5)

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

category_combobox.bind(
    "<<ComboboxSelected>>",
    handle_category_change
)

# Add Transaction Button
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

search_entry.bind(
    "<KeyRelease>",
    debounce_search
)

# Filter
tk.Label(search_frame, text="Type").grid(row=0, column=2, padx=5)

filter_combobox = ttk.Combobox(
    search_frame,
    values=["All", "Income", "Expense"],
    state="readonly",
    width=15
)

filter_combobox.grid(row=0, column=3,padx=5)
filter_combobox.current(0)

filter_combobox.bind(
    "<<ComboboxSelected>>",
    lambda event: apply_filter()
)

# Reset Filter Button
reset_button = tk.Button(
    search_frame,
    text="Reset Filter",
    command=reset_filter
)

reset_button.grid(row=0, column=4, padx=5)

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

# Delete Transaction(s) Button
delete_button = tk.Button(
    action_frame,
    text="Delete Selected Transaction(s)",
    command=delete_transaction
)

delete_button.grid(row=0, column=2, padx=5, pady=5)

# Undo Delete Button
undo_delete_button = tk.Button(
    action_frame,
    text="Undo Delete",
    command=undo_delete,
    state="disabled"
)

undo_delete_button.grid(row=0, column=3, padx=5, pady=5)

# Monthly Expense Breakdown Button
chart_button = tk.Button(
    action_frame,
    text="Monthly Expense Breakdown",
    command=lambda: open_month_selector(
        root,
        "Show Expense Breakdown",
        generate_expense_breakdown
    )
)

chart_button.grid(row=1, column=0, padx=5, pady=5)

# Monthly Category-Wise Spending Report 
category_report_button = tk.Button(
    action_frame,
    text="Monthly Category Report",
    command=lambda: open_month_selector(
        root,
        "Show Report",
        lambda selector, month, year:
            generate_category_report(
                root,
                selector,
                month,
                year
            )
    )
)

category_report_button.grid(row=2, column=0, padx=5, pady=5)

# Monthly Summary Button
monthly_summary_button = tk.Button(
    action_frame,
    text="Monthly Summary",
    command=lambda: open_month_selector(
        root,
        "Show Summary",
        lambda selector, month, year:
            generate_monthly_summary(
                root,
                selector,
                month,
                year
            )
    )
)

monthly_summary_button.grid(row=2, column=1, padx=5, pady=5)

# Monhly Category Budget Status Button
category_budget_status_button = tk.Button(
    action_frame,
    text="Monthly Category Budget Status",
    command=lambda: open_month_selector(
        root,
        "Show Status",
        lambda selector, month, year:
            generate_category_budget_status(
                root,
                selector,
                month,
                year
            )
    )
)

category_budget_status_button.grid(row=2, column=2, padx=5, pady=5)

# Monthly Expense Trend Button
trend_button = tk.Button(
    action_frame,
    text="Monthly Trend",
    command=show_monthly_trend
)

trend_button.grid(row=1, column=1, padx=5, pady=5)

# Export button
export_button = tk.Button(
    action_frame,
    text="Export Financial Report",
    command=lambda: export_report(root)
)

export_button.grid(row=1, column=2, padx=5, pady=5)

# Table Frame
table_frame = tk.Frame(root)

table_frame.pack(fill="both", expand=True, padx=20, pady=20)

# Transaction Table
columns = ("ID", "Date", "Type", "Category", "Amount", "Description")

tree = ttk.Treeview(
    table_frame,
    columns=columns,
    show="headings",
    selectmode="extended"
)

for column in columns:

    if column in ("Date", "Amount", "Category"):

        tree.heading(
            column,
            text=column,
            command=lambda c=column: sort_treeview(c)
        )

    else:

        tree.heading(
            column,
            text=column
        )

    if column == "ID":

        tree.column(column, width=0, stretch=False)

    elif column == "Description":

        tree.column(column, width=350, minwidth=250, anchor="w", stretch=True)

    elif column == "Category":

        tree.column(column, width=180, minwidth=140, anchor="center", stretch=True)

    elif column == "Amount":

        tree.column(column, width=120, minwidth=100, anchor="e", stretch=False)

    else:

        tree.column(column, width=140, minwidth=100, anchor="center", stretch=True)

update_sort_headers()

tree.tag_configure(
    "evenrow",
    background=EVEN_ROW_COLOR
)

tree.tag_configure(
    "oddrow",
    background=ODD_ROW_COLOR
)

# Vertical Scrollbar
scrollbar_y = ttk.Scrollbar(
    table_frame,
    orient="vertical",
    command=tree.yview
)

tree.configure(yscrollcommand=scrollbar_y.set)

enable_mousewheel_scrolling(tree)

# Horizontal Scrollbar
scrollbar_x = ttk.Scrollbar(
    table_frame,
    orient="horizontal",
    command=tree.xview
)

tree.configure(xscrollcommand=scrollbar_x.set)

# Pack Widgets
scrollbar_y.pack(side="right", fill="y")

scrollbar_x.pack(side="bottom", fill="x")

tree.pack(side="left", fill="both", expand=True)



load_transactions()

update_summary()

root.bind("<Return>", shortcut_add)

root.bind("<Control-s>", shortcut_save)

root.bind("<Delete>", shortcut_delete)

root.bind("<Control-z>", shortcut_undo)

root.bind("<Control-e>", shortcut_edit)

root.bind("<Control-f>", shortcut_search)

root.bind("<Escape>", shortcut_clear)

root.mainloop()