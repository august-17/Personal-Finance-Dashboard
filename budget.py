from imports import *
from constants import *

def load_budget():

    if not os.path.exists(BUDGET_FILE):

        return 0

    try:

        with open(BUDGET_FILE, "r", encoding="utf-8") as file:

            return float(file.read())

    except ValueError:

        return 0


def check_budget_warning(amount):

    if type_combobox.get() != "Expense":

        return True

    budget = load_budget()

    if budget == 0:

        return True

    current_month = datetime.now().strftime("%Y-%m")

    monthly_expenses = 0

    transactions = read_transactions()

    for row in transactions:

        if (
            row["Type"] == "Expense"
            and row["Date"].startswith(current_month)
        ):
            
            monthly_expenses += float(row["Amount"])

    if monthly_expenses + amount > budget:

        return messagebox.askyesno(
            "Budget Warning",
            "This transaction exceeds your monthly budget.\n\nDo you want to continue?"
        )

    return True



def check_category_budget_warning(category, amount):

    if type_combobox.get() != "Expense":

        return True

    category_budgets = load_category_budgets()

    if category not in category_budgets:

        return True

    budget = category_budgets[category]

    current_month = datetime.now().strftime("%Y-%m")

    category_spent = 0

    transactions = read_transactions()

    for row in transactions:

        if (
            row["Type"] == "Expense"
            and row["Category"] == category
            and row["Date"].startswith(current_month)
        ):

            category_spent += float(row["Amount"])

    if category_spent + amount > budget:

        return messagebox.askyesno(
            "Category Budget Warning",
            f"This transaction exceeds the budget for '{category}'.\n\n"
            "Do you want to continue?"
        )

    return True



def load_category_budgets():

    if not os.path.exists(CATEGORY_BUDGET_FILE):

        return {}

    try:

        with open(CATEGORY_BUDGET_FILE, "r", encoding="utf-8") as file:

            return json.load(file)

    except (FileNotFoundError, json.JSONDecodeError):

        return {}



def save_category_budgets(category_budgets):

    with open(CATEGORY_BUDGET_FILE, "w", encoding="utf-8") as file:

        json.dump(category_budgets, file, indent=4)



def open_category_budget_window():

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

            entry.insert(
                0,
                str(saved_budgets[category])
            )

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

        try:

            budget = float(budget)

        except ValueError:

            messagebox.showerror(
                "Error",
                f"Budget for {category} must be a number."
            )

            return

        if budget <= 0:

            messagebox.showerror(
                "Error",
                f"Budget for {category} must be greater than zero."
            )

            return

        if budget > MAX_AMOUNT:

            messagebox.showerror(
                "Error",
                f"Budget for {category} cannot exceed ₹{MAX_AMOUNT:,}."
            )

            return

        category_budgets[category] = budget

    save_category_budgets(category_budgets)

    messagebox.showinfo(
        "Success",
        "Category budgets saved successfully."
    )

    budget_window.destroy()



def save_budget():

    budget = budget_entry.get().strip()

    if not budget:

        messagebox.showerror(
            "Error",
            "Please enter a budget amount."
        )
        return

    try:

        budget = float(budget)

    except ValueError:

        messagebox.showerror(
            "Error",
            "Budget must be a number."
        )
        return

    if budget <= 0:

        messagebox.showerror(
            "Error",
            "Budget must be greater than zero."
        )
        return
    
    if budget > MAX_AMOUNT:

        messagebox.showerror(
            "Error",
            f"Budget cannot exceed ₹{MAX_AMOUNT:,}."
        )
        return

    with open(BUDGET_FILE, "w", encoding="utf-8") as file:

        file.write(str(budget))

    update_summary()

    messagebox.showinfo(
        "Success",
        "Budget saved successfully."
    )



def reset_budget():

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