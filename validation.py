import re
from tkinter import messagebox
from datetime import datetime

from constants import (
    MIN_AMOUNT,
    MAX_AMOUNT,
    MAX_DESCRIPTION_LENGTH,
    MAX_CATEGORY_LENGTH,
    CUSTOM_CATEGORY,
)

from storage import (
    load_budget, 
    load_category_budgets
)

from finance import get_monthly_transactions



def validate_numeric_amount(amount_text, field_name="Amount"):

    if not amount_text:

        return None, f"Please enter a {field_name.lower()}."

    try:

        amount = float(amount_text)

    except ValueError:

        return None, f"{field_name} must be a number."

    if amount < MIN_AMOUNT:

        return None, f"{field_name} must be at least ₹{MIN_AMOUNT}."

    if amount > MAX_AMOUNT:

        return None, f"{field_name} cannot exceed ₹{MAX_AMOUNT:,}."

    return amount, None


def validate_amount(amount_entry):

    amount, error = validate_numeric_amount(
        amount_entry.get().strip()
    )

    if error:

        messagebox.showerror(
            "Error",
            error
        )

        return None

    return amount


def validate_description(description_entry):

    description = description_entry.get().strip()

    if len(description) > MAX_DESCRIPTION_LENGTH:

        messagebox.showerror(
            "Error",
            f"Description cannot exceed {MAX_DESCRIPTION_LENGTH} characters."
        )
        return None

    return description


def get_category(category_combobox, custom_category_entry):

    category = category_combobox.get()

    if category != CUSTOM_CATEGORY:

        return category

    category = custom_category_entry.get().strip()

    if not category:

        messagebox.showerror(
            "Error",
            "Please enter a custom category."
        )
        return None
    
    if len(category) > MAX_CATEGORY_LENGTH:

        messagebox.showerror(
            "Error",
            f"Category name cannot exceed {MAX_CATEGORY_LENGTH} characters."
        )
        return None

    if not re.search(r"[A-Za-z]", category):

        messagebox.showerror(
            "Error",
            "Category must contain at least one alphabet."
        )
        return None

    if not re.fullmatch(r"[A-Za-z0-9 &()-]+", category):

        messagebox.showerror(
            "Error",
            "Category contains invalid characters."
        )
        return None

    return category.title()


def is_budget_exceeded(transaction_type, amount, selected_month=None):

    if transaction_type != "Expense":

        return False

    budget = load_budget()

    if budget == 0:

        return False
    
    if selected_month is None:

        selected_month = datetime.now().strftime("%Y-%m")

    monthly_expenses = 0

    transactions = get_monthly_transactions(selected_month)

    for row in transactions:

        if row["Type"] == "Expense":

            monthly_expenses += float(row["Amount"])

    return monthly_expenses + amount > budget


def is_category_budget_exceeded(transaction_type, category, amount, selected_month=None):

    if transaction_type != "Expense":

        return False

    category_budgets = load_category_budgets()

    if category not in category_budgets:

        return False
    
    if selected_month is None:

        selected_month = datetime.now().strftime("%Y-%m")

    budget = category_budgets[category]

    category_spent = 0

    transactions = get_monthly_transactions(selected_month)

    for row in transactions:

        if (
            row["Type"] == "Expense"
            and row["Category"] == category
        ):

            category_spent += float(row["Amount"])

    return category_spent + amount > budget