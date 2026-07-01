import os
import tkinter as tk
from tkinter import messagebox

from constants import *
from storage import write_budget, load_category_budgets, save_category_budgets, get_all_categories
from validation import is_budget_exceeded, is_category_budget_exceeded, validate_numeric_amount
from gui import update_summary
from ui_helpers import enable_mousewheel_scrolling



def check_budget_warning(transaction_type, amount):

    if not is_budget_exceeded(transaction_type, amount):

        return True

    return messagebox.askyesno(
        "Budget Warning",
        "This transaction exceeds your monthly budget.\n\n"
        "Do you want to continue?"
    )


def check_category_budget_warning(transaction_type, category, amount):

    if not is_category_budget_exceeded(
        transaction_type,
        category,
        amount
    ):

        return True

    return messagebox.askyesno(
        "Category Budget Warning",
        f"This transaction exceeds the budget for '{category}'.\n\n"
        "Do you want to continue?"
    )


def save_budget(budget_entry):

    budget_text = budget_entry.get().strip()

    budget, error = validate_numeric_amount(budget_text, "Budget")

    if error:

        messagebox.showerror(
            "Error",
            error
        )
        return

    write_budget(budget)

    update_summary()

    messagebox.showinfo(
        "Success",
        "Budget saved successfully."
    )


def reset_budget(budget_entry):

    confirm = messagebox.askyesno(
        "Reset Budget",
        "Are you sure you want to reset the budget?"
    )

    if not confirm:

        return

    if os.path.exists(BUDGET_FILE):

        os.remove(BUDGET_FILE)

    budget_entry.delete(0, tk.END)

    update_summary()

    messagebox.showinfo(
        "Success",
        "Budget reset successfully."
    )


def open_category_budget_window(root):

    budget_window = tk.Toplevel(root)

    budget_window.title("Category Budgets")

    budget_window.geometry(f"{BUDGET_WIDTH}x{BUDGET_HEIGHT}")

    canvas = tk.Canvas(budget_window)

    scrollbar = tk.Scrollbar(
        budget_window,
        orient="vertical",
        command=canvas.yview
    )

    scrollable_frame = tk.Frame(canvas)

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )

    canvas.create_window(
        (0, 0),
        window=scrollable_frame,
        anchor="nw"
    )

    canvas.configure(yscrollcommand=scrollbar.set)

    enable_mousewheel_scrolling(canvas)

    canvas.pack(side="left", fill="both", expand=True)

    scrollbar.pack(side="right", fill="y")

    saved_budgets = load_category_budgets()

    category_entries = {}

    all_categories = get_all_categories()

    for index, category in enumerate(all_categories):

        tk.Label(scrollable_frame, text=category).grid(row=index, column=0, padx=(15, 10), pady=6, sticky="w")

        entry = tk.Entry(scrollable_frame, width=15)

        entry.grid(row=index, column=1, padx=(15, 10), pady=6)

        reset_button = tk.Button(
            scrollable_frame,
            text="Reset",
            width=8,
            command=lambda e=entry: reset_single_category(e)
        )

        reset_button.grid(row=index, column=2, padx=5, pady=6)

        if category in saved_budgets:

            entry.insert(0, str(saved_budgets[category]))

        category_entries[category] = entry

    save_button = tk.Button(
        scrollable_frame,
        text="Save Budgets",
        command=lambda: save_category_budget_entries(
            category_entries,
            budget_window
        )
    )

    save_button.grid(row=len(all_categories), column=0, columnspan=3, padx=10, pady=15)


def reset_single_category(entry):

    entry.delete(0, tk.END)


def save_category_budget_entries(category_entries, budget_window):

    category_budgets = {}

    for category, entry in category_entries.items():

        budget = entry.get().strip()

        if not budget:

            continue

        budget, error = validate_numeric_amount(budget, f"Budget for '{category}'")

        if error:

            messagebox.showerror(
                "Error",
                error
            )
            return

        category_budgets[category] = budget

    save_category_budgets(category_budgets)

    messagebox.showinfo(
        "Success",
        "Category budgets saved successfully."
    )

    budget_window.destroy()