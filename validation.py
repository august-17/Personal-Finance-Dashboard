import re
from tkinter import messagebox

from constants import *


def validate_amount(amount_entry):

    amount = amount_entry.get().strip()

    if not amount:

        messagebox.showerror(
            "Error",
            "Please enter an amount."
        )

        return None

    try:

        amount = float(amount)

    except ValueError:

        messagebox.showerror(
            "Error",
            "Amount must be a number."
        )

        return None

    if amount < MIN_AMOUNT:

        messagebox.showerror(
            "Error",
            f"Amount must be at least ₹{MIN_AMOUNT}."
        )

        return None

    if amount > MAX_AMOUNT:

        messagebox.showerror(
            "Error",
            f"Amount cannot exceed ₹{MAX_AMOUNT:,}."
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

    if category != "Other":

        return category

    category = custom_category_entry.get().strip()

    if not category:

        messagebox.showerror(
            "Error",
            "Please enter a custom category."
        )

        return None
    
    if len(category) > 30:

        messagebox.showerror(
            "Error",
            "Category name cannot exceed 30 characters."
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