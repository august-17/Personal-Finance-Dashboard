# Root Window
root = None

# Treeview
tree = None

# Input Widgets
amount_entry = None
description_entry = None
date_entry = None

type_combobox = None
category_combobox = None
custom_category_entry = None
custom_category_label = None

# Search
search_entry = None
filter_combobox = None

# Buttons
undo_delete_button = None

# Dashboard Labels
income_label = None
expense_label = None
balance_label = None
budget_label = None
status_label = None

# Treeview Sorting State
sort_reverse = {"Date": True}
sort_column = "Date"

# Search Debounce
search_after_id = None

# Transaction State
editing_transaction_id = None
delete_history = []