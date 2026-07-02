import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from tkcalendar import DateEntry

from constants import (
    SORTABLE_COLUMNS,
    WINDOW_WIDTH,
    WINDOW_HEIGHT,
    TITLE_FONT,
    LABEL_FONT,
    CATEGORIES,
    COLUMNS,
    EVEN_ROW_COLOR,
    ODD_ROW_COLOR
)

from storage import load_budget

from dialogs import open_month_selector

from reports import (
    generate_monthly_summary, 
    generate_category_report, 
    generate_category_budget_status
)

from charts import (
    show_monthly_trend, 
    generate_expense_breakdown
)

from exports import export_report

from budgets import (
    save_budget, 
    reset_budget, 
    open_category_budget_window
)

from ui_helpers import enable_mousewheel_scrolling

from operations import (
    add_transaction,
    load_transactions,
    delete_transaction,
    edit_transaction,
    save_changes,
    undo_delete,
    apply_filter,
    reset_filter
)

from gui_actions import (
    update_sort_headers,
    update_summary,
    clear_inputs
)

import app_state



# ========================================
# Keyboard Shortcuts
# ========================================

def shortcut_add(event=None):
    add_transaction()


def shortcut_save(event=None):
    save_changes()


def shortcut_delete(event=None):
    delete_transaction()


def shortcut_undo(event=None):
    undo_delete()


def shortcut_edit(event=None):
    edit_transaction()


def shortcut_search(event=None):
    app_state.search_entry.focus_set()


def shortcut_clear(event=None):
    clear_inputs()


# ========================================
# Input Helpers
# ========================================

def handle_category_change(event):

    if app_state.category_combobox.get() == "Other":

        app_state.custom_category_label.grid(row=5, column=0, padx=5, pady=5)
        app_state.custom_category_entry.grid(row=5, column=1, padx=5, pady=5)

    else:

        app_state.custom_category_label.grid_remove()
        app_state.custom_category_entry.grid_remove()


def debounce_search(event=None):

    if app_state.search_after_id is not None:

        app_state.root.after_cancel(app_state.search_after_id)

    app_state.search_after_id = app_state.root.after(250, apply_filter)


# ========================================
# Report Callbacks
# ========================================

def open_summary_selector():

    open_month_selector(
        app_state.root,
        "Show Summary",
        open_monthly_summary
    )


def open_monthly_summary(selector, month, year):

    generate_monthly_summary(
        app_state.root,
        selector,
        month,
        year
    )


def open_category_report_selector():

    open_month_selector(
        app_state.root,
        "Generate Report",
        open_category_report
    )


def open_category_report(selector, month, year):

    generate_category_report(
        app_state.root,
        selector,
        month,
        year
    )


def open_category_budget_status_selector():

    open_month_selector(
        app_state.root,
        "Show Status",
        open_category_budget_status
    )


def open_category_budget_status(selector, month, year):

    generate_category_budget_status(
        app_state.root,
        selector,
        month,
        year
    )


# ========================================
# GUI Creation
# ========================================

def create_gui():

    app_state.root = tk.Tk()
    app_state.root.title("Personal Finance Dashboard")
    app_state.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
    app_state.root.resizable(True, True)

    #--------------------------------------------------
    # Title
    #--------------------------------------------------
    title_label = tk.Label(
        app_state.root,
        text="Personal Finance Dashboard",
        font=TITLE_FONT
    )
    title_label.pack(pady=10)

    #--------------------------------------------------
    # Summary Frame
    #--------------------------------------------------
    summary_frame = tk.Frame(app_state.root)

    summary_frame.pack(pady=10)

    app_state.income_label = tk.Label(
        summary_frame,
        text="Total Income: ₹0.00",
        font=LABEL_FONT
    )
    app_state.income_label.grid(row=0, column=0, padx=20)

    app_state.expense_label = tk.Label(
        summary_frame,
        text="Total Expenses: ₹0.00",
        font=LABEL_FONT
    )
    app_state.expense_label.grid(row=0, column=1, padx=20)

    app_state.balance_label = tk.Label(
        summary_frame,
        text="Current Balance: ₹0.00",
        font=LABEL_FONT
    )
    app_state.balance_label.grid(row=0, column=2, padx=20)

    app_state.budget_label = tk.Label(
        summary_frame,
        text="Monthly Budget: ₹0.00",
        font=LABEL_FONT
    )
    app_state.budget_label.grid(row=1, column=0, padx=20)

    app_state.status_label = tk.Label(
        summary_frame,
        text="Budget Status: Not Set",
        font=LABEL_FONT
    )
    app_state.status_label.grid(row=1, column=2, padx=20)

    #--------------------------------------------------
    # Budget Frame
    #--------------------------------------------------
    budget_frame = tk.Frame(app_state.root)

    budget_frame.pack(pady=5)

    tk.Label(budget_frame, text="Monthly Budget").grid(row=0, column=0, padx=5)

    budget_entry = tk.Entry(budget_frame, width=20)
    budget_entry.grid(row=0, column=1, padx=5)

    saved_budget = load_budget()

    if saved_budget > 0:
        budget_entry.insert(0, str(saved_budget))

    #--------------------------------------------------
    # Set Budget Button
    #--------------------------------------------------
    budget_button = tk.Button(
        budget_frame,
        text="Set Budget",
        command=lambda: save_budget(budget_entry)
    )
    budget_button.grid(row=0, column=2, padx=5)

    #--------------------------------------------------
    # Reset Budget Button
    #--------------------------------------------------
    reset_budget_button = tk.Button(
        budget_frame,
        text="Reset Budget",
        command=lambda: reset_budget(budget_entry)
    )
    reset_budget_button.grid(row=0, column=3, padx=5)

    #--------------------------------------------------
    # Category Budgets Button
    #--------------------------------------------------
    category_budget_button = tk.Button(
        budget_frame,
        text="Category Budgets",
        command=lambda: open_category_budget_window(app_state.root)
    )
    category_budget_button.grid(row=0, column=4, padx=5)

    #--------------------------------------------------
    # Input Frame
    #--------------------------------------------------
    input_frame = tk.Frame(app_state.root)
    input_frame.pack(pady=10)

    #--------------------------------------------------
    # Date
    #--------------------------------------------------
    tk.Label(input_frame, text="Date").grid(row=0, column=0, padx=5, pady=5)

    app_state.date_entry = DateEntry(
        input_frame,
        width=20,
        date_pattern="yyyy-mm-dd"
    )
    app_state.date_entry.grid(row=0, column=1, padx=5, pady=5)

    #--------------------------------------------------
    # Type
    #--------------------------------------------------
    tk.Label(input_frame, text="Type").grid(row=1, column=0, padx=5, pady=5)

    app_state.type_combobox = ttk.Combobox(
        input_frame,
        values=["Expense", "Income"],
        state="readonly",
        width=20
    )
    app_state.type_combobox.grid(row=1, column=1, padx=5, pady=5)
    app_state.type_combobox.current(0)

    #--------------------------------------------------
    # Category
    #--------------------------------------------------
    tk.Label(input_frame, text="Category").grid(row=2, column=0, padx=5, pady=5)

    app_state.category_combobox = ttk.Combobox(
        input_frame,
        values=CATEGORIES,
        state="readonly",
        width=20
    )
    app_state.category_combobox.grid(row=2, column=1, padx=5, pady=5)
    app_state.category_combobox.current(0)

    #--------------------------------------------------
    #Custom category
    #--------------------------------------------------
    app_state.custom_category_label = tk.Label(input_frame, text="Custom Category")
    app_state.custom_category_entry = tk.Entry(input_frame, width=23)

    app_state.custom_category_label.grid(row=5, column=0, padx=5, pady=5)
    app_state.custom_category_entry.grid(row=5, column=1, padx=5, pady=5)

    app_state.custom_category_label.grid_remove()
    app_state.custom_category_entry.grid_remove()

    #--------------------------------------------------
    # Amount
    #--------------------------------------------------
    tk.Label(input_frame, text="Amount").grid(row=3, column=0, padx=5, pady=5)

    app_state.amount_entry = tk.Entry(input_frame, width=23)
    app_state.amount_entry.grid(row=3, column=1, padx=5, pady=5)

    #--------------------------------------------------
    # Description
    #--------------------------------------------------
    tk.Label(input_frame, text="Description").grid(row=4, column=0, padx=5, pady=5)

    app_state.description_entry = tk.Entry(input_frame, width=23)
    app_state.description_entry.grid(row=4, column=1, padx=5, pady=5)

    app_state.category_combobox.bind(
        "<<ComboboxSelected>>",
        handle_category_change
    )

    #--------------------------------------------------
    # Add Transaction Button
    #--------------------------------------------------
    add_button = tk.Button(
        input_frame,
        text="Add Transaction",
        command=add_transaction
    )
    add_button.grid(row=6, column=0, columnspan=2, pady=10)

    #--------------------------------------------------
    # Search Frame
    #--------------------------------------------------
    search_frame = tk.Frame(app_state.root)
    search_frame.pack(pady=10)

    tk.Label(search_frame, text="Search").grid(row=0, column=0, padx=5)

    app_state.search_entry = tk.Entry(search_frame, width=30)
    app_state.search_entry.grid(row=0, column=1, padx=5)

    app_state.search_entry.bind(
        "<KeyRelease>",
        debounce_search
    )

    #--------------------------------------------------
    # Filter
    #--------------------------------------------------
    tk.Label(search_frame, text="Type").grid(row=0, column=2, padx=5)

    app_state.filter_combobox = ttk.Combobox(
        search_frame,
        values=["All", "Income", "Expense"],
        state="readonly",
        width=15
    )

    app_state.filter_combobox.grid(row=0, column=3,padx=5)
    app_state.filter_combobox.current(0)

    app_state.filter_combobox.bind(
        "<<ComboboxSelected>>",
        lambda event: apply_filter()
    )

    #--------------------------------------------------
    # Reset Filter Button
    #--------------------------------------------------
    reset_button = tk.Button(
        search_frame,
        text="Reset Filter",
        command=reset_filter
    )
    reset_button.grid(row=0, column=4, padx=5)

    #--------------------------------------------------
    # Action Frame
    #--------------------------------------------------
    action_frame = tk.Frame(app_state.root)

    action_frame.pack(pady=10)

    #--------------------------------------------------
    # Edit Transaction Button
    #--------------------------------------------------
    edit_button = tk.Button(
        action_frame,
        text="Edit Selected Transaction",
        command=edit_transaction
    )
    edit_button.grid(row=0, column=0, padx=5, pady=5)

    #--------------------------------------------------
    # Save Changes Button
    #--------------------------------------------------
    save_button = tk.Button(
        action_frame,
        text="Save Changes",
        command=save_changes
    )
    save_button.grid(row=0, column=1, padx=5, pady=5)

    #--------------------------------------------------
    # Delete Transaction(s) Button
    #--------------------------------------------------
    delete_button = tk.Button(
        action_frame,
        text="Delete Selected Transaction(s)",
        command=delete_transaction
    )
    delete_button.grid(row=0, column=2, padx=5, pady=5)

    #--------------------------------------------------
    # Undo Delete Button
    #--------------------------------------------------
    app_state.undo_delete_button = tk.Button(
        action_frame,
        text="Undo Delete",
        command=undo_delete,
        state="disabled"
    )
    app_state.undo_delete_button.grid(row=0, column=3, padx=5, pady=5)

    #--------------------------------------------------
    # Monthly Expense Breakdown Button
    #--------------------------------------------------
    chart_button = tk.Button(
        action_frame,
        text="Monthly Expense Breakdown",
        command=lambda: open_month_selector(
            app_state.root,
            "Show Expense Breakdown",
            generate_expense_breakdown
        )
    )
    chart_button.grid(row=1, column=0, padx=5, pady=5)

    #--------------------------------------------------
    # Monthly Category-Wise Spending Report Button
    #--------------------------------------------------
    category_report_button = tk.Button(
        action_frame,
        text="Monthly Category Report",
        command=open_category_report_selector
    )
    category_report_button.grid(row=2, column=0, padx=5, pady=5)

    #--------------------------------------------------
    # Monthly Summary Button
    #--------------------------------------------------
    monthly_summary_button = tk.Button(
        action_frame,
        text="Monthly Summary",
        command=open_summary_selector
    )
    monthly_summary_button.grid(row=2, column=1, padx=5, pady=5)

    #--------------------------------------------------
    # Monhly Category Budget Status Button
    #--------------------------------------------------
    category_budget_status_button = tk.Button(
        action_frame,
        text="Monthly Category Budget Status",
        command=open_category_budget_status_selector
    )
    category_budget_status_button.grid(row=2, column=2, padx=5, pady=5)

    #--------------------------------------------------
    # Monthly Expense Trend Button
    #--------------------------------------------------
    trend_button = tk.Button(
        action_frame,
        text="Monthly Trend",
        command=show_monthly_trend
    )
    trend_button.grid(row=1, column=1, padx=5, pady=5)

    #--------------------------------------------------
    # Export button
    #--------------------------------------------------
    export_button = tk.Button(
        action_frame,
        text="Export Financial Report",
        command=lambda: export_report(app_state.root)
    )
    export_button.grid(row=1, column=2, padx=5, pady=5)

    #--------------------------------------------------
    # Table Frame
    #--------------------------------------------------
    table_frame = tk.Frame(app_state.root)

    table_frame.pack(fill="both", expand=True, padx=20, pady=20)

    #--------------------------------------------------
    # Transaction Table
    #--------------------------------------------------
    app_state.tree = ttk.Treeview(
        table_frame,
        columns=COLUMNS,
        show="headings",
        selectmode="extended"
    )

    for column in COLUMNS:

        app_state.tree.heading(column, text=column)

        if column == "ID":

            app_state.tree.column(column, width=0, stretch=False)

        elif column == "Description":

            app_state.tree.column(column, width=350, minwidth=250, anchor="w", stretch=True)

        elif column == "Category":

            app_state.tree.column(column, width=180, minwidth=140, anchor="center", stretch=True)

        elif column == "Amount":

            app_state.tree.column(column, width=120, minwidth=100, anchor="e", stretch=False)

        else:

            app_state.tree.column(column, width=140, minwidth=100, anchor="center", stretch=True)

    update_sort_headers()

    app_state.tree.tag_configure(
        "evenrow",
        background=EVEN_ROW_COLOR
    )

    app_state.tree.tag_configure(
        "oddrow",
        background=ODD_ROW_COLOR
    )

    #--------------------------------------------------
    # Vertical Scrollbar
    #--------------------------------------------------
    scrollbar_y = ttk.Scrollbar(
        table_frame,
        orient="vertical",
        command=app_state.tree.yview
    )

    app_state.tree.configure(yscrollcommand=scrollbar_y.set)

    enable_mousewheel_scrolling(app_state.tree)

    #--------------------------------------------------
    # Horizontal Scrollbar
    #--------------------------------------------------
    scrollbar_x = ttk.Scrollbar(
        table_frame,
        orient="horizontal",
        command=app_state.tree.xview
    )

    app_state.tree.configure(xscrollcommand=scrollbar_x.set)

    #--------------------------------------------------
    # Pack Widgets
    #--------------------------------------------------
    scrollbar_y.pack(side="right", fill="y")

    scrollbar_x.pack(side="bottom", fill="x")

    app_state.tree.pack(side="left", fill="both", expand=True)



    load_transactions()

    update_summary()

    app_state.root.bind("<Return>", shortcut_add)

    app_state.root.bind("<Control-s>", shortcut_save)

    app_state.root.bind("<Delete>", shortcut_delete)

    app_state.root.bind("<Control-z>", shortcut_undo)

    app_state.root.bind("<Control-e>", shortcut_edit)

    app_state.root.bind("<Control-f>", shortcut_search)

    app_state.root.bind("<Escape>", shortcut_clear)

    app_state.root.mainloop()